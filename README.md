# Taiwan Stock Radar

[![GitHub repo](https://img.shields.io/badge/GitHub-rabbit68116--ux%2Ftaiwan--stock--radar-181717?logo=github)](https://github.com/rabbit68116-ux/taiwan-stock-radar)
![Status](https://img.shields.io/badge/status-architecture%20v1.0-blue)
![Skill](https://img.shields.io/badge/skill-v1.2-orange)
![Market](https://img.shields.io/badge/market-Taiwan%20Stocks-red)
![Mode](https://img.shields.io/badge/mode-single--stock%20multi--agent-green)

Taiwan Stock Radar v1.2 is a Taiwan-equity research skill built for AI agents that need to evaluate one stock with the discipline of a professional investment committee.

> One stock. Six specialist AI analysts. One formal research meeting. One structured decision packet.

[Official Website](https://rabbit68116-ux.github.io/taiwan-stock-radar/) | [Featured Case Study](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html) | [GitHub Repo](https://github.com/rabbit68116-ux/taiwan-stock-radar)

---

## 繁體中文

### 封面定位

**Taiwan Stock Radar** 是一個專注於台灣股票單股研判的 AI skill。  
它不是一般的看盤摘要，也不是只有一句看多看空的選股工具，而是把一檔股票交給多位不同專長的 AI agent 分身，模擬一場正式的投資研究會議。

這個專案展示的是一種更專業的工作方式：

- 用多位 specialist agent 拆開不同分析視角
- 讓技術面、籌碼面、基本面、事件面、風險面分開陳述
- 用主持 agent 做權重整合與衝突裁決
- 最後輸出一份可執行、可檢討、可更新的決策文件

### 產品價值主張

Taiwan Stock Radar 解決的不是「找一檔今天最會漲的股票」，而是更根本的問題：

- 如何讓 AI 對一檔台股做出像資深研究團隊一樣的判斷
- 如何把分歧觀點保留下來，而不是用一段空泛敘事把它們蓋掉
- 如何把觀點轉成買點、停損、停利、失效條件與信心分級
- 如何讓最終輸出更像專業會議結論，而不是聊天式回答

### Exhibit Snapshot

| 項目 | 說明 |
|---|---|
| Product mode | `v1.2` single-stock multi-agent council |
| Coverage | `TWSE / TPEX` 單股深度研判 |
| Output style | 專業會議摘要 + 決策文件 |
| Final deliverable | 趨勢預測、情境分支、買入區、停損區、停利區、失效條件 |
| Public surface | GitHub repo + GitHub Pages product site |

### 多重 AI Agent 研討會

在 `v1.2` 中，單一股票會進入一個多 agent council。每位 agent 有不同性格、專業、指標權重與發言責任。

| AI Agent | 角色定位 | 核心觀察 | 權重 |
|---|---|---|---:|
| Chief Strategist | 主持研究會議，整合全局結論 | 市場背景、結論整合、衝突裁決 | 0.24 |
| Technical Strategist | 技術面與趨勢結構分析 | 多週期趨勢、支撐壓力、量價結構 | 0.18 |
| Chip Flow Analyst | 籌碼與資金流向分析 | 外資、投信、融資、主力結構 | 0.18 |
| Fundamental Analyst | 基本面與品質分析 | 月營收、獲利品質、產品週期、估值敘事 | 0.17 |
| Catalyst Analyst | 事件與催化因子分析 | 法說、營收公告、產業事件、政策節點 | 0.11 |
| Risk Manager | 反方與風控代表 | 流動性、波動、失敗型態、部位風險 | 0.12 |

### 會議流程

1. `Case setup`
   確認股票、日期、研究週期、研究目標與資料邊界。
2. `Independent briefs`
   各 specialist agent 獨立提出初步觀點與主要疑慮。
3. `Cross-examination`
   主持 agent 將衝突點攤開，不讓弱點被強行蓋過。
4. `Weighted synthesis`
   依權重整合共識方向，同時保留反方立場。
5. `Decision packet`
   形成正式輸出，包含趨勢研判、情境分析、操作區間與風險條件。

### 單股研討會輸出範例

下面是 GitHub 首頁想展示的輸出樣貌。這不是即時盤中建議，而是產品展示用的標準決策文件格式。

```text
Taiwan Stock Radar v1.2
Illustrative Single-Stock Council Output
Case: 2330 台積電
Analysis Date: 2026-03-13
Horizon: Swing

Committee Thesis
- Base view remains constructive while sector leadership and institutional support stay intact.

Specialist Leaning
- Chief Strategist: Bullish with discipline
- Technical Strategist: Constructive trend continuation
- Chip Flow Analyst: Supportive but watch for distribution
- Fundamental Analyst: Quality remains strong
- Catalyst Analyst: Positive if event window stays orderly
- Risk Manager: Acceptable only with clear invalidation

Scenario Tree
- Base case: range expansion after orderly pullback
- Bull case: leadership continuation with volume confirmation
- Bear case: failed structure plus institutional distribution

Action Plan
- Preferred buy zone: support retest area
- Aggressive trigger: breakout reclaim with volume
- Conservative trigger: weekly confirmation above key resistance
- Stop loss: structural break below support
- TP1: first expansion objective
- TP2: trend extension objective
- Invalidation: thesis weakens if structure fails and chip flow deteriorates together
```

### Featured Case Study

如果你要看更完整的展示頁，不只是摘要格式，可以直接看這一頁：

- [Single-Stock Case Study](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

這個頁面會展示：

- 個案背景與研究問題
- specialist agent 個別觀點
- 共識與分歧整理
- base / bull / bear 三情境框架
- 買入區、停損區、停利區、失效條件
- 為什麼這樣的輸出更像真正的研究會議結果

### 為什麼值得追蹤

- 它展示的是 **AI agent 編排能力**，不是單一 prompt 技巧。
- 它專注在 **台灣股票單股研判**，不是用通用美股邏輯硬套。
- 它把分析過程做成 **可檢討、可辯論、可更新** 的研究流程。
- 它讓 GitHub repo 本身就像一個完整展品，而不是只有工程骨架。

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
| [`docs/index.html`](./docs/index.html) | 公開產品首頁 |
| [`docs/case-study.html`](./docs/case-study.html) | 單股完整展示頁 |

### 公開入口

- GitHub Repo: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
- Public Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- Case Study: [https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

### Quick Start

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_daily_scan.py
streamlit run app/streamlit_app.py
```

目前的 scan 與 dashboard 仍保留為展示型資產。  
`v1.2` 的核心價值則集中在 skill、blueprint、persona config、case study 與公開展示頁。

---

## English

### Cover Statement

**Taiwan Stock Radar v1.2** is a Taiwan-equity research skill designed around one stock at a time. Rather than returning a loose opinion, it stages a formal investment discussion between multiple specialist AI analysts and produces a structured decision packet.

### Product Promise

The system is built to answer a higher-standard question:

- how should an AI agent evaluate one Taiwan stock like a serious research team
- how should disagreement be preserved instead of erased
- how should a view be translated into scenarios, entries, stops, targets, and invalidation

### What the Product Returns

- a weighted committee thesis
- specialist viewpoints across structure, flow, fundamentals, catalysts, and risk
- base, bull, and bear scenarios
- preferred buy zone and alternate entry triggers
- stop-loss and invalidation
- take-profit ladder and dissent notes

### Featured Case Study

The public exhibit includes a dedicated case-study page:

- [Single-Stock Case Study](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

### Public Surfaces

- Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- GitHub: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
