# Táiwān gǔshì AI Radar v1.0

台股量化研究框架 — 正式版本 1.0 架構與說明文件

版本：v1.0  
專案名稱：`taiwan-gushi-ai-radar`  
定位：開源台股量化研究 / 選股 / 回測 / 訊號框架  
用途：作為 GitHub 專案正式架構說明，供後續由 Codex App 接手工程實作。

---

## 1. 專案定位

**Táiwān gǔshì AI Radar** 是一個面向台灣股票市場的開源量化研究框架。  
它的目標不是直接提供保證獲利的投資建議，而是提供一套 **可擴充、可回測、可解釋、可展示** 的研究基礎設施，讓開發者、研究者與交易者可以：

- 建立台股市場資料管線
- 萃取技術面、量價、籌碼、基本面、族群與市場環境特徵
- 建立雷達分數與觀測排序
- 執行歷史回測
- 生成買入 / 賣出 / 觀察訊號
- 透過視覺化介面展示市場狀態
- 以每日自動掃描產出 Top 20 觀測名單

本文件是 **正式版本 1.0 的工程規格**，聚焦在：

1. 研究框架完整性
2. 程式碼結構清晰與易維護
3. 可由 Codex App 接手實作
4. 保留後續 AI / ML / ranking model 擴充空間
5. 提供足夠好的 demo layer，以利 GitHub 開源專案吸引 star

---

## 2. v1.0 範圍

### 2.1 包含內容

v1.0 預計包含以下核心能力：

- 台股資料載入接口
- 統一資料格式與資料驗證
- 技術面、量價、動能、籌碼、品質、族群與市場特徵工程
- 雷達評分模型
- 市場 regime 判斷
- 風險調整層
- 訊號引擎
- 單策略回測引擎
- Streamlit dashboard MVP
- Market heatmap MVP
- Daily auto scan 與 Top 20 輸出
- 範例腳本與基本文件

### 2.2 不包含內容

v1.0 暫不實作：

- 真實券商下單 API
- 多資產投資組合最佳化
- 強化學習交易代理
- 高頻交易
- 盤中即時撮合模擬
- 新聞 NLP 與事件驅動交易
- 分散式回測叢集
- 複雜的超參數搜尋平台

這些項目可列入後續 roadmap。

---

## 3. 設計原則

### 3.1 模組化

避免把資料清洗、因子計算、策略邏輯、回測流程、dashboard 與報表混在單一檔案中。

### 3.2 可替換

每個模組應支援替換，例如：

- 不同資料來源
- 不同因子模型
- 不同進出場規則
- 不同風控模型
- 不同展示層

### 3.3 可回測

所有會影響策略結果的規則，都應能以程式落地並可回測，而不是只存在 README 描述。

### 3.4 可解釋

v1.0 以規則式與因子式為主，讓使用者能清楚理解：

- 為什麼某檔股票分數較高
- 哪些因子給了加分
- 哪些風險條件造成降權
- 訊號是如何生成的

### 3.5 可擴充到 AI / ML

v1.0 不強制納入 ML，但介面設計必須預留：

- `model_score`
- `probability`
- `expected_return`
- `ranking_model`

這樣後續可加入 LightGBM、XGBoost、Learning-to-Rank 等模型。

### 3.6 展示優先

作為 GitHub 開源專案，v1.0 需要至少有可視化介面與可重複產出結果，避免 repo 看起來只有底層程式碼而缺乏可展示性。

---

## 4. 系統總體架構

系統建議採用以下分層：

1. **Data Layer**：資料層  
2. **Feature Layer**：特徵層  
3. **Factor / Scoring Layer**：因子與評分層  
4. **Strategy Layer**：策略層  
5. **Signal Layer**：訊號層  
6. **Risk Layer**：風控層  
7. **Backtest Layer**：回測層  
8. **App / Visualization Layer**：展示層  
9. **Output Layer**：輸出層  
10. **Automation Layer**：自動化層

資料流如下：

