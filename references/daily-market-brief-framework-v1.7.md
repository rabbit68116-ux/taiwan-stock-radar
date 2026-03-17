# Daily Market Brief Framework v1.7

Version: `v1.7`

這份文件定義 Taiwan Stock Radar `v1.7` 的第一層產品輸出：**每日 08:30 台股日盤預測報告**。

## 1. 核心目的

08:30 日盤報告的任務不是預言指數點位，而是把隔夜市場壓縮成一份可執行的早盤判讀：

- 台指期夜盤是否支持今天的風險偏好
- 美股大盤、半導體與 AI 指標是否同步
- 新聞流向是否加強或削弱原本的外盤訊號
- 今天應優先觀察哪些族群、避免哪些風險

## 2. 固定資料來源

`v1.7` 正式來源配比為：

- 台指期夜盤
- Yahoo奇摩股市
- Anue 鉅亨網
- 美國大盤與半導體關鍵指標

## 3. 固定輸出欄位

每份報告至少輸出：

- `analysis_date`
- `generated_at_local`
- `scheduled_time_local`
- `opening_bias`
- `opening_score`
- `headline_score`
- `overall_score`
- `overall_label`
- `overall_summary`
- `top_messages`
- `sector_watchlist`
- `risk_flags`
- `sources`
- `disclaimer`

## 4. 十大訊息結構

固定為 `10` 則：

- `4` 則市場訊號
- `6` 則新聞訊息

市場訊號：

1. 台指期夜盤
2. S&P 500 / Nasdaq / Dow
3. SOX / TSM ADR / NVIDIA
4. VIX

新聞訊息：

- Yahoo 台股 `3`
- Anue 台股 `2`
- Anue 美股 `1`

## 5. 容錯規則

`v1.7` 不允許單一 live source 中斷就讓整份報告失效。

如果單一來源失敗：

- 保留其餘可用來源
- 下調該面向權重
- 在 `sources` 與 `risk_flags` 明確標示缺口

如果核心行情來源不足：

- 仍可輸出報告
- 但整體結論必須自動降級成保守語氣

## 6. 與單股委員會的關係

`single_stock_committee` 在 `v1.7` 中屬於第二層輸出。
若同日的 `daily_market_brief` 不存在，單股 workflow 必須先補產生它，再進入個股判讀。
