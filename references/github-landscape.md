# GitHub Landscape For This Skill

Snapshot date: 2026-03-13 (Asia/Taipei)

Purpose: identify the strongest recurring open-source patterns in quant research, backtesting, trading, and finance tooling, then adapt them for a Taiwan-stock AI skill.

Method:

- Queried GitHub repositories by `topic:quantitative-finance`, `topic:algorithmic-trading`, and `topic:backtesting`
- Sorted by stars
- Deduplicated results
- Kept the top 20 unique repos by star count

Note: not all repos are stock-only or Taiwan-specific. Several crypto or multi-asset repos are included because their architecture, UX, or research workflow is reusable.

## 1. Top 20 reference repos

| Rank | Repo | Stars | Why it matters |
|---|---|---:|---|
| 1 | OpenBB-finance/OpenBB | 62,890 | Data-platform thinking, multi-surface delivery, AI-agent positioning |
| 2 | freqtrade/freqtrade | 47,584 | Config-first workflow, dry-run discipline, bot lifecycle, strong docs |
| 3 | microsoft/qlib | 38,651 | AI-oriented quant platform, full ML pipeline, research-to-production framing |
| 4 | wilsonfreitas/awesome-quant | 24,803 | Ecosystem map and coverage benchmark |
| 5 | mementum/backtrader | 20,708 | Backtesting baseline and strategy API expectations |
| 6 | quantopian/zipline | 19,503 | Event-driven backtesting and institutional-style research framing |
| 7 | hummingbot/hummingbot | 17,673 | Execution-aware framework design and operational UX |
| 8 | UFund-Me/Qbot | 16,517 | AI-quant framing and local deployment emphasis |
| 9 | bbfamily/abu | 16,444 | Chinese-language quant workflow and strategy system packaging |
| 10 | AI4Finance-Foundation/FinRL | 14,171 | ML / RL extension path for future versions |
| 11 | myhhub/stock | 11,861 | Stock-oriented feature breadth and screening mindset |
| 12 | TA-Lib/ta-lib-python | 11,778 | Indicator standardization layer |
| 13 | je-suis-tm/quant-trading | 9,385 | Strategy example coverage and educational patterns |
| 14 | StockSharp/StockSharp | 9,253 | Large modular trading platform reference |
| 15 | firmai/financial-machine-learning | 8,446 | Finance ML reference catalog |
| 16 | kernc/backtesting.py | 8,035 | Minimal developer-friendly backtest API and visual outputs |
| 17 | jesse-ai/jesse | 7,532 | Strategy engine and operator experience |
| 18 | paperswithbacktest/awesome-systematic-trading | 7,290 | Research and resource aggregation |
| 19 | polakowo/vectorbt | 6,850 | Fast vectorized research and parameter sweep patterns |
| 20 | lballabio/QuantLib | 6,842 | Finance library depth and long-term extensibility |

## 2. Taiwan-specific ecosystem notes

These repos are smaller but relevant:

| Repo | Stars | Relevance |
|---|---:|---|
| mlouielu/twstock | 1,305 | TWSE / TPEX data access, CLI examples, Taiwan-oriented usage |
| FinMind/FinMindBook | 46 | FinMind ecosystem pointer |
| chunkai1312/node-twstock | 8 | Node client for Taiwan stock scraping |

Important takeaway: Taiwan-specific open-source projects are much smaller than global quant frameworks. That means this skill should borrow architecture quality from large global repos while keeping its market logic Taiwan-native.

## 3. Patterns worth copying

### Pattern A: Connect once, consume everywhere

Seen strongly in:
- OpenBB

Adaptation for this skill:
- one normalized Taiwan-market schema
- reusable outputs for CLI, reports, dashboard, and agent prompts

### Pattern B: Research pipeline end-to-end

Seen strongly in:
- Qlib
- Zipline
- Backtrader

Adaptation:
- data -> features -> factors -> scoring -> signals -> backtest -> report

### Pattern C: Strong operator workflow

Seen strongly in:
- freqtrade
- jesse
- hummingbot

Adaptation:
- config files for weights and universe
- dry-run and daily scan before any stronger action language
- explicit risk flags and operating assumptions

### Pattern D: Fast experimentation

Seen strongly in:
- vectorbt
- backtesting.py

Adaptation:
- simple strategy API
- quick scoring tests
- parameter sweeps for feature thresholds
- visual summaries and compact metrics tables

### Pattern E: Factor validation, not just factor invention

Seen strongly in:
- Alphalens
- quantstats

Adaptation:
- tear-sheet-like factor review
- trade metrics
- drawdown and turnover visibility

### Pattern F: Documentation as product

Seen strongly in:
- OpenBB
- freqtrade
- backtesting.py
- twstock

Adaptation:
- keep examples short and executable
- include CLI or prompt-level examples
- make skill usage obvious in the landing page

## 4. Recommendations for this repo

### Should be added immediately

- `SKILL.md` with explicit Taiwan-stock reasoning workflow
- focused reference files instead of one giant architecture note
- config-driven scoring weights and universe selection
- example watchlist outputs

### Should be added next

- sample daily scan script
- backtest skeleton
- dashboard mock or screenshot
- a factor tear-sheet style report page

### Should not be copied blindly

- exchange-specific live-trading complexity from crypto bots
- RL-heavy workflows before the baseline rule engine is stable
- portfolio optimization before single-name scoring and backtest hygiene are reliable

## 5. Key design conclusion

The strongest open-source projects share three traits:

1. They make the data and workflow explicit.
2. They show results visually and repeatedly.
3. They let users inspect the reasoning, not just the conclusion.

This skill should do the same for Taiwan stocks:

- explicit data freshness
- explicit factor stack
- explicit risk
- explicit scenario framing

That combination is more valuable than a vague "AI predicts stocks" claim.
