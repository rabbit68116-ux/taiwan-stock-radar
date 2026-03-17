# Taiwan Stock Radar

[![GitHub repo](https://img.shields.io/badge/GitHub-rabbit68116--ux%2Ftaiwan--stock--radar-181717?logo=github)](https://github.com/rabbit68116-ux/taiwan-stock-radar)
![Status](https://img.shields.io/badge/status-architecture%20v1.0-blue)
![Skill](https://img.shields.io/badge/skill-v1.6-orange)
![Market](https://img.shields.io/badge/market-Taiwan%20Stocks-red)
![Mode](https://img.shields.io/badge/mode-08%3A30%20daily%20brief%20%2B%20single--stock%20committee-green)

Taiwan Stock Radar v1.6 是一個專為台灣股票研究打造的 AI skill。
這一版把產品主輸出正式升級為 **每日早上 08:30 的台股日盤預測報告**：先整合夜盤趨勢、Yahoo奇摩股市、Anue 鉅亨網與美股趨勢，整理 10 大重點股市訊息，再輸出當日台股趨勢綜合評估；若使用者指定個股，系統再進一步展開單股研究委員會。

> 每日 08:30 台股日盤預測報告。10 大重點股市訊息。夜盤趨勢 + Yahoo奇摩股市 + Anue 鉅亨網 + 美國美股趨勢。必要時再進入單股深度研判。
> Daily 08:30 Taiwan market brief. Ten key market signals. Night-session trend plus Yahoo Taiwan market pages, Anue headlines, and US-market direction. Then a single-stock deep dive when needed.

[官方網站 Official Website](https://rabbit68116-ux.github.io/taiwan-stock-radar/) | [案例頁 Featured Case Study](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html) | [GitHub Repo](https://github.com/rabbit68116-ux/taiwan-stock-radar)

---

## 繁體中文

### 產品定位

**Taiwan Stock Radar** 不是單純的開盤前新聞整理頁，也不是只回答一句看多看空的聊天工具。
它是一套面向台股日盤的研究工作流，先在 **08:30** 以前把隔夜訊號、關鍵新聞與美股方向濃縮成一份簡潔報告，再決定今天台股該如何看盤、哪些族群值得先觀察、哪些風險要先避開。

`v1.6` 的主輸出是：

- 一份 **台股日盤 08:30 預測報告**
- 一組 **10 大重點股市訊息**
- 一段 **當日台股趨勢綜合評估**
- 若需要，再延伸到 **單股研究委員會**、策略建議與買賣點

### v1.6 升級重點

- 新增 **每日早上 08:30 台股日盤預測報告**
- 新增 [`scripts/run_daily_market_brief.py`](./scripts/run_daily_market_brief.py)，直接抓取夜盤、Yahoo奇摩股市、Anue 鉅亨網與美股趨勢後輸出報告
- 新增 [`src/taiwan_stock_radar/daily_market_brief.py`](./src/taiwan_stock_radar/daily_market_brief.py)，把台指期近月、S&P 500、Nasdaq、Dow、SOX、TSM ADR、NVIDIA、VIX 與 10 則重點訊息整合成日盤簡報
- 新增 [`config/daily_market_brief_rules.yaml`](./config/daily_market_brief_rules.yaml)，正式定義 `08:30` 發佈時間、訊息配比、來源網址與綜合評分權重
- 承接既有開市前環境判讀與單股委員會層，讓日盤簡報能直接延伸到單股深度判斷

### 展品摘要 Exhibit Snapshot

| 項目 | 說明 |
|---|---|
| 產品模式 Product mode | `v1.6` daily 08:30 market brief + single-stock committee |
| 發佈時點 Schedule | 每日 `08:30` |
| 核心來源 Core sources | 夜盤趨勢、Yahoo奇摩股市、Anue 鉅亨網、美股趨勢 |
| 重點輸出 Key deliverables | 10 大重點股市訊息、台股趨勢綜合評估、族群觀察、風險提示 |
| Agent 模型 Agent model | `8` 位加權專家角色，供單股 deep-dive 使用 |
| 公開展示 Public surface | GitHub repo + GitHub Pages product site |

### 產品工作流 Product Workflow

#### 1. 日盤簡報層 Daily 08:30 Brief Layer

系統會在台股日盤前完成以下工作：

- 讀取 **台指期近月 / 夜盤趨勢**
- 讀取 **Yahoo奇摩股市** 的台股與美股頁面
- 讀取 **Anue 鉅亨網** 的台股與美股新聞頁
- 讀取 **美股大盤與半導體領先訊號**
- 整理成 **10 大重點股市訊息**
- 輸出 **當日台股趨勢綜合評估**

#### 2. 單股委員會層 Single-Stock Committee

如果使用者指定個股，系統會在日盤簡報後展開正式單股研究流程：

- 六層台股訊號引擎先校準證據
- 八位專家級 AI 分析師分別形成獨立觀點
- 依 `short_term / swing / position` 切換風格權重
- 由 Strategy Architect 提名最適合的策略家族
- 由 Quant Validation Analyst 做穩健度與風險檢查
- 最後整合成具體的買入區、停損區、停利階梯與失效條件

### 每日 08:30 日盤報告包含什麼

| 區塊 | 內容 |
|---|---|
| 夜盤趨勢 | 台指期近月漲跌、成交量與早盤基調 |
| 美股大盤 | `S&P 500 / Nasdaq / Dow` 當晚方向 |
| 半導體領先 | `SOX / TSM ADR / NVIDIA` 是否持續帶頭 |
| 風險情緒 | `VIX` 升降與避險需求變化 |
| 10 大重點訊息 | 依來源配比整理的市場重點 |
| 綜合評估 | 當日台股偏多、偏弱、偏震盪或建設性偏強 |
| 族群觀察 | 半導體、AI、金融、防禦型族群 |
| 風險提示 | 外盤分歧、夜盤缺口、追價風險與消息不確定性 |

### 六層台股訊號引擎 Signal Engines

| 引擎 | 核心用途 | 代表欄位 |
|---|---|---|
| 趨勢引擎 Trend | 定義個股目前是多頭、整理還是轉弱 | `5/10/20/60/120/240MA`、是否站上 `20MA/60MA`、均線斜率、`52W high/low distance` |
| 動能引擎 Momentum | 判斷短中線強弱、過熱與轉折節奏 | `MACD`、`RSI(14)`、`KD(9,3,3)`、近 `5/20` 日報酬、布林通道位置 |
| 量價引擎 Price-Volume | 避免假突破與無量反彈 | 當日量、`5/20` 日均量、量比、放量突破、回檔縮量、價漲量增 / 價跌量增 |
| 籌碼引擎 Chip Flow | 補足台股特有的法人與部位結構 | 外資、投信、自營商、融資融券、借券賣出、連買 / 連賣天數 |
| 基本面引擎 Fundamentals | 確認價格背後是否有商業品質與估值支持 | 月營收 `MoM / YoY`、`EPS`、`ROE`、毛利率、營益率、`PE`、殖利率、`PB` |
| 事件引擎 Events | 管理法說、財報、月營收、除權息與重大訊息風險 | 法說日期、財報日期、月營收公布日、除權息日期、重大訊息、產業題材、ADR 連動 |

### 三種交易風格 Style Profiles

| 風格 | 優先訊號 | 核心判斷 |
|---|---|---|
| 短線 `short_term` | `5/10/20MA`、成交量、`KD`、`RSI`、短期法人買賣超 | 追蹤節奏與轉折，重視量價與短期動能 |
| 波段 `swing` | `20/60/120MA`、`MACD`、量價突破、投信 / 外資趨勢、月營收與財報 | 找健康趨勢中的突破與回檔承接 |
| 中長線 `position` | 殖利率、配息穩定性、`PE`、`ROE`、現金流、產業趨勢、大盤位置 | 更重基本面、事件紀律與長線方向 |

### 08:30 日盤預測報告輸出範例

```text
Taiwan Stock Radar v1.6 台股日盤 08:30 預測報告
Analysis Date: 2026-03-17
Scheduled Time: 08:30

Overall Assessment
- 偏多開盤且延續機率較高 (82.3 / 100)

Market Signals
- 台指期近一 +1.49%
- S&P 500 +1.01% / Nasdaq +1.22% / Dow +0.83%
- SOX +1.96% / TSM ADR +0.57% / NVDA +1.65%
- VIX -13.53%

Top Messages
1. Yahoo奇摩股市 / 台股盤勢
2. Yahoo奇摩股市 / 台股盤勢
3. Yahoo奇摩股市 / 台股盤勢
4. Anue 鉅亨網 / 鉅亨台股
5. Anue 鉅亨網 / 鉅亨台股
6. Anue 鉅亨網 / 鉅亨美股

Conclusion
- 夜盤、美股與半導體訊號大致同向，台股今天較有機會由電子權值與 AI 供應鏈領漲。
```

### 專案內容 Repo Contents

| 路徑 | 作用 |
|---|---|
| [`SKILL.md`](./SKILL.md) | `v1.6` 核心 skill 定義，說明 08:30 日盤簡報與單股委員會流程 |
| [`references/daily-market-brief-framework-v1.6.md`](./references/daily-market-brief-framework-v1.6.md) | `v1.6` 日盤 08:30 報告方法，定義來源、配比、權重與容錯 |
| [`references/taiwan-indicator-framework-v1.6.md`](./references/taiwan-indicator-framework-v1.6.md) | `v1.6` 台股指標白皮書，整理六層訊號引擎與風格切換 |
| [`references/agent-analyst-blueprint.md`](./references/agent-analyst-blueprint.md) | 多 agent 研討會與加權輸出藍圖 |
| [`config/daily_market_brief_rules.yaml`](./config/daily_market_brief_rules.yaml) | 08:30 報告來源、訊息配比與權重設定 |
| [`config/premarket_rules.yaml`](./config/premarket_rules.yaml) | 夜盤 / 美股趨勢評估權重 |
| [`scripts/run_daily_market_brief.py`](./scripts/run_daily_market_brief.py) | 產出台股日盤 08:30 預測報告 |
| [`scripts/run_premarket_brief.py`](./scripts/run_premarket_brief.py) | 產出基礎開市前環境報告 |
| [`src/taiwan_stock_radar/daily_market_brief.py`](./src/taiwan_stock_radar/daily_market_brief.py) | Live data 擷取、10 則訊息整理與綜合評估 |
| [`docs/index.html`](./docs/index.html) | 公開產品首頁 |
| [`docs/case-study.html`](./docs/case-study.html) | 單股完整展示頁 |

### 快速開始 Quick Start

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_daily_market_brief.py --date 2026-03-17
python3 scripts/run_premarket_brief.py --date 2026-03-17
python3 scripts/run_daily_scan.py
streamlit run app/streamlit_app.py
```

`v1.6` 新增的日盤報告預設會輸出到 [`output/`](./output)：

- `daily_market_brief.json`
- `daily_market_brief.md`

### 公開入口 Public Links

- GitHub Repo: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
- Public Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- Case Study: [https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

### 免責聲明 Disclaimer

Taiwan Stock Radar 僅供研究、教育與產品展示使用，不構成任何形式的投資建議、招攬、保證報酬或個別證券推薦。
專案中的日盤預測報告、夜盤評估、情境推演、買入區、停損區、停利階梯與失效條件，皆屬方法展示，不應被視為對未來市場走勢或個股表現的確定承諾。
任何交易決策、資金配置與風險承擔，仍應由使用者自行判斷與負責。

---

## English

### Cover Statement

**Taiwan Stock Radar v1.6** turns the product into a daily 08:30 Taiwan market brief. It combines Taiwan night-session, Yahoo Taiwan market pages, Anue headlines, and US-market direction into ten key market messages and a concise daily outlook, then expands into a single-stock committee when needed.

### What Changed in v1.6

- a new daily 08:30 Taiwan market brief is now the primary product output
- the brief blends night-session trend, Yahoo Taiwan pages, Anue headlines, and US-market signals
- `scripts/run_daily_market_brief.py` and `src/taiwan_stock_radar/daily_market_brief.py` formalize the live workflow
- the single-stock committee remains available as the second layer for deeper analysis

### What the Product Returns

- a daily Taiwan market brief at 08:30
- ten key market signals and headlines
- an opening-bias and full-session assessment
- sector watchlists and risk flags
- a single-stock deep dive when requested

### Disclaimer

Taiwan Stock Radar is provided for research, education, and product demonstration. It is not investment advice, not a solicitation, and not a guarantee of future returns. Any daily market brief, case study, scenario, action zone, stop, target, or invalidation rule in this project is illustrative and should not be treated as a certain commitment about future market behavior.