```text
Data Source
  ↓
Data Loader
  ↓
Data Normalizer / Cleaner
  ↓
Feature Engineering
  ↓
Factor Calculation
  ↓
Radar Scoring
  ↓
Strategy Rules
  ↓
Risk Adjustment
  ↓
Signal Generation
  ↓
Backtest / Dashboard / Daily Output / Export
```

---

## 5. 建議專案目錄結構

```text
taiwan-gushi-ai-radar/
├─ README.md
├─ LICENSE
├─ pyproject.toml
├─ requirements.txt
├─ .gitignore
├─ config/
│  ├─ settings.yaml
│  ├─ weights.yaml
│  └─ universe.yaml
├─ data/
│  ├─ raw/
│  ├─ interim/
│  └─ processed/
├─ docs/
│  ├─ architecture.md
│  ├─ strategy.md
│  ├─ backtesting.md
│  ├─ data-model.md
│  └─ roadmap.md
├─ src/
│  ├─ __init__.py
│  ├─ data_loader/
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ twse_loader.py
│  │  ├─ tpex_loader.py
│  │  ├─ finmind_loader.py
│  │  ├─ market_watch_loader.py
│  │  └─ local_csv_loader.py
│  ├─ preprocessing/
│  │  ├─ __init__.py
│  │  ├─ cleaner.py
│  │  ├─ aligner.py
│  │  └─ validator.py
│  ├─ features/
│  │  ├─ __init__.py
│  │  ├─ technical_features.py
│  │  ├─ momentum_features.py
│  │  ├─ volume_features.py
│  │  ├─ capital_features.py
│  │  ├─ fundamental_features.py
│  │  ├─ sector_features.py
│  │  ├─ market_features.py
│  │  └─ feature_pipeline.py
│  ├─ factors/
│  │  ├─ __init__.py
│  │  ├─ factor_model.py
│  │  ├─ scoring.py
│  │  └─ normalization.py
│  ├─ regime/
│  │  ├─ __init__.py
│  │  └─ market_regime.py
│  ├─ risk/
│  │  ├─ __init__.py
│  │  ├─ risk_model.py
│  │  ├─ stop_rules.py
│  │  └─ position_filter.py
│  ├─ strategy/
│  │  ├─ __init__.py
│  │  ├─ radar_strategy.py
│  │  ├─ breakout_strategy.py
│  │  └─ pullback_strategy.py
│  ├─ signals/
│  │  ├─ __init__.py
│  │  └─ signal_engine.py
│  ├─ backtest/
│  │  ├─ __init__.py
│  │  ├─ backtester.py
│  │  ├─ metrics.py
│  │  ├─ trade_log.py
│  │  └─ portfolio_simulator.py
│  ├─ reports/
│  │  ├─ __init__.py
│  │  ├─ console_report.py
│  │  ├─ markdown_report.py
│  │  └─ csv_export.py
│  ├─ app/
│  │  ├─ streamlit_app.py
│  │  └─ pages/
│  │     ├─ market_overview.py
│  │     ├─ stock_detail.py
│  │     ├─ sector_rotation.py
│  │     └─ backtest_report.py
│  └─ utils/
│     ├─ __init__.py
│     ├─ logger.py
│     ├─ dates.py
│     ├─ math_utils.py
│     └─ helpers.py
├─ scripts/
│  ├─ run_daily_scan.py
│  ├─ generate_heatmap.py
│  └─ export_dashboard_data.py
├─ output/
│  ├─ daily_top20.csv
│  ├─ daily_top20.json
│  └─ daily_summary.md
├─ examples/
│  ├─ scan_market.py
│  ├─ generate_signal.py
│  ├─ backtest_strategy.py
│  └─ compare_strategies.py
├─ notebooks/
│  ├─ 01_data_exploration.ipynb
│  ├─ 02_feature_research.ipynb
│  └─ 03_strategy_backtest.ipynb
├─ tests/
│  ├─ test_features.py
│  ├─ test_scoring.py
│  ├─ test_signals.py
│  └─ test_backtest.py
└─ .github/
   └─ workflows/
      └─ daily_scan.yml
```

