# Windows Desktop Framework v1.7

Version: `v1.7`

這份文件定義 Taiwan Stock Radar `v1.7` 的 Windows 單機版定位。

## 1. 產品角色

Windows 版不是另一套獨立產品，而是 **shared core 的桌面交付層**。

它必須呼叫同一套 Python workflows：

- `generate_premarket_brief(...)`
- `generate_daily_market_brief(...)`
- `generate_market_scan(...)`
- `generate_single_stock_committee_report(...)`

## 2. 固定頁籤

主頁籤固定為：

- Dashboard
- 08:30 日盤報告
- 開市前報告
- Top20 掃描
- 單股委員會

## 3. 固定行為

- GUI 內可直接執行 workflow
- GUI 內直接顯示結構化輸出
- 顯示執行狀態、錯誤訊息與最近輸出時間
- 若單股委員會缺少同日 daily brief，必須自動補產生

## 4. 打包策略

`v1.7` 採 `PyInstaller` one-folder。

注意：

- 真正的 Windows EXE 應在 Windows 主機上打包
- 非 Windows 主機可以做原始碼 smoke check，但不應被當成正式 Windows build 驗收
