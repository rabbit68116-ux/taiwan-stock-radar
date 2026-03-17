# Taiwan Stock Radar

[![GitHub repo](https://img.shields.io/badge/GitHub-rabbit68116--ux%2Ftaiwan--stock--radar-181717?logo=github)](https://github.com/rabbit68116-ux/taiwan-stock-radar)
![Status](https://img.shields.io/badge/status-architecture%20v1.0-blue)
![Skill](https://img.shields.io/badge/skill-v1.7-orange)
![Market](https://img.shields.io/badge/market-Taiwan%20Stocks-red)
![Mode](https://img.shields.io/badge/mode-shared%20core%20%2B%20Windows%20desktop-green)

Taiwan Stock Radar v1.7 是一個專為台股研究打造的雙軌產品。
它保留原本的 AI skill / CLI / GitHub Pages 研究流程，同時新增一套 Windows 單機版桌面程式。兩條路線共用同一套 Python shared core、同一份 config、同一個版本號來源與同一套輸出 schema，避免後續更新出現功能漂移。

> 每日 08:30 台股日盤預測報告。必要時自動延伸成單股委員會。<br>
> 同一套 shared core，同步服務 AI skill、CLI、GitHub 展示站與 Windows desktop app。<br>
> Daily 08:30 Taiwan market brief. A single-stock committee when deeper work is needed.<br>
> One shared Python core serving the skill, CLI, GitHub showcase, and the Windows desktop app.

[官方網站 Official Website](https://rabbit68116-ux.github.io/taiwan-stock-radar/) | [Windows 版說明 Windows App](https://rabbit68116-ux.github.io/taiwan-stock-radar/windows-app.html) | [案例頁 Featured Case Study](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

---

## 繁體中文

### 產品定位

**Taiwan Stock Radar** 不是單純的盤前新聞摘要，也不是只會輸出一句看多或看空的聊天工具。
`v1.7` 的產品定位，是一套以台股為核心的 shared-core research system：

- `路線 A`：AI skill / CLI / GitHub repo / 文件站
- `路線 B`：Windows 單機版桌面程式

兩條路線都會做同一件事：

1. 在每日 `08:30` 前後整理台股日盤預測報告
2. 需要時自動進入單股委員會
3. 以六層台股訊號引擎、八位專家 AI 分析師與三種交易風格權重，輸出具體的買入區、停損、停利與失效條件

### v1.7 升級重點

- 正式拆成 **雙軌版本**：skill 路線與 Windows desktop 路線同步維護
- 新增 `shared workflow/service layer`，統一四個可呼叫入口：
  - `generate_premarket_brief(...)`
  - `generate_daily_market_brief(...)`
  - `generate_market_scan(...)`
  - `generate_single_stock_committee_report(...)`
- 新增真正可執行的 **單股委員會 engine**
- 新增 [`scripts/run_single_stock_committee.py`](./scripts/run_single_stock_committee.py)
- 新增 [`apps/windows/main.py`](./apps/windows/main.py) `PySide6` 桌面版
- 新增 archive/history 輸出策略，讓 `latest output` 與 `archive output` 同步寫入
- Windows 版與 skill 路線共用 [`config/settings.yaml`](./config/settings.yaml) 的 `plan_version`

### 雙軌產品結構

| 路線 | 角色 | 主要交付 |
|---|---|---|
| Skill / CLI | 保留原本的 AI workflow、GitHub repo、CLI 與文件站 | 08:30 日盤報告、Top20 demo scan、單股委員會報告 |
| Windows Desktop | 原生單機版操作介面 | GUI 執行 daily brief / premarket / scan / single-stock committee |
| Shared Core | 唯一商業邏輯來源 | 同一套 config、同一套 schema、同一版本號、同一輸出格式 |

### 四條 workflow

| Workflow | 用途 | 主要輸出 |
|---|---|---|
| `generate_premarket_brief(...)` | 開市前環境評估 | 夜盤、美股、半導體、VIX、開盤偏向 |
| `generate_daily_market_brief(...)` | 每日 `08:30` 日盤報告 | 10 大重點訊息、開盤偏向、綜合評估、族群觀察、風險提示 |
| `generate_market_scan(...)` | Demo market scan | Top20 watchlist、sector summary、buy zone、stop |
| `generate_single_stock_committee_report(...)` | 單股 deep dive | signal-engine summary、specialist briefs、strategy selection、validation、action plan |

### 單股委員會現在會輸出什麼

`v1.7` 的單股委員會不再只停留在規格文件。現在已經能產出一份真正可執行的決策文件，至少包含：

- analysis date
- symbol / stock context
- linked daily brief summary
- signal-engine summary
- specialist briefs
- style profile
- strategy selection
- validation scorecard
- scenario tree
- buy zone / entry triggers / stop / take-profit / invalidation
- missing data / confidence / dissent

### Windows Desktop 版本

Windows 版採 `PySide6` 原生 GUI，放在 [`apps/windows/`](./apps/windows/)。
桌面版固定提供 5 個主頁籤：

- `Dashboard`
- `08:30 日盤報告`
- `開市前報告`
- `Top20 掃描`
- `單股委員會`

桌面版的行為重點：

- 使用者可以直接在 GUI 內執行 4 條 workflow
- 若單股委員會發現當日 `daily brief` 尚未存在，會先自動補產生
- GUI 會顯示執行狀態、最近輸出時間與結構化結果
- `output/` 保留 latest files，`output/archive/` 保留歷史歸檔

### 專案內容 Repo Contents

| 路徑 | 作用 |
|---|---|
| [`SKILL.md`](./SKILL.md) | `v1.7` 核心 skill 定義，描述雙軌產品與 shared core 行為 |
| [`src/taiwan_stock_radar/workflows.py`](./src/taiwan_stock_radar/workflows.py) | 四條 shared workflow 入口 |
| [`src/taiwan_stock_radar/single_stock_committee.py`](./src/taiwan_stock_radar/single_stock_committee.py) | 可執行單股委員會 engine |
| [`src/taiwan_stock_radar/output_store.py`](./src/taiwan_stock_radar/output_store.py) | latest + archive 輸出管理與 history 讀取 |
| [`scripts/run_daily_market_brief.py`](./scripts/run_daily_market_brief.py) | 產出 08:30 日盤預測報告 |
| [`scripts/run_premarket_brief.py`](./scripts/run_premarket_brief.py) | 產出開市前環境報告 |
| [`scripts/run_daily_scan.py`](./scripts/run_daily_scan.py) | 產出 Top20 demo scan |
| [`scripts/run_single_stock_committee.py`](./scripts/run_single_stock_committee.py) | 產出單股委員會報告 |
| [`apps/windows/main.py`](./apps/windows/main.py) | Windows desktop app 主入口 |
| [`scripts/build_windows_app.py`](./scripts/build_windows_app.py) | Windows 打包腳本 |
| [`requirements-desktop.txt`](./requirements-desktop.txt) | 桌面版依賴 |

### 快速開始 Quick Start

```bash
python3 -m pip install -r requirements.txt
python3 scripts/run_daily_market_brief.py --date 2026-03-17
python3 scripts/run_premarket_brief.py --date 2026-03-17 --profile semi_risk_on
python3 scripts/run_daily_scan.py --date 2026-03-17
python3 scripts/run_single_stock_committee.py --symbol 2330 --date 2026-03-17 --style swing
```

若要啟動桌面版：

```bash
python3 -m pip install -r requirements-desktop.txt
python3 apps/windows/main.py
```

若你是在 Windows 上直接雙擊啟動，也可以使用：

```bat
start_windows_app.bat
```

這支 launcher 會自動：

- 建立 `.venv`
- 檢查 `PySide6`
- 第一次啟動時安裝 `requirements-desktop.txt`
- 啟動 Windows desktop app

若要在 Windows 主機打包 one-folder EXE：

```bash
python3 scripts/build_windows_app.py
```

### 輸出結構

目前系統同時維持：

- latest outputs 直接寫到 [`output/`](./output/)
- history/archive 寫到 [`output/archive/`](./output/archive/)

範例：

- `output/daily_market_brief.json`
- `output/daily_market_brief.md`
- `output/single_stock_committee.json`
- `output/archive/single_stock_committee/2026-03-17/2330/single_stock_committee.md`

### Public Links

- GitHub Repo: [https://github.com/rabbit68116-ux/taiwan-stock-radar](https://github.com/rabbit68116-ux/taiwan-stock-radar)
- Public Website: [https://rabbit68116-ux.github.io/taiwan-stock-radar/](https://rabbit68116-ux.github.io/taiwan-stock-radar/)
- Windows App Page: [https://rabbit68116-ux.github.io/taiwan-stock-radar/windows-app.html](https://rabbit68116-ux.github.io/taiwan-stock-radar/windows-app.html)
- Case Study: [https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html](https://rabbit68116-ux.github.io/taiwan-stock-radar/case-study.html)

### 免責聲明 Disclaimer

Taiwan Stock Radar 僅供研究、教育與產品展示使用，不構成任何形式的投資建議、招攬、保證報酬或個別證券推薦。
專案中的日盤預測報告、夜盤評估、Top20 排名、單股委員會、情境推演、買入區、停損區、停利階梯與失效條件，皆屬方法展示，不應被視為對未來市場走勢或個股表現的確定承諾。
任何交易決策、資金配置與風險承擔，仍應由使用者自行判斷與負責。

---

## English

### Cover Statement

**Taiwan Stock Radar v1.7** is now a dual-track product:

- `Track A`: the original AI skill, CLI workflows, GitHub repo, and docs site
- `Track B`: a native Windows desktop application

Both tracks share the same Python core, the same config, the same output schema, and the same version source.

### What Changed in v1.7

- a shared workflow layer now formalizes four callable entry points
- the single-stock committee is now executable instead of remaining only a spec
- a new `PySide6` Windows desktop app is included under `apps/windows/`
- latest outputs and archived history are written together
- the same version value in `config/settings.yaml` now anchors the product surfaces

### What the Product Returns

- a daily Taiwan market brief at 08:30
- a premarket brief
- a Top20 demo scan
- an executable single-stock committee report
- archived history under `output/archive/`

### Windows Packaging Note

The build script is intended for a Windows host. The current repository includes the desktop app source, the desktop dependencies, and the packaging script, but the actual Windows EXE should be built on Windows.

### Disclaimer

Taiwan Stock Radar is provided for research, education, and product demonstration. It is not investment advice, not a solicitation, and not a guarantee of future returns. Any market brief, scan result, committee memo, scenario, action zone, stop, target, or invalidation rule in this project is illustrative and should not be treated as a certain commitment about future market behavior.