---

## 6. 核心資料模型

### 6.1 基礎市場資料欄位

所有資料載入後，應盡量轉成統一 schema：

| 欄位 | 說明 |
|---|---|
| date | 交易日期 |
| symbol | 股票代號 |
| name | 股票名稱 |
| open | 開盤價 |
| high | 最高價 |
| low | 最低價 |
| close | 收盤價 |
| volume | 成交量 |
| turnover | 成交值 |
| market | 上市 / 上櫃 |
| sector | 產業或族群 |

### 6.2 籌碼資料欄位

| 欄位 | 說明 |
|---|---|
| foreign_buy | 外資買賣超 |
| trust_buy | 投信買賣超 |
| dealer_buy | 自營商買賣超 |
| margin_balance | 融資餘額 |
| short_balance | 融券餘額 |
| sbl_balance | 借券餘額（若可得） |

### 6.3 基本面資料欄位

| 欄位 | 說明 |
|---|---|
| revenue_yoy | 月營收年增率 |
| revenue_mom | 月營收月增率 |
| eps | 每股盈餘 |
| roe | 股東權益報酬率 |
| gross_margin | 毛利率 |
| debt_ratio | 負債比 |

### 6.4 計算後特徵欄位

| 欄位 | 說明 |
|---|---|
| ma20 | 20 日均線 |
| ma60 | 60 日均線 |
| rsi14 | RSI |
| atr14 | ATR |
| return_5d | 5 日報酬 |
| return_20d | 20 日報酬 |
| relative_strength | 相對強弱 |
| volume_ratio_20d | 量比 |
| trend_score | 趨勢分數 |
| capital_score | 籌碼分數 |
| radar_score | 總雷達分數 |

---

## 7. 資料來源策略

### 7.1 核心研究資料來源

v1.0 的核心研究資料來源建議為：

- TWSE
- TPEx
- FinMind
- 本地 CSV / parquet

這些資料來源用於：

- 歷史回測
- 特徵工程
- 因子計算
- 日終策略掃描

### 7.2 市場追蹤資料來源

為提升 dashboard 可用性與市場觀察能力，可加入下列網站作為 **市場追蹤來源**：

- Yahoo 奇摩股市：`https://tw.stock.yahoo.com/`
- WantGoo 玩股：`https://www.wantgoo.com/stock`
- 鉅亨網台股：`https://www.cnyes.com/twstock`

這三個來源主要用於：

- 市場概覽連結
- 熱門排行觀察
- 類股與個股頁面追蹤入口
- dashboard 的外部追蹤入口

### 7.3 合規與授權原則

v1.0 應避免在未確認授權前，將上述網站當成完整歷史研究資料的主要抓取來源。

原則如下：

- **核心回測資料** 應優先來自可驗證且穩定的資料來源
- **市場追蹤網站** 應優先視為 dashboard 入口或輔助觀察來源
- 若未來需要正式抓取其資料，應先檢視 robots、使用條款、授權限制與頻率控制
- 工程上要將 `market_watch_loader` 與核心 `data_loader` 解耦

---

## 8. 特徵工程模組

### 8.1 技術面特徵

- MA5 / MA10 / MA20 / MA60 / MA120
- 均線斜率
- RSI
- MACD
- KD
- ATR
- 布林通道
- 前高 / 前低突破偵測

### 8.2 量價特徵

- 當日量與 5 / 20 日均量比
- 價漲量增 / 價跌量增
- 突破量能確認
- 爆量長黑
- 縮量整理後放量

### 8.3 籌碼特徵

- 外資 / 投信 / 自營商買賣超
- 法人連買 / 連賣天數
- 融資增減
- 融券增減
- 借券餘額變化

### 8.4 品質特徵

- 營收成長
- EPS 趨勢
- ROE
- 毛利率
- 負債比

### 8.5 市場與族群特徵

- 大盤 MA20 / MA60 結構
- 櫃買指數強弱
- 市場成交量變化
- 類股輪動排名
- 同族群相對強弱

