
---

## 開發計劃（Roadmap）

### Phase 1：基礎可運行版本（MVP）
- [x] 專案結構與設定
- [ ] Buttplug 連線 + 基本震動控制
- [ ] DeepSeek Tool Calling 接駁
- [ ] 簡單文字輸入測試（先唔用語音）
- [ ] 急停（Esc）與 30 秒超時保護

### Phase 2：語音輸入
- [ ] 接入 RealtimeSTT
- [ ] 支援 Push-to-Talk
- [ ] 支援連續聽模式
- [ ] 語音「停」指令

### Phase 3：AI 語音回覆
- [ ] 接入 edge-TTS
- [ ] AI 回覆時同步控制玩具
- [ ] 廣東話 System Prompt 優化

### Phase 4：體驗優化
- [ ] 震動模式（pulse、wave、pattern）
- [ ] 狀態顯示優化
- [ ] 錯誤處理與重連機制
- [ ] 設定檔完善

### Phase 5（之後再考慮）
- [ ] 簡單 Web UI
- [ ] 多角色人格切換
- [ ] 本地模型支援（Ollama）
- [ ] 錄音與對話記錄

---

## 安全設計原則

1. **急停優先**：任何時候按 Esc 或講「停」，必須即時停止所有震動。
2. **超時保護**：單一連續震動指令最長 30 秒，超時自動停止。
3. **強度上限**：預設最高 0.85，可在設定中調整。
4. **本地優先**：語音轉文字與控制邏輯盡量在本地完成，只有文字會傳去 DeepSeek API。

---

## 使用前準備

1. 安裝並啟動 [Intiface Central](https://intiface.com/central)
2. 連接你的玩具（或使用模擬裝置測試）
3. 申請 DeepSeek API Key
4. Python 3.10 或以上

---

## 注意事項

- 本軟體僅供 **同意的成年人** 私人使用
- 請確保玩具支援 Buttplug / Intiface
- 使用時請注意身體狀況，適時休息
- 開發過程中建議先用 Intiface 的模擬裝置測試

---

## 目前狀態

**Phase 1 準備開始**

等待確認後開始實作 MVP。