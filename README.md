# Taiwan Stock Radar

[![GitHub repo](https://img.shields.io/badge/GitHub-rabbit68116--ux%2Ftaiwan--stock--radar-181717?logo=github)](https://github.com/rabbit68116-ux/taiwan-stock-radar)
![Status](https://img.shields.io/badge/status-architecture%20v1.0-blue)
![Skill](https://img.shields.io/badge/skill-v1.2-orange)
![Market](https://img.shields.io/badge/market-Taiwan%20Stocks-red)
![Mode](https://img.shields.io/badge/mode-single--stock%20multi--agent-green)

Taiwan Stock Radar v1.2 is a professional single-stock analysis skill for Taiwan equities. It is designed for AI agents that need to behave less like a generic chatbot and more like a disciplined investment committee.

> One stock. Multiple specialist AI agents. One formal research meeting. One final decision packet with trend scenarios, buy zones, sell zones, and explicit invalidation.

[Official Website](https://rabbit68116-ux.github.io/taiwan-stock-radar/) | [GitHub Repo](https://github.com/rabbit68116-ux/taiwan-stock-radar)

---

## 繁體中文

### 展品定位

**Taiwan Stock Radar** 不是一個只會丟出股票代號的選股頁，也不是一段模糊的市場情緒評論。  
`v1.2` 的核心定位是把單一台股個案，交給多位具不同性格、專長、權重的 AI agent 分身，模擬一場專業股市研討會議，最後輸出可執行的研究結論。

這個 skill 專門處理一件事：

- 針對一檔台股做深入研判
- 讓不同專業 AI analyst 各自提出論點與反對意見
- 將技術面、籌碼面、基本面、事件面與風險管理整合成一份正式決策摘要
- 明確給出趨勢判斷、買入區、停損區、停利區、失效條件與信心等級

### v1.2 核心升級

相較於先前版本，`v1.2` 將主軸明確收斂為 **單股、多 agent、會議式決策**：

- 將市場掃描降為背景展示層，首頁聚焦單股決策能力
- 將單股分析視為一個完整專案，而不是掃描後附帶的一段補充
- 透過多位專業 agent 分工，避免單一視角誤判
- 允許 agent 之間保留歧見，而不是強迫輸出單一路徑
- 最終輸出以「決策文件」為核心，而不是只給一句看多或看空

### 多重 AI Agent 專業研討會

在 `v1.2` 中，單一股票會進入一個多 agent council。每位 agent 有不同的性格、分析責任、使用指標與投票權重。

| AI Agent | 角色定位 | 核心觀察 | 權重 |
|---|---|---|---:|
| Chief Strategist | 主持研究會議，整合全局結論 | 市場背景、結論整合、衝突裁決 | 0.24 |
| Technical Strategist | 技術面與趨勢結構分析 | 多週期趨勢、支撐壓力、量價結構 | 0.18 |
| Chip Flow Analyst | 籌碼與資金流向分析 | 外資、投信、融資、主力結構 | 0.18 |
| Fundamental Analyst | 基本面與品質分析 | 月營收、獲利品質、產品週期、估值敘事 | 0.17 |
| Catalyst Analyst | 事件與催化因子分析 | 法說、營收公告、產業事件、政策節點 | 0.11 |
| Risk Manager | 反方與風控代表 | 流動性、波動、失敗型態、部位風險 | 0.12 |

### 研討會議流程

1. `Case setup`
   確認股票代號、公司名稱、分析日期、時間週期、研究問題與目前已知限制。
2. `Specialist briefs`
   每位 agent 先獨立輸出自己的分析摘要，不先受其他 agent 影響。
3. `Cross-examination`
   由主持 agent 將衝突點攤開，例如技術面強但籌碼轉弱、基本面改善但事件風險逼近。
4. `Weighted verdict`
   依權重計算共識方向，同時保留反方意見與主要風險。
5. `Decision packet`
   輸出專業研究結論，包括趨勢預測、情境機率、買賣點、停損、停利與失效條件。

### 最終輸出長什麼樣

`Taiwan Stock Radar v1.2` 的標準輸出不是一句「看多」或「看空」，而是一份完整的單股決策包：

- `Final thesis`
  這檔股票目前最值得成立的主論點是什麼。
- `Trend forecast`
  以 tactical、swing、position 三種週期區分方向判斷。
- `Scenario tree`
  至少包含 base case、bull case、bear case，並標記觸發條件。
- `Action zones`
  給出理想買入區、積極買點、保守確認買點。
- `Risk controls`
  包含停損區、失效條件、不能追價的條件。
- `Exit plan`
  提供 TP1、TP2、減碼邏輯與失敗退出規則。
- `Consensus and dissent`
  顯示哪些 agent 支持、哪些 agent 保留、爭議點是什麼。

### 為什麼值得追蹤

- 它展示的是 **AI agent 編排能力**，不是單一 prompt 技巧。
- 它專注在 **台灣股票**，而不是用美股邏輯硬套本地市場。
- 它把分析過程做成 **可追蹤、可辯論、可更新** 的研究流程。
- 它讓最終輸出更接近資深分析師的會議摘要，而不是散亂評論。

### Repo 內容

| 路徑 | 作用 |
|---|---|
| [`SKILL.md`](./SKILL.md) | `v1.2` 核心 skill 定義，說明多 agent 單股分析流程 |
| [`references/agent-analyst-blueprint.md`](./references/agent-analyst-blueprint.md) | 多 agent 研討會藍圖與輸出規格 |
| [`references/taiwan-market-playbook.md`](./references/taiwan-market-playbook.md) | 台股市場脈絡、常見因子與台灣特有風險規則 |
| [`references/prediction-framework.md`](./references/prediction-framework.md) | 預測語氣、情境推演、信心表達與失效條件框架 |
| [`config/agent_personas.yaml`](./config/agent_personas.yaml) | 各 agent 的性格、專長、權重與分析責任 |
| [`config/settings.yaml`](./config/settings.yaml) | 專案版本與分析模式設定 |
| [`config/action_rules.yaml`](./config/action_rules.yaml) | 買點、停損、停利與決策輸出欄位規範 |
| [`agents/openai.yaml`](./agents/openai.yaml) | agent 介面與預設提示描述 |
| [`scripts/run_daily_scan.py`](./scripts/run_daily_scan.py) | 先前版本留下的 demo scan 腳本，作為展示型輔助資產 |
| [`app/streamlit_app.py`](./app/streamlit_app.py) | 先前版本的 demo dashboard 骨架 |

### 版本說明

- `v1.0`
  建立台股分析架構基底。
- `v1.1`
  建立市場掃描與單股 deep-dive 的分析藍圖。
- `v1.2`
  正式聚焦單股研究，升級為多重 AI agent 專業研討會模式。

### 公開入口

- GitHub Repo: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
- Public Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)

### Quick Start

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_daily_scan.py
streamlit run app/streamlit_app.py
```

上面的 scan 與 dashboard 目前仍保留作為展示型資產。  
`v1.2` 的主要價值則在於 skill、blueprint、persona config 與單股研究流程本身。

---

## English

### Exhibit Statement

**Taiwan Stock Radar v1.2** is a professional Taiwan-equity skill focused on one stock at a time. Instead of producing a shallow recommendation from a single prompt, it orchestrates a formal multi-agent research meeting around a selected TWSE or TPEX name.

The core idea is simple:

- one stock enters the room
- multiple specialist AI analysts review it from different angles
- a chair agent moderates disagreement
- the system produces a final decision packet with scenarios, trade zones, risk controls, and invalidation

### What Makes v1.2 Different

- It is no longer centered on a broad-market ranking homepage narrative.
- It treats single-stock analysis as the primary product, not as a secondary memo.
- It uses specialist agents with different personalities, priorities, and weights.
- It preserves disagreement instead of flattening everything into one generic conclusion.
- It aims to resemble a professional investment discussion, not a sentiment summary.

### Specialist Agent Council

| Agent | Responsibility | Examples of focus |
|---|---|---|
| Chief Strategist | Leads the meeting and writes the final synthesis | cross-agent conflicts, decision framing, conclusion quality |
| Technical Strategist | Owns trend and structure | support, resistance, multi-timeframe trend, volume confirmation |
| Chip Flow Analyst | Tracks positioning and capital flow | foreign flow, trust flow, financing, distribution risk |
| Fundamental Analyst | Tests business quality | revenue trajectory, earnings quality, product cycle, valuation story |
| Catalyst Analyst | Monitors timing | earnings, monthly revenue, policy, launches, industry catalysts |
| Risk Manager | Challenges the thesis | liquidity, volatility, fragility, downside asymmetry |

### Standard Output

The expected output is a professional decision packet:

- final thesis
- tactical, swing, and position-horizon trend view
- base, bull, and bear scenarios
- preferred buy zone
- aggressive and conservative entry triggers
- stop-loss and invalidation
- take-profit ladder
- weighted consensus and dissent notes

### Project Assets

The repository combines a public-facing presentation layer with reusable skill assets:

- a `v1.2` skill definition in [`SKILL.md`](./SKILL.md)
- a multi-agent research blueprint in [`references/agent-analyst-blueprint.md`](./references/agent-analyst-blueprint.md)
- Taiwan-market heuristics in [`references/taiwan-market-playbook.md`](./references/taiwan-market-playbook.md)
- prediction discipline in [`references/prediction-framework.md`](./references/prediction-framework.md)
- persona configuration in [`config/agent_personas.yaml`](./config/agent_personas.yaml)

### Public Links

- Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- GitHub: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