---

## 9. 因子與評分模型

### 9.1 雷達評分結構

建議使用 100 分制，預設權重如下：

| 模組 | 權重 |
|---|---:|
| Trend | 20 |
| Volume | 15 |
| Capital Flow | 20 |
| Quality | 10 |
| Momentum | 10 |
| Sector | 10 |
| Market | 5 |
| Risk Adjustment | -20 ~ 0 |

### 9.2 分數分級

| 分數區間 | 分類 |
|---|---|
| 80 - 100 | 高優先觀測 |
| 65 - 79 | 偏多觀察 |
| 50 - 64 | 中性觀察 |
| 0 - 49 | 風險警示 |

### 9.3 設計原則

- 分數高不代表必漲
- 分數低不代表必跌
- 分數是綜合觀測結果
- 若欄位缺失，需降低可信度或標註資料不足

---

## 10. 市場 Regime 模組

v1.0 應先判斷市場環境，再調整策略權重。

### 10.1 Regime 類型

- Bull Market
- Sideways Market
- Bear Market
- High Volatility

### 10.2 判斷依據

- 加權指數是否站上 MA20 / MA60
- 櫃買指數是否同步轉強
- 市場成交量是否擴大
- 強勢股續航比例
- 類股擴散度

### 10.3 Regime 對策略的影響

- 多頭：提高趨勢與動能權重
- 盤整：提高突破確認門檻
- 空頭：提高風險權重、降低樂觀訊號
- 高波動：採保守模式

---

## 11. 風控模組

v1.0 的風控必須獨立存在，而不是只在最後扣幾分。

### 11.1 風險旗標

- 成交量過低
- ATR 過高
- 爆量長黑
- 跌破 MA20
- 融資暴增
- 法人連賣
- 市場 regime 轉弱

### 11.2 風控輸出

- `risk_flags`
- `risk_score`
- `stop_loss`
- `take_profit`
- `position_filter`

### 11.3 停損停利邏輯

建議保留兩類：

- 固定百分比停損 / 停利
- ATR-based 停損 / 移動停利

---

## 12. 策略與訊號引擎

### 12.1 v1.0 優先策略

- 雷達總分排序策略
- Breakout strategy
- Pullback strategy

### 12.2 買入條件範例

- 價格站上 MA20 且 MA20 > MA60
- 20 日相對強弱高於門檻
- 成交量高於 20 日均量一定倍數
- 風險旗標未觸發關鍵否決條件

### 12.3 賣出條件範例

- 跌破 MA20
- 動能明顯轉弱
- 爆量長黑
- 觸發停損或移動停利

### 12.4 訊號分類

- Strong Buy Watch
- Buy Watch
- Hold
- Sell Watch
- Risk Alert

---

## 13. 回測引擎

### 13.1 目標

- 驗證規則是否具有統計優勢
- 比較不同策略表現
- 驗證不同 regime 下的有效性

### 13.2 基本能力

- 日頻回測
- 單標的 / 多標的回測
- 交易日誌記錄
- 費用與滑價參數保留

### 13.3 回測指標

- Win rate
- Average return
- Max drawdown
- Sharpe ratio
- Annualized return
- Profit factor

### 13.4 注意事項

回測報表應明確標示：

- 回測期間
- 策略版本
- 交易成本是否納入
- 滑價是否納入
- 歷史績效不代表未來

---

## 14. Streamlit Dashboard MVP

Streamlit dashboard 應作為 v1.0 的主要互動展示層。

### 14.1 目標

- 提供市場雷達總覽
- 讓使用者可互動檢視個股分數與風險
- 提高 GitHub 專案可展示性

### 14.2 建議頁面

- Market Overview
- Radar Ranking Table
- Stock Detail
- Sector Rotation
- Backtest Summary

### 14.3 建議顯示內容

- Top 20 雷達股
- 單股因子拆解
- 風險旗標
- 買入 / 賣出 / 觀察訊號
- 市場 regime 摘要
- 類股強弱摘要
- 外部市場追蹤入口

