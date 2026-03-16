# Taiwan Stock Radar

[![GitHub repo](https://img.shields.io/badge/GitHub-rabbit68116--ux%2Ftaiwan--stock--radar-181717?logo=github)](https://github.com/rabbit68116-ux/taiwan-stock-radar)
![Status](https://img.shields.io/badge/status-architecture%20v1.0-blue)
![Skill](https://img.shields.io/badge/skill-v1.5-orange)
![Market](https://img.shields.io/badge/market-Taiwan%20Stocks-red)
![Mode](https://img.shields.io/badge/mode-premarket%20brief%20%2B%20single--stock%20committee-green)

Taiwan Stock Radar v1.5 是一個專為台灣股票研究打造的 AI skill。
這一版把產品正式分成兩層：先在開市前讀取台股夜盤與美股趨勢，形成隔日開盤評估；再把指定股票送進八位專家級 AI 分析師組成的單股研究委員會，輸出可執行的策略與買賣點。

> 一份開市前環境報告。一檔股票。八位專家級 AI 分析師。六層台股訊號引擎。三種交易風格權重。
> One premarket environment brief. One stock. Eight specialist AI analysts. Six Taiwan-stock signal engines. Three trading-style profiles.

[官方網站 Official Website](https://rabbit68116-ux.github.io/taiwan-stock-radar/) | [案例頁 Featured Case Study](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html) | [GitHub Repo](https://github.com/rabbit68116-ux/taiwan-stock-radar)

---

## 繁體中文

### 產品定位

**Taiwan Stock Radar** 的定位不是聊天室式喊單，也不是只排出排行榜的市場摘要工具。
它是一套面向台股的研究工作流，先回答「明天台股可能怎麼開」，再回答「這一檔股票在這樣的環境下應該如何理解、如何執行、什麼情況不該碰」。

`v1.5` 的核心價值是把兩件原本容易分散的工作整合成同一個 skill：

- 開市前環境判讀：台股夜盤、美股三大指數、半導體領先訊號、VIX 與風險情緒
- 單股深度研究：六層訊號引擎、八位專家 agent、交易風格權重、策略模組、買賣點與失效條件

### v1.5 升級重點

- 新增 **開市前趨勢報告**，可在台股開市前整合台股夜盤與美股趨勢，輸出隔日開盤偏向與風險提示
- 新增 [`config/premarket_rules.yaml`](./config/premarket_rules.yaml)，把夜盤、美股、半導體與風險權重正式配置化
- 新增 [`scripts/run_premarket_brief.py`](./scripts/run_premarket_brief.py)，可直接產出 `JSON + Markdown` 的開市前報告
- 新增 [`src/taiwan_stock_radar/premarket_brief.py`](./src/taiwan_stock_radar/premarket_brief.py)，把台指夜盤、S&P 500、Nasdaq、SOX、TSM ADR、NVIDIA、VIX 轉成加權分數
- 新增 [`references/premarket-brief-framework-v1.5.md`](./references/premarket-brief-framework-v1.5.md)，說明開市前報告的評估框架、欄位定義與使用限制
- 保留原本的單股委員會核心，並把開市前環境層接到單股決策前面，讓買賣點不脫離隔夜市況

### 展品摘要 Exhibit Snapshot

| 項目 | 說明 |
|---|---|
| 產品模式 Product mode | `v1.5` premarket brief + single-stock committee |
| 市場 Coverage | `TWSE / TPEX` 與台股開市前環境評估 |
| Agent 數量 Agent count | `8` 位加權專家角色 |
| 訊號引擎 Signal engines | `6` 層台股單股訊號 + `1` 層開市前環境層 |
| 交易風格 Style profiles | `short_term / swing / position` |
| 主要輸出 Final deliverables | 開市前趨勢報告、單股決策文件、買入區、停損區、停利階梯、失效條件 |
| 公開展示 Public surface | GitHub repo + GitHub Pages product site |

### 產品工作流 Product Workflow

#### 1. 開市前環境層 Premarket Layer

系統先在台股開市前建立一份環境報告，核心問題是：

- 台股可能偏多開、偏弱開，還是開盤後震盪分化
- 半導體與大型電子是否有機會接棒
- 夜盤與美股訊號是否一致，還是出現衝突
- 哪些外部風險可能讓夜盤與美股方向在開盤後失效

這一層目前整合：

- 台指期夜盤變動與量比
- `S&P 500 / Nasdaq / Dow`
- `SOX / TSM ADR / NVIDIA`
- `VIX`
- 夜盤與外盤對台股族群的領先訊號

#### 2. 單股委員會層 Single-Stock Committee

完成開市前環境判讀後，指定股票會進入正式單股研究流程：

- 六層台股訊號引擎先校準證據
- 八位專家級 AI 分析師分別形成獨立觀點
- 依 `short_term / swing / position` 切換風格權重
- 由 Strategy Architect 提名最適合的策略家族
- 由 Quant Validation Analyst 做穩健度與風險檢查
- 最後整合成具體的買入區、停損區、停利階梯與失效條件

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

### 八位 AI 分析師 Eight Specialist AI Analysts

| AI Agent | 角色定位 | 核心觀察 | 權重 |
|---|---|---|---:|
| Chief Strategist | 主持研究會議，整合最終結論 | 市場背景、衝突裁決、資本配置語言 | 0.18 |
| Technical Strategist | 技術面與結構分析 | 均線、趨勢、`MACD`、`RSI`、`KD`、布林通道 | 0.16 |
| Chip Flow Analyst | 籌碼與資金流向分析 | 外資、投信、融資、融券、借券、連買連賣 | 0.14 |
| Fundamental Analyst | 基本面與品質分析 | 月營收、`EPS`、`ROE`、毛利率、估值與股利 | 0.14 |
| Catalyst Analyst | 事件與催化因子分析 | 法說、財報、營收、除權息、重大訊息、產業事件 | 0.10 |
| Risk Manager | 反方與風控代表 | 流動性、跳空風險、事件聚集、失效條件 | 0.11 |
| Strategy Architect | 策略模組選擇與風格切換 | 個案類型、風格適配、策略衝突 | 0.09 |
| Quant Validation Analyst | 驗證與穩健度檢查 | 回測品質、尾部風險、參數穩定性、成本敏感度 | 0.08 |

### 開市前趨勢報告輸出範例

```text
Taiwan Stock Radar v1.5 開市前趨勢報告
Analysis Date: 2026-03-17
Profile: 半導體領漲的風險偏好盤

Opening Bias
- 偏多開盤 (91.8 / 100)

Key Drivers
- 台指期夜盤 +0.86% ，量比 1.34
- Nasdaq +1.12% / SOX +2.08%
- VIX -5.30% ，風險分數 1.00

Sector Watchlist
- 半導體：優先觀察
- AI 伺服器 / 高速運算：偏多觀察
- 金融股：中性偏穩

Expected Opening Plan
- 預估台股偏高開，早盤若量價延續，電子權值與 AI 鏈有望主導。
```

### 單股研討會輸出範例

```text
Taiwan Stock Radar v1.5
Illustrative Single-Stock Committee Output
Case: 2330 台積電
Analysis Date: 2026-03-17
Style: Swing

Premarket Context
- 夜盤與 Nasdaq / SOX 同步偏強
- 風險情緒穩定，電子權值具接棒條件

Signal Engine Summary
- Trend: constructive above 20MA and 60MA
- Momentum: MACD positive, RSI firm but not exhausted
- Price-Volume: breakout quality depends on volume persistence
- Chip Flow: foreign / trust alignment remains supportive
- Fundamentals: revenue and quality metrics stay constructive
- Events: maintain discipline around earnings and revenue windows

Action Plan
- Preferred buy zone: pullback into support while volume contracts
- Aggressive trigger: reclaim with volume after opening confirmation
- Conservative trigger: confirmation above resistance with peer leadership intact
- Stop loss: structure break below support
- Invalidation: downgrade if 60MA fails, flow deteriorates, and event risk worsens together
```

### 專案內容 Repo Contents

| 路徑 | 作用 |
|---|---|
| [`SKILL.md`](./SKILL.md) | `v1.5` 核心 skill 定義，說明開市前環境層與單股委員會流程 |
| [`references/agent-analyst-blueprint.md`](./references/agent-analyst-blueprint.md) | 多 agent 研討會與加權輸出藍圖 |
| [`references/taiwan-indicator-framework-v1.5.md`](./references/taiwan-indicator-framework-v1.5.md) | 台股指標白皮書與實戰判讀框架 |
| [`references/premarket-brief-framework-v1.5.md`](./references/premarket-brief-framework-v1.5.md) | 開市前報告方法與欄位說明 |
| [`config/indicator_catalog.yaml`](./config/indicator_catalog.yaml) | 核心欄位、指標、來源與使用規則 |
| [`config/style_weights.yaml`](./config/style_weights.yaml) | 交易風格權重設定 |
| [`config/strategy_modules.yaml`](./config/strategy_modules.yaml) | 策略模組、適用 regime、確認條件與禁用條件 |
| [`config/evaluation_metrics.yaml`](./config/evaluation_metrics.yaml) | 績效、尾部風險、執行品質與穩健度評估集合 |
| [`config/premarket_rules.yaml`](./config/premarket_rules.yaml) | 開市前夜盤與美股趨勢權重、閾值與輸出設定 |
| [`scripts/run_premarket_brief.py`](./scripts/run_premarket_brief.py) | 產出開市前趨勢報告 |
| [`scripts/run_daily_scan.py`](./scripts/run_daily_scan.py) | 保留的市場掃描展示型腳本 |
| [`docs/index.html`](./docs/index.html) | 公開產品首頁 |
| [`docs/case-study.html`](./docs/case-study.html) | 單股完整展示頁 |

### 快速開始 Quick Start

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_premarket_brief.py --profile semi_risk_on --date 2026-03-17
python3 scripts/run_daily_scan.py
streamlit run app/streamlit_app.py
```

開市前報告預設會輸出到 [`output/`](./output)：

- `premarket_brief.json`
- `premarket_brief.md`

目前 scan、dashboard 與 case study 仍屬展示型資產；`v1.5` 的核心價值則集中在 **開市前環境層 + 單股研究委員會** 這條工作流。

### 公開入口 Public Links

- GitHub Repo: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
- Public Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- Case Study: [https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

### 免責聲明 Disclaimer

Taiwan Stock Radar 僅供研究、教育與產品展示使用，不構成任何形式的投資建議、招攬、保證報酬或個別證券推薦。
專案中的案例、開市前趨勢報告、情境推演、買入區、停損區、停利階梯與失效條件，皆屬方法展示，不應被視為對未來市場走勢或個股表現的確定承諾。
任何交易決策、資金配置與風險承擔，仍應由使用者自行判斷與負責。

---

## English

### Cover Statement

**Taiwan Stock Radar v1.5** is a Taiwan-equity research skill with two connected layers: a premarket environment brief built from Taiwan night-session and US-market signals, followed by a single-stock research committee built around one stock at a time.

### What Changed in v1.5

- a new premarket opening-bias brief now evaluates Taiwan night-session, US broad indices, semiconductor leadership, and VIX risk
- the overnight layer now feeds into the single-stock committee before strategy and action planning
- `config/premarket_rules.yaml`, `scripts/run_premarket_brief.py`, and `references/premarket-brief-framework-v1.5.md` formalize the new workflow
- the existing single-stock engine remains intact with six signal engines, eight specialist analysts, and style-aware weighting

### What the Product Returns

- a premarket Taiwan-opening assessment
- a weighted single-stock committee thesis
- signal-engine health across trend, momentum, price-volume, chip flow, fundamentals, and events
- style-specific interpretation for short-term, swing, and position trading
- buy zone, stop-loss, take-profit ladder, invalidation, and risk flags

### Disclaimer

Taiwan Stock Radar is provided for research, education, and product demonstration. It is not investment advice, not a solicitation, and not a guarantee of future returns. Any premarket brief, case study, scenario, action zone, stop, target, or invalidation rule in this project is illustrative and should not be treated as a certain commitment about future market behavior.
