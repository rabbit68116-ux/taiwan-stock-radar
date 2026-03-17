"""Daily 08:30 Taiwan market brief built from live Yahoo and Cnyes pages."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen

from .premarket_brief import generate_premarket_brief

QUOTE_LABELS = {
    "sp500": "S&P 500",
    "nasdaq": "Nasdaq",
    "dow": "Dow",
    "sox": "SOX",
    "tsm_adr": "TSM ADR",
    "nvidia": "NVIDIA",
    "vix": "VIX",
}
BROAD_KEYS = ("sp500", "nasdaq", "dow")
SEMI_KEYS = ("sox", "tsm_adr", "nvidia")


def _fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", "ignore")


def _clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", unescape(value)).strip()
    return value


def _parse_float(value: str) -> float:
    return float(value.replace(",", "").replace("%", ""))


def _exception_text(exc: Exception) -> str:
    text = _clean_text(str(exc))
    if not text:
        return exc.__class__.__name__
    return f"{exc.__class__.__name__}: {text[:120]}"


def _source_status(
    name: str,
    url: str,
    status: str,
    detail: str,
    *,
    category: str,
    critical: bool,
) -> dict[str, Any]:
    return {
        "name": name,
        "url": url,
        "status": status,
        "detail": detail,
        "category": category,
        "critical": critical,
    }


class _AnchorCollector(HTMLParser):
    def __init__(self, href_predicate: Callable[[str], bool], base_url: str) -> None:
        super().__init__()
        self.href_predicate = href_predicate
        self.base_url = base_url
        self.current_href: str | None = None
        self.current_parts: list[str] = []
        self.items: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = dict(attrs)
        href = attr_map.get("href")
        if href and self.href_predicate(href):
            self.current_href = urljoin(self.base_url, href)
            self.current_parts = []

    def handle_data(self, data: str) -> None:
        if self.current_href is not None:
            self.current_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self.current_href is None:
            return
        title = _clean_text("".join(self.current_parts))
        href = self.current_href
        self.current_href = None
        self.current_parts = []
        if not title or len(title) < 8 or title.isdigit():
            return
        self.items.append((href, title))


@dataclass
class MarketHeadline:
    source: str
    section: str
    title: str
    url: str
    sentiment_score: int


def _headline_sentiment(title: str, rules: dict[str, Any]) -> int:
    positive_keywords = rules["headline_sentiment"]["positive_keywords"]
    negative_keywords = rules["headline_sentiment"]["negative_keywords"]
    lower = title.lower()
    score = 0
    for keyword in positive_keywords:
        if keyword.lower() in lower:
            score += 1
    for keyword in negative_keywords:
        if keyword.lower() in lower:
            score -= 1
    return score


def _normalize_yahoo_url(url: str) -> str:
    return url.split("?")[0]


def _collect_yahoo_headlines(url: str, section: str, limit: int, rules: dict[str, Any]) -> list[MarketHeadline]:
    html = _fetch_text(url)
    parser = _AnchorCollector(
        href_predicate=lambda href: href.startswith("/news/") or href.startswith("https://tw.stock.yahoo.com/news/"),
        base_url="https://tw.stock.yahoo.com",
    )
    parser.feed(html)

    items: list[MarketHeadline] = []
    seen: set[str] = set()
    for href, title in parser.items:
        normalized_url = _normalize_yahoo_url(href)
        if normalized_url in seen:
            continue
        seen.add(normalized_url)
        items.append(
            MarketHeadline(
                source="Yahoo奇摩股市",
                section=section,
                title=title,
                url=normalized_url,
                sentiment_score=_headline_sentiment(title, rules),
            )
        )
        if len(items) >= limit:
            break
    return items


def _collect_cnyes_headlines(url: str, section: str, limit: int, rules: dict[str, Any]) -> list[MarketHeadline]:
    html = _fetch_text(url)
    parser = _AnchorCollector(
        href_predicate=lambda href: href.startswith("/news/id/") or href.startswith("https://news.cnyes.com/news/id/"),
        base_url="https://news.cnyes.com",
    )
    parser.feed(html)

    items: list[MarketHeadline] = []
    seen: set[str] = set()
    for href, title in parser.items:
        if href in seen:
            continue
        seen.add(href)
        items.append(
            MarketHeadline(
                source="Anue 鉅亨網",
                section=section,
                title=title,
                url=href,
                sentiment_score=_headline_sentiment(title, rules),
            )
        )
        if len(items) >= limit:
            break
    return items


def _quote_url(symbol: str) -> str:
    return f"https://tw.stock.yahoo.com/quote/{quote(symbol, safe='')}"


def _fetch_yahoo_quote(symbol: str) -> dict[str, Any]:
    url = _quote_url(symbol)
    html = _fetch_text(url)
    pattern = re.compile(
        rf'"libra":\{{"{re.escape(symbol)}":\{{"meta":\{{(.*?)\}},"timestamp"',
        re.S,
    )
    match = pattern.search(html)
    if not match:
        raise ValueError(f"Unable to locate Yahoo quote payload for {symbol}.")

    meta = json.loads("{" + match.group(1) + "}")
    price = float(meta["regularMarketPrice"])
    previous_close = float(meta["previousClose"])
    change = price - previous_close
    change_pct = (change / previous_close) * 100 if previous_close else 0.0
    return {
        "symbol": symbol,
        "name": meta.get("name", symbol),
        "price": price,
        "previous_close": previous_close,
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "market_time": meta.get("regularMarketTime"),
        "timezone": meta.get("timezone"),
    }


def _estimate_volume_ratio(volume: int, rules: dict[str, Any]) -> float:
    if volume >= int(rules["night_session"]["hot_volume_threshold"]):
        return 1.25
    if volume <= int(rules["night_session"]["soft_volume_threshold"]):
        return 0.8
    return 1.0


def _fetch_taiwan_night_session(rules: dict[str, Any]) -> dict[str, Any]:
    html = _fetch_text(rules["sources"]["yahoo_futures_url"])
    symbol = rules["night_session"]["preferred_contract"]
    href_marker = f"https://tw.stock.yahoo.com/future/{symbol.replace('&', '&amp;')}"
    start = html.find(href_marker)
    if start == -1:
        raise ValueError("Unable to locate Yahoo futures near-month row.")
    end = html.find('<li class="List(n)">', start + 1)
    segment = html[start:end if end != -1 else None]

    label_match = re.search(
        r'Fz\(16px\) Ell">([^<]+)</div><div class="D\(f\) Ai\(c\)"><span class="Fz\(14px\) Ell C\(#5b636a\)">([^<]+)</span>',
        segment,
    )
    if not label_match:
        raise ValueError("Unable to parse Yahoo futures label block.")

    values = re.findall(r'>([-+]?\d[\d,]*\.?\d*%?)<', segment)
    if len(values) < 6:
        raise ValueError("Unable to parse Yahoo futures numeric values.")

    price = _parse_float(values[2])
    change = _parse_float(values[3])
    change_pct = _parse_float(values[4])
    volume = int(values[5].replace(",", ""))
    volume_ratio = _estimate_volume_ratio(volume, rules)

    return {
        "label": _clean_text(label_match.group(1)),
        "contract": _clean_text(label_match.group(2)),
        "price": round(price, 2),
        "change": round(change, 2),
        "change_pct": round(change_pct, 2),
        "volume": volume,
        "volume_ratio": volume_ratio,
        "breadth_note": f"{_clean_text(label_match.group(1))} {change_pct:+.2f}% ，成交量 {volume:,}",
    }


def _neutral_quote(symbol: str, label: str, note: str) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "name": label,
        "price": 0.0,
        "previous_close": 0.0,
        "change": 0.0,
        "change_pct": 0.0,
        "market_time": None,
        "timezone": None,
        "data_status": "unavailable",
        "data_note": note,
    }


def _neutral_night_session(contract: str, note: str) -> dict[str, Any]:
    return {
        "label": "台指期近月",
        "contract": contract,
        "price": 0.0,
        "change": 0.0,
        "change_pct": 0.0,
        "volume": 0,
        "volume_ratio": 1.0,
        "breadth_note": note,
        "data_status": "unavailable",
        "data_note": note,
    }


def _safe_fetch_yahoo_quote(key: str, symbol: str) -> tuple[dict[str, Any], dict[str, Any], bool]:
    label = QUOTE_LABELS.get(key, symbol)
    url = _quote_url(symbol)
    try:
        quote_data = _fetch_yahoo_quote(symbol)
        quote_data["data_status"] = "ok"
        quote_data["data_note"] = f"{label} 行情抓取成功。"
        return (
            quote_data,
            _source_status(
                f"Yahoo奇摩股市 / {label}",
                url,
                "ok",
                f"{label} 行情抓取成功。",
                category="market",
                critical=True,
            ),
            True,
        )
    except Exception as exc:
        note = f"{label} 行情暫時無法取得，先以中性值處理。"
        return (
            _neutral_quote(symbol, label, note),
            _source_status(
                f"Yahoo奇摩股市 / {label}",
                url,
                "unavailable",
                f"{note} {_exception_text(exc)}",
                category="market",
                critical=True,
            ),
            False,
        )


def _safe_fetch_taiwan_night_session(rules: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], bool]:
    source_urls = rules["sources"]
    contract = rules["night_session"]["preferred_contract"]
    try:
        night = _fetch_taiwan_night_session(rules)
        night["data_status"] = "ok"
        night["data_note"] = "台指期近月夜盤抓取成功。"
        return (
            night,
            _source_status(
                "Yahoo奇摩股市 / 台指期夜盤",
                source_urls["yahoo_futures_url"],
                "ok",
                "台指期近月夜盤抓取成功。",
                category="market",
                critical=True,
            ),
            True,
        )
    except Exception as exc:
        note = "台指期近月夜盤暫時無法取得，今日開盤偏向對夜盤訊號採保守解讀。"
        return (
            _neutral_night_session(contract, note),
            _source_status(
                "Yahoo奇摩股市 / 台指期夜盤",
                source_urls["yahoo_futures_url"],
                "unavailable",
                f"{note} {_exception_text(exc)}",
                category="market",
                critical=True,
            ),
            False,
        )


def build_live_premarket_context(daily_rules: dict[str, Any]) -> dict[str, Any]:
    source_urls = daily_rules["sources"]
    symbol_map = source_urls["yahoo_quote_symbols"]
    source_statuses: list[dict[str, Any]] = []

    night, night_status, night_ok = _safe_fetch_taiwan_night_session(daily_rules)
    source_statuses.append(night_status)

    quotes: dict[str, dict[str, Any]] = {}
    quote_successes = 0
    major_index_successes = 0
    for key, symbol in symbol_map.items():
        quote_data, status, success = _safe_fetch_yahoo_quote(key, symbol)
        quotes[key] = quote_data
        source_statuses.append(status)
        if success:
            quote_successes += 1
            if key in BROAD_KEYS:
                major_index_successes += 1

    core_signal_total = 1 + len(symbol_map)
    core_signal_successes = quote_successes + (1 if night_ok else 0)

    return {
        "profile_label": "Live 08:30 Yahoo + Cnyes market brief",
        "taiwan_night": {
            "change_pct": night["change_pct"],
            "volume_ratio": night["volume_ratio"],
            "breadth_note": night["breadth_note"],
        },
        "us_markets": {
            "sp500": {"change_pct": quotes["sp500"]["change_pct"]},
            "nasdaq": {"change_pct": quotes["nasdaq"]["change_pct"]},
            "dow": {"change_pct": quotes["dow"]["change_pct"]},
            "sox": {"change_pct": quotes["sox"]["change_pct"]},
            "tsm_adr": {"change_pct": quotes["tsm_adr"]["change_pct"]},
            "nvidia": {"change_pct": quotes["nvidia"]["change_pct"]},
            "vix": {"change_pct": quotes["vix"]["change_pct"]},
        },
        "macro": {
            "night_session_label": night["label"],
            "night_session_contract": night["contract"],
            "night_session_price": night["price"],
            "night_session_volume": night["volume"],
            "night_session_url": source_urls["yahoo_futures_url"],
            "us_quotes": quotes,
        },
        "availability": {
            "core_signal_successes": core_signal_successes,
            "core_signal_total": core_signal_total,
            "core_signal_ratio": round(core_signal_successes / core_signal_total, 3),
            "major_index_successes": major_index_successes,
            "major_index_ratio": round(major_index_successes / len(BROAD_KEYS), 3),
            "night_session_ok": night_ok,
        },
        "source_statuses": source_statuses,
    }


def _format_quote_change(quote_data: dict[str, Any]) -> str:
    if quote_data.get("data_status") != "ok":
        return "資料缺口"
    return f"{quote_data['change_pct']:+.2f}%"


def _average_change(quotes: dict[str, dict[str, Any]], keys: tuple[str, ...]) -> float:
    values = [float(quotes[key]["change_pct"]) for key in keys if quotes[key].get("data_status") == "ok"]
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def _missing_labels(quotes: dict[str, dict[str, Any]], keys: tuple[str, ...]) -> list[str]:
    return [QUOTE_LABELS[key] for key in keys if quotes[key].get("data_status") != "ok"]


def _directional_sentiment(value: float, *, tolerance: float = 0.15, invert: bool = False) -> int:
    if invert:
        if value <= -tolerance:
            return 1
        if value >= tolerance:
            return -1
        return 0
    if value >= tolerance:
        return 1
    if value <= -tolerance:
        return -1
    return 0


def _build_market_signal_items(context: dict[str, Any], premarket_brief: dict[str, Any]) -> list[dict[str, Any]]:
    night = context["macro"]
    quotes = night["us_quotes"]

    night_ok = quotes["sp500"].get("data_status") is not None  # ensures quote metadata exists
    items: list[dict[str, Any]] = []

    night_note = context["taiwan_night"]["breadth_note"]
    if night["night_session_volume"] > 0 and night["night_session_price"] > 0:
        night_title = (
            f"{night['night_session_label']} {night['night_session_contract']} "
            f"{context['taiwan_night']['change_pct']:+.2f}% ，最新 {night['night_session_price']:.2f}，"
            f"量能 {night['night_session_volume']:,}。"
        )
        night_sentiment = _directional_sentiment(float(context["taiwan_night"]["change_pct"]))
    else:
        night_title = f"{night_note} 今日開盤偏向需更依賴現貨第一波量價確認。"
        night_sentiment = 0
        night_ok = False
    items.append(
        {
            "kind": "market_signal",
            "source": "Yahoo奇摩股市",
            "section": "夜盤趨勢",
            "title": night_title,
            "sentiment_score": night_sentiment,
            "url": night["night_session_url"],
        }
    )

    broad_missing = _missing_labels(quotes, BROAD_KEYS)
    broad_avg = _average_change(quotes, BROAD_KEYS)
    if len(broad_missing) == len(BROAD_KEYS):
        broad_title = "美股大盤行情資料暫時無法完整取得，今日大盤外溢訊號改採保守解讀，需等台股現貨第一波量價確認。"
        broad_sentiment = 0
    else:
        broad_title = (
            f"S&P 500 {_format_quote_change(quotes['sp500'])} / Nasdaq {_format_quote_change(quotes['nasdaq'])} / "
            f"Dow {_format_quote_change(quotes['dow'])}，{premarket_brief['opening_bias']}的外盤基底偏向已形成。"
        )
        if broad_missing:
            broad_title += f" 但 {', '.join(broad_missing)} 資料暫時缺口，今日美股大盤訊號採保守解讀。"
        broad_sentiment = _directional_sentiment(broad_avg)
    items.append(
        {
            "kind": "market_signal",
            "source": "Yahoo奇摩股市",
            "section": "美股大盤",
            "title": broad_title,
            "sentiment_score": broad_sentiment,
            "url": "https://tw.stock.yahoo.com/us-market/",
        }
    )

    semi_missing = _missing_labels(quotes, SEMI_KEYS)
    semi_avg = _average_change(quotes, SEMI_KEYS)
    if len(semi_missing) == len(SEMI_KEYS):
        semi_title = "半導體與 AI 領先訊號暫時無法完整取得，電子主線的延續性需等台股開盤後再確認。"
        semi_sentiment = 0
    else:
        semi_title = (
            f"SOX {_format_quote_change(quotes['sox'])} / TSM ADR {_format_quote_change(quotes['tsm_adr'])} / "
            f"NVDA {_format_quote_change(quotes['nvidia'])}，半導體與 AI 供應鏈仍是今日主導訊號。"
        )
        if semi_missing:
            semi_title += f" 但 {', '.join(semi_missing)} 暫時缺口，相關族群評估保留保守折扣。"
        semi_sentiment = _directional_sentiment(semi_avg)
    items.append(
        {
            "kind": "market_signal",
            "source": "Yahoo奇摩股市",
            "section": "半導體領先",
            "title": semi_title,
            "sentiment_score": semi_sentiment,
            "url": _quote_url("^SOX"),
        }
    )

    vix_quote = quotes["vix"]
    if vix_quote.get("data_status") != "ok":
        vix_title = "VIX 資料暫時無法取得，今日風險情緒訊號改採保守解讀，不宜只依賴外盤樂觀敘事。"
        vix_sentiment = 0
    else:
        vix_change_pct = float(vix_quote["change_pct"])
        vix_title = (
            f"VIX {vix_change_pct:+.2f}% ，"
            f"{'避險壓力下降' if vix_change_pct <= 0 else '避險需求升高'}，"
            f"今日宜留意開盤後追價節奏。"
        )
        vix_sentiment = _directional_sentiment(vix_change_pct, invert=True)
    items.append(
        {
            "kind": "market_signal",
            "source": "Yahoo奇摩股市",
            "section": "風險情緒",
            "title": vix_title,
            "sentiment_score": vix_sentiment,
            "url": _quote_url("^VIX"),
        }
    )

    return items


def _collect_headlines_with_status(
    source_name: str,
    section: str,
    url: str,
    limit: int,
    rules: dict[str, Any],
    collector: Callable[[str, str, int, dict[str, Any]], list[MarketHeadline]],
    *,
    include_in_mix: bool,
) -> tuple[list[MarketHeadline], dict[str, Any]]:
    if not include_in_mix or limit <= 0:
        return [], _source_status(
            source_name,
            url,
            "skipped",
            "此來源在 v1.6 正式訊息配比中未納入，以降低雜訊。",
            category="headline",
            critical=False,
        )

    try:
        items = collector(url, section, limit, rules)
    except Exception as exc:
        return [], _source_status(
            source_name,
            url,
            "unavailable",
            f"來源暫時無法取得，新聞流向權重已下調。 {_exception_text(exc)}",
            category="headline",
            critical=False,
        )

    if not items:
        return [], _source_status(
            source_name,
            url,
            "partial",
            "頁面可讀，但目前未擷取到足量可用標題，新聞流向權重已保守處理。",
            category="headline",
            critical=False,
        )

    return items, _source_status(
        source_name,
        url,
        "ok",
        f"取得 {len(items)} 則可用標題。",
        category="headline",
        critical=False,
    )


def _select_headlines_by_plan(
    yahoo_tw: list[MarketHeadline],
    yahoo_us: list[MarketHeadline],
    cnyes_tw: list[MarketHeadline],
    cnyes_us: list[MarketHeadline],
    rules: dict[str, Any],
) -> list[dict[str, Any]]:
    limits = rules["headline_plan"]["source_limits"]
    ordered_groups = [
        yahoo_tw[: int(limits["yahoo_tw"])],
        yahoo_us[: int(limits["yahoo_us"])],
        cnyes_tw[: int(limits["cnyes_tw"])],
        cnyes_us[: int(limits["cnyes_us"])],
    ]

    items: list[dict[str, Any]] = []
    for group in ordered_groups:
        for headline in group:
            items.append(
                {
                    "kind": "headline",
                    "source": headline.source,
                    "section": headline.section,
                    "title": headline.title,
                    "sentiment_score": headline.sentiment_score,
                    "url": headline.url,
                }
            )
    return items[: int(rules["headline_plan"]["headline_slots"])]


def _headline_gap_item(status: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "headline_gap",
        "source": "系統狀態",
        "section": status["name"],
        "title": f"{status['name']} 暫時無法提供足量重點訊息，今日新聞流向評估已保守處理。",
        "sentiment_score": 0,
        "url": status["url"],
    }


def _pad_headline_items(
    items: list[dict[str, Any]],
    headline_statuses: list[dict[str, Any]],
    rules: dict[str, Any],
) -> list[dict[str, Any]]:
    target = int(rules["headline_plan"]["headline_slots"])
    padded = list(items)
    gap_statuses = [status for status in headline_statuses if status["status"] != "ok" and status["status"] != "skipped"]

    for status in gap_statuses:
        if len(padded) >= target:
            break
        padded.append(_headline_gap_item(status))

    while len(padded) < target:
        padded.append(
            {
                "kind": "headline_gap",
                "source": "系統狀態",
                "section": "新聞流向",
                "title": "今日可用新聞數量不足，剩餘配額保留為保守解讀，不以低品質資訊強行填滿。",
                "sentiment_score": 0,
                "url": "",
            }
        )

    return padded[:target]


def _headline_tone_score(headlines: list[dict[str, Any]]) -> float:
    if not headlines:
        return 50.0
    raw_score = sum(item["sentiment_score"] for item in headlines)
    max_abs = max(len(headlines), 1)
    normalized = ((raw_score / max_abs) + 1) / 2
    return round(normalized * 100, 1)


def _headline_coverage_ratio(headline_statuses: list[dict[str, Any]], actual_headline_count: int, rules: dict[str, Any]) -> tuple[float, float]:
    active_sources = [status for status in headline_statuses if status["status"] != "skipped"]
    if not active_sources:
        return 1.0, 1.0
    available_sources = sum(1 for status in active_sources if status["status"] == "ok")
    source_ratio = round(available_sources / len(active_sources), 3)
    target_slots = max(int(rules["headline_plan"]["headline_slots"]), 1)
    slot_ratio = round(min(actual_headline_count, target_slots) / target_slots, 3)
    return source_ratio, slot_ratio


def _apply_reliability_guardrail(
    score: float,
    availability: dict[str, Any],
    headline_source_ratio: float,
    headline_slot_ratio: float,
) -> tuple[float, str]:
    adjusted = float(score)
    notes: list[str] = []

    core_ratio = float(availability["core_signal_ratio"])
    major_ratio = float(availability["major_index_ratio"])
    night_ok = bool(availability["night_session_ok"])

    if core_ratio < 1.0:
        adjusted -= round((1.0 - core_ratio) * 18.0, 1)
        notes.append("部分核心行情來源暫時缺口，市場訊號可信度已下調。")

    severe_market_gap = (not night_ok) or major_ratio < 0.67 or core_ratio < 0.5
    if severe_market_gap:
        adjusted = min(adjusted, 47.9)
        notes.append("因夜盤或美股大盤資料不足，今日綜合評估改採保守解讀。")

    if headline_slot_ratio < 1.0:
        adjusted -= round((1.0 - headline_slot_ratio) * 8.0, 1)
        notes.append("部分新聞來源不足，新聞流向權重已降低。")

    if headline_source_ratio < 0.67:
        adjusted = min(adjusted, 61.9)

    adjusted = max(20.0, round(adjusted, 1))
    return adjusted, " ".join(dict.fromkeys(notes))


def _overall_assessment(score: float) -> tuple[str, str]:
    if score >= 75:
        return (
            "偏多開盤且延續機率較高",
            "夜盤、美股與新聞流向大致同向，台股今天較有機會由電子權值與 AI 供應鏈領漲，但仍需確認開盤後量價是否承接。",
        )
    if score >= 62:
        return (
            "建設性偏強",
            "整體環境偏正向，但盤中是否延續仍取決於大型電子與半導體能否接棒，追價宜有節奏。",
        )
    if score >= 48:
        return (
            "中性偏多",
            "外盤與新聞面偏向中性到正向，但尚未形成壓倒性優勢，今天較可能是開高後分化或盤中震盪整理。",
        )
    if score >= 36:
        return (
            "偏震盪保守",
            "夜盤與新聞面出現雜訊，今天的台股較適合等早盤第一波主線與量能確認，不宜太早放大部位。",
        )
    return (
        "偏弱防守",
        "隔夜環境與新聞面偏空，今天台股較可能以防守盤開出，應優先確認賣壓是否擴散並避免逆勢追價。",
    )


def _source_gap_flags(source_statuses: list[dict[str, Any]]) -> list[str]:
    flags: list[str] = []
    for status in source_statuses:
        if status["status"] == "unavailable":
            if status["category"] == "market":
                flags.append(f"{status['name']} 暫時無法取得，相關市場訊號已改採保守解讀。")
            elif status["category"] == "headline":
                flags.append(f"{status['name']} 暫時無法取得，新聞流向權重已下調。")
        elif status["status"] == "partial" and status["category"] == "headline":
            flags.append(f"{status['name']} 可用標題不足，今日新聞流向評估偏保守。")
    deduped: list[str] = []
    for item in flags:
        if item not in deduped:
            deduped.append(item)
    return deduped[:4]


def generate_daily_market_brief(
    settings: dict[str, Any],
    premarket_rules: dict[str, Any],
    daily_rules: dict[str, Any],
    *,
    analysis_date: str | None = None,
) -> dict[str, Any]:
    analysis_date = analysis_date or date.today().isoformat()
    context = build_live_premarket_context(daily_rules)
    premarket_brief = generate_premarket_brief(
        settings,
        premarket_rules,
        analysis_date=analysis_date,
        context=context,
    )

    source_urls = daily_rules["sources"]
    source_statuses = list(context["source_statuses"])

    yahoo_tw, yahoo_tw_status = _collect_headlines_with_status(
        "Yahoo奇摩股市 / 台股盤勢",
        "台股盤勢",
        source_urls["yahoo_tw_market_url"],
        6,
        daily_rules,
        _collect_yahoo_headlines,
        include_in_mix=True,
    )
    yahoo_us, yahoo_us_status = _collect_headlines_with_status(
        "Yahoo奇摩股市 / 美股盤勢",
        "美股盤勢",
        source_urls["yahoo_us_market_url"],
        4,
        daily_rules,
        _collect_yahoo_headlines,
        include_in_mix=bool(daily_rules["headline_plan"]["source_limits"].get("yahoo_us", 0)),
    )
    cnyes_tw, cnyes_tw_status = _collect_headlines_with_status(
        "Anue 鉅亨網 / 台股新聞",
        "鉅亨台股",
        source_urls["cnyes_tw_stock_url"],
        6,
        daily_rules,
        _collect_cnyes_headlines,
        include_in_mix=True,
    )
    cnyes_us, cnyes_us_status = _collect_headlines_with_status(
        "Anue 鉅亨網 / 美股新聞",
        "鉅亨美股",
        source_urls["cnyes_us_stock_url"],
        4,
        daily_rules,
        _collect_cnyes_headlines,
        include_in_mix=True,
    )
    headline_statuses = [yahoo_tw_status, yahoo_us_status, cnyes_tw_status, cnyes_us_status]
    source_statuses.extend(headline_statuses)

    market_signals = _build_market_signal_items(context, premarket_brief)
    selected_headlines = _select_headlines_by_plan(yahoo_tw, yahoo_us, cnyes_tw, cnyes_us, daily_rules)
    headline_items = _pad_headline_items(selected_headlines, headline_statuses, daily_rules)
    top_messages = (market_signals + headline_items)[: int(daily_rules["headline_plan"]["top_n"])]

    headline_score = _headline_tone_score(selected_headlines)
    weights = daily_rules["summary_weights"]
    raw_overall_score = round(
        premarket_brief["opening_score"] * float(weights["premarket"])
        + headline_score * float(weights["headlines"]),
        1,
    )
    headline_source_ratio, headline_slot_ratio = _headline_coverage_ratio(headline_statuses, len(selected_headlines), daily_rules)
    overall_score, reliability_note = _apply_reliability_guardrail(
        raw_overall_score,
        context["availability"],
        headline_source_ratio,
        headline_slot_ratio,
    )
    overall_label, overall_summary = _overall_assessment(overall_score)
    if reliability_note:
        overall_summary = f"{overall_summary} {reliability_note}".strip()

    risk_flags = list(premarket_brief["risk_flags"])
    for item in _source_gap_flags(source_statuses):
        if item not in risk_flags:
            risk_flags.append(item)

    return {
        "analysis_date": analysis_date,
        "generated_at_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "project": settings.get("project", {}).get("display_name", "Taiwan Stock Radar"),
        "version": settings.get("project", {}).get("plan_version", "v1.6"),
        "report_type": "daily_taiwan_market_brief",
        "scheduled_time_local": daily_rules["schedule"]["report_time_local"],
        "opening_bias": premarket_brief["opening_bias"],
        "opening_score": premarket_brief["opening_score"],
        "headline_score": headline_score,
        "overall_score": overall_score,
        "overall_label": overall_label,
        "overall_summary": overall_summary,
        "premarket_brief": premarket_brief,
        "top_messages": top_messages,
        "sector_watchlist": premarket_brief["sector_watchlist"],
        "risk_flags": risk_flags,
        "sources": source_statuses,
        "disclaimer": (
            "本報告僅供研究、教育與產品展示使用，不構成投資建議、招攬、保證報酬或個別證券推薦。 "
            "This report is for research, education, and product demonstration only. It is not investment advice and does not guarantee intraday performance or future returns."
        ),
    }


def write_daily_market_brief_outputs(
    output_dir: Path,
    brief: dict[str, Any],
    *,
    basename: str = "daily_market_brief",
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{basename}.json").write_text(
        json.dumps(brief, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / f"{basename}.md").write_text(_render_daily_market_brief(brief), encoding="utf-8")


def _render_source_line(record: dict[str, Any]) -> str:
    status_labels = {
        "ok": "可用",
        "partial": "部分可用",
        "unavailable": "資料缺口",
        "skipped": "未納入",
    }
    label = status_labels.get(record["status"], record["status"])
    url = f" ({record['url']})" if record.get("url") else ""
    return f"- {record['name']}：{label}。{record['detail']}{url}"


def _render_daily_market_brief(brief: dict[str, Any]) -> str:
    messages = "\n".join(
        [
            f"{index}. [{item['source']} / {item['section']}] {item['title']}"
            + (f"\n   - 連結：{item['url']}" if item.get("url") else "")
            for index, item in enumerate(brief["top_messages"], start=1)
        ]
    )
    sector_lines = "\n".join(
        [
            f"- {item['sector']}：{item['view']}，{item['reason']}"
            for item in brief["sector_watchlist"]
        ]
    ) or "- 暫無特別優先族群。"
    risk_lines = "\n".join([f"- {item}" for item in brief["risk_flags"]]) or "- 暫無額外風險提示。"
    source_lines = "\n".join([_render_source_line(item) for item in brief["sources"]])

    return f"""# Taiwan Stock Radar v{brief['version']} 台股日盤 08:30 預測報告

- 日期：{brief['analysis_date']}
- 產生時間：{brief['generated_at_local']}
- 發佈時點：{brief['scheduled_time_local']}
- 模式：夜盤趨勢 + Yahoo奇摩股市 + Anue 鉅亨網 + 美國美股趨勢

## 當日一句話

**{brief['overall_label']}**  
{brief['overall_summary']}

## 開市前市場訊號

- 開盤偏向：**{brief['opening_bias']}**（{brief['opening_score']}/100）
- 新聞流向分數：**{brief['headline_score']}/100**
- 綜合評估分數：**{brief['overall_score']}/100**
- 夜盤與美股摘要：{brief['premarket_brief']['expected_opening_plan']}

## 10 大重點股市訊息

{messages}

## 今日台股趨勢綜合評估

- 綜合結論：**{brief['overall_label']}**
- 盤勢摘要：{brief['overall_summary']}
- 早盤觀察：{brief['premarket_brief']['expected_opening_plan']}

### 族群觀察

{sector_lines}

### 風險提示

{risk_lines}

## 資料來源與可用性

{source_lines}

## 免責聲明

{brief['disclaimer']}
"""