---

## 15. Market Heatmap

### 15.1 目標

- 以視覺方式展示市場強弱
- 快速辨識強勢族群與弱勢族群
- 提升 dashboard 吸引力

### 15.2 建議形式

- Sector heatmap
- Radar score heatmap
- Relative strength heatmap
- Treemap by sector

### 15.3 技術建議

- 優先使用 Plotly
- 可搭配 Streamlit 呈現
- 色彩對應 radar score、return 或 capital flow

---

## 16. Daily Auto Scan

### 16.1 目標

- 收盤後自動掃描市場
- 生成 Top 20 名單
- 產生 markdown / csv / json 輸出
- 供 dashboard 與歷史紀錄使用

### 16.2 工作流程

```text
Market data update
→ feature calculation
→ radar scoring
→ risk filtering
→ ranking
→ output Top 20
→ update dashboard data
```

### 16.3 輸出檔案

- `output/daily_top20.csv`
- `output/daily_top20.json`
- `output/daily_summary.md`

### 16.4 自動化方式

- GitHub Actions
- cron job
- APScheduler

---

## 17. 設定檔建議

### 17.1 `settings.yaml`

建議包含：

- 預設資料來源
- 市場追蹤來源開關
- dashboard 設定
- 回測參數
- 輸出路徑
- 自動掃描時間

範例：

```yaml
data_sources:
  core:
    - twse
    - tpex
    - finmind
  market_watch:
    yahoo_tw_stock: true
    wantgoo_stock: true
    cnyes_twstock: true

output:
  save_daily_top20_csv: true
  save_daily_top20_json: true
  save_daily_summary_md: true

app:
  enable_dashboard: true
  enable_heatmap: true
```

### 17.2 `weights.yaml`

獨立存放因子權重，方便研究與調整。

### 17.3 `universe.yaml`

定義掃描股票池：

- 上市全體
- 上櫃全體
- ETF
- 自訂名單

---

## 18. README 與 GitHub 展示建議

為提升 GitHub star，README 建議至少包含：

- 專案簡介
- 功能總覽
- 架構圖
- dashboard 截圖
- heatmap 截圖
- Top 20 輸出範例
- 安裝方式
- 快速開始
- 風險聲明
- roadmap

建議 GitHub topics：

- quantitative-trading
- algorithmic-trading
- taiwan-stock-market
- backtesting
- ai-trading
- stock-market
- finance
- machine-learning

---

## 19. 開發優先順序

### Phase 1

- Data loader
- Feature pipeline
- Radar scoring
- Signal engine
- Basic backtest

### Phase 2

- Streamlit dashboard MVP
- Daily auto scan
- Markdown / CSV / JSON export

### Phase 3

- Market heatmap
- Sector rotation page
- Historical scan archive

---

## 20. Roadmap

### v1.1

- Sector rotation enhancement
- Historical scan archive
- More backtest reports

### v1.2

- Machine learning ranking interface
- Strategy comparison tools
- Extended factor research

### v2.0

- Ranking model integration
- Portfolio construction
- More advanced research workflows

---

## 21. 風險聲明

本專案僅供研究、教育與工程實作用途。  
專案輸出的分數、排序、訊號與回測結果，均不構成投資建議或保證報酬。  
任何實際投資行為均應由使用者自行判斷並承擔風險。

---

## 22. 給 Codex App 的實作指引

Codex App 接手時，建議依下列順序拆工程：

1. 建立 repo 基礎檔案與目錄結構
2. 實作資料載入與統一 schema
3. 完成 feature pipeline
4. 完成 factor scoring 與 signal engine
5. 完成 basic backtest
6. 製作 Streamlit dashboard MVP
7. 加入 heatmap 與 daily auto scan
8. 補 tests、README、docs

v1.0 的重點不是一次做滿所有量化功能，而是先做出：

- 結構正確
- 可跑
- 可回測
- 可展示
- 可擴充

這樣就適合先正式發佈到 GitHub，並讓後續工程逐步演進。
