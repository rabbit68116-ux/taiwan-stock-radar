# Taiwan Stock Radar

[![GitHub repo](https://img.shields.io/badge/GitHub-rabbit68116--ux%2Ftaiwan--stock--radar-181717?logo=github)](https://github.com/rabbit68116-ux/taiwan-stock-radar)
![Status](https://img.shields.io/badge/status-architecture%20v1.0-blue)
![Skill](https://img.shields.io/badge/skill-v1.4-orange)
![Market](https://img.shields.io/badge/market-Taiwan%20Stocks-red)
![Mode](https://img.shields.io/badge/mode-single--stock%20indicator%20committee-green)

Taiwan Stock Radar v1.4 是一個面向台灣股票單股研判的研究型 AI skill。
這一版把重心從「策略模組」再往前推一層，正式建立成 **台股指標作業系統**，讓 AI agent 能依照不同交易風格，系統化讀取趨勢、動能、量價、籌碼、基本面與事件面訊號，再產出可執行的判斷。

> 一檔股票。八位 specialist AI analysts。六層台股訊號引擎。三種交易風格權重。
> One stock. Eight specialist AI analysts. Six Taiwan-market signal engines. Three trading-style profiles.

[官方網站 Official Website](https://rabbit68116-ux.github.io/taiwan-stock-radar/) | [案例頁 Featured Case Study](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html) | [GitHub Repo](https://github.com/rabbit68116-ux/taiwan-stock-radar)

---

## 繁體中文

### 封面定位

**Taiwan Stock Radar** 是一個專注於台灣股票單股深度研判的 AI skill。
它不是只做市場掃描的 watchlist 工具，也不是只輸出一句方向判斷的聊天式助理，而是把一檔股票交給多位不同專長、不同性格、不同權重的 AI analyst 分身，模擬一場正式的投資研究會議。

`v1.4` 的重心是 **台股指標與風格加強版本**：

- 不只問「這檔股票偏多還是偏空」
- 也不只問「最適合哪一種交易策略」
- 而是先回答「這檔股票目前的訊號堆疊是否健康」
- 再依短線、波段、中長線三種風格切換權重
- 最後才輸出策略、買賣點與風險條件

### v1.4 升級重點

- 建立 `6` 層台股訊號引擎：`Trend`、`Momentum`、`Price-Volume`、`Chip Flow`、`Fundamentals`、`Events`
- 新增 [`config/indicator_catalog.yaml`](./config/indicator_catalog.yaml)，把均線、MACD、RSI、KD、布林通道、法人、融資融券、借券、月營收、EPS、PE、殖利率、事件日期等欄位正式收編
- 新增 [`config/style_weights.yaml`](./config/style_weights.yaml)，定義 `short_term`、`swing`、`position` 三種風格的權重切換
- 把「最小可用欄位集合」寫成正式規格，讓 AI agent 至少能用 12 個核心欄位做出穩定的初判
- 將台股最實戰的判讀語言正式化，例如 `60MA 之上找買點、回檔量縮、投信連買、月營收轉強、事件窗口降權`

### 展品摘要 Exhibit Snapshot

| 項目 | 說明 |
|---|---|
| 產品模式 Product mode | `v1.4` indicator-driven single-stock committee |
| 主要市場 Coverage | `TWSE / TPEX` 單股深度研判 |
| Agent 數量 Agent count | `8` 位 specialist personas |
| 訊號引擎 Signal engines | `6` 層台股訊號堆疊 |
| 交易風格 Style profiles | `short_term / swing / position` |
| 最終交付 Final deliverable | 風格化判斷、策略建議、買入區、停損區、停利區、失效條件 |
| 公開展示 Public surface | GitHub repo + GitHub Pages product site |

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

### 最小可用欄位 Minimum Viable Field Set

如果系統只允許先做最小版本，`v1.4` 建議先放這 `12` 個欄位：

- 收盤價
- `20MA`
- `60MA`
- `20MA` 斜率
- 成交量
- `20日均量`
- 是否放量突破
- `MACD`
- `RSI(14)`
- 外資買賣超
- 投信買賣超
- 月營收 `YoY`

這組欄位足以支撐一個台股單股 AI agent 做出 80% 以上的基礎判斷。

### 最實用的組合模板

#### 組合 1：趨勢突破

- `20MA` 上彎
- 股價站上 `60MA`
- 放量突破前高
- `MACD` 翻正
- 外資或投信同步買超

#### 組合 2：回檔承接

- 多頭排列
- 回測 `20MA` 或 `60MA`
- 回檔量縮
- `KD` 低檔黃金交叉
- 法人沒有明顯轉賣

#### 組合 3：價值 + 技術

- 本益比合理
- 殖利率不差
- 月營收 `YoY` 轉強
- 股價重新站回 `60MA`
- 量能開始放大

### AI Agent 研討會

在 `v1.4` 中，單一股票會進入一個以指標引擎為核心的 multi-agent committee。每位 agent 有不同性格、專業、指標權重與責任。

| AI Agent | 角色定位 | 核心觀察 | 權重 |
|---|---|---|---:|
| Chief Strategist | 主持研究會議，整合最終結論 | 市場背景、衝突裁決、資本配置語言 | 0.18 |
| Technical Strategist | 技術面與結構分析 | 均線、趨勢、`MACD`、`RSI`、`KD`、布林通道 | 0.16 |
| Chip Flow Analyst | 籌碼與資金流向分析 | 外資、投信、融資、融券、借券、連買連賣 | 0.14 |
| Fundamental Analyst | 基本面與品質分析 | 月營收、`EPS`、`ROE`、毛利率、估值與股利 | 0.14 |
| Catalyst Analyst | 事件與催化因子分析 | 法說、財報、營收、除權息、重大訊息、產業事件 | 0.10 |
| Risk Manager | 反方與風控代表 | 流動性、跳空風險、事件聚集、失效條件 | 0.11 |
| Strategy Architect | 策略模組選擇與風格切換 | setup 類型、style fit、策略衝突 | 0.09 |
| Quant Validation Analyst | 驗證與穩健度檢查 | 回測品質、尾部風險、參數穩定性、成本敏感度 | 0.08 |

### 單股研討會輸出範例

```text
Taiwan Stock Radar v1.4
Illustrative Single-Stock Indicator Committee Output
Case: 2330 台積電
Analysis Date: 2026-03-13
Style: Swing

Signal Engine Summary
- Trend: constructive above 20MA and 60MA
- Momentum: MACD positive, RSI strong but not exhausted
- Price-Volume: breakout valid only if volume expansion persists
- Chip Flow: foreign / trust alignment still supportive
- Fundamentals: monthly revenue and quality metrics remain constructive
- Events: maintain caution around earnings and revenue windows

Style Weighting
- Swing profile active
- Trend / Price-Volume / Chip Flow / Fundamentals prioritized
- KD and short-term noise de-emphasized

Committee Thesis
- Base view remains constructive while structure, flow, and event order remain intact.

Action Plan
- Preferred buy zone: pullback into support while volume contracts
- Aggressive trigger: reclaim with volume
- Conservative trigger: confirmation above resistance with peer leadership intact
- Stop loss: structure break below support
- Invalidation: downgrade if 60MA fails, flow deteriorates, and event risk worsens together
```

### v1.4 新增的正式規格

| 路徑 | 作用 |
|---|---|
| [`config/indicator_catalog.yaml`](./config/indicator_catalog.yaml) | 台股核心技術、籌碼、基本面、事件欄位清單與用法 |
| [`config/style_weights.yaml`](./config/style_weights.yaml) | 短線 / 波段 / 中長線三種風格的權重切換 |
| [`references/taiwan-indicator-framework-v1.4.md`](./references/taiwan-indicator-framework-v1.4.md) | `v1.4` 指標白皮書，整理各欄位的台股實戰意義 |

### 專案內容 Repo Contents

| 路徑 | 作用 |
|---|---|
| [`SKILL.md`](./SKILL.md) | `v1.4` 核心 skill 定義，說明指標引擎版單股分析流程 |
| [`references/agent-analyst-blueprint.md`](./references/agent-analyst-blueprint.md) | 多 agent 研討會與風格化輸出藍圖 |
| [`references/taiwan-indicator-framework-v1.4.md`](./references/taiwan-indicator-framework-v1.4.md) | `v1.4` 指標白皮書與台股實戰判讀框架 |
| [`config/indicator_catalog.yaml`](./config/indicator_catalog.yaml) | 核心欄位、指標、來源與使用規則 |
| [`config/style_weights.yaml`](./config/style_weights.yaml) | 交易風格權重設定 |
| [`config/strategy_modules.yaml`](./config/strategy_modules.yaml) | 策略模組、適用 regime、確認條件與禁用條件 |
| [`config/evaluation_metrics.yaml`](./config/evaluation_metrics.yaml) | 績效、尾部風險、執行品質與穩健度評估集合 |
| [`docs/index.html`](./docs/index.html) | 公開產品首頁 |
| [`docs/case-study.html`](./docs/case-study.html) | 單股完整展示頁 |

### 公開入口 Public Links

- GitHub Repo: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
- Public Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- Case Study: [https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

### 快速開始 Quick Start

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_daily_scan.py
streamlit run app/streamlit_app.py
```

目前的 scan 與 dashboard 仍保留為展示型資產。  
`v1.4` 的核心價值則集中在 skill、blueprint、indicator catalog、style weights、case study 與公開展示頁。

---

## English

### Cover Statement

**Taiwan Stock Radar v1.4** is a Taiwan-equity research skill built around one stock at a time. This release formalizes the product into a Taiwan-stock indicator operating system, so AI agents can read trend, momentum, price-volume, chip flow, fundamentals, and event risk through style-specific weighting.

### What Changed in v1.4

- six Taiwan-market signal engines now structure the single-stock workflow
- a formal indicator catalog was added for technical, flow, fundamental, and event fields
- style-weight profiles were added for `short_term`, `swing`, and `position`
- the system now treats signal quality as the first gate before strategy and action planning
- the repo now includes a whitepaper-style indicator framework for Taiwan equities

### What the Product Returns

- a weighted committee thesis
- signal-engine health across trend, momentum, price-volume, flow, fundamentals, and events
- style-specific interpretation for short-term, swing, and position trading
- strategy-family selection and execution-aware action zones
- buy zone, stop-loss, take-profit ladder, and invalidation

### Public Surfaces

- Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- Case Study: [https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)
- GitHub: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
