# Taiwan Indicator Framework v1.7

Version: `v1.7`

這份文件整理 Taiwan Stock Radar `v1.7` 的台股單股指標框架。重點不是堆更多指標名稱，而是把最常用、最能落地的欄位整理成一套 **可同時服務 skill 與 Windows desktop app** 的 shared-core model。

## 1. 六層訊號引擎

每次單股委員會至少要檢查：

1. 趨勢
2. 動能
3. 量價
4. 籌碼
5. 基本面
6. 事件

## 2. 三種交易風格

`v1.7` 固定切換三種 style：

- `short_term`
- `swing`
- `position`

風格切換不是裝飾，而是決定：

- 哪些引擎權重更高
- 哪些欄位只屬於輔助參考
- 哪些策略家族應該優先或避免

## 3. 指標作業原則

- 趨勢面負責定義結構
- 動能面負責節奏與延續性
- 量價面負責辨識真假突破
- 籌碼面負責讀取台股特有資金結構
- 基本面負責確認商業品質
- 事件面負責控制時點風險

## 4. 與 v1.7 shared core 的關係

這份框架不只服務文字型 skill。
同一套指標框架也直接餵給：

- `generate_single_stock_committee_report(...)`
- CLI 輸出
- Windows desktop GUI 顯示

因此任何欄位新增或權重更動，都應優先更新 `config/indicator_catalog.yaml` 與 `config/style_weights.yaml`，而不是先改某個前端。
