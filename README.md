# AI Toy Controller

> 你講嘢 / 按推薦話語 → DeepSeek 理解內容 → 即時控制情趣玩具 + 語音回覆

一個結合 **語音輸入、推薦話語選項、DeepSeek Tool Calling、Buttplug/Intiface、TTS** 的本地 AI 玩具控制系統。

---

## 目前進度

**Phase 1 已完成（文字控制 + 安全機制）**

可以先用文字指令測試玩具控制與模式。

---

## Phase 1 功能

- ✅ 連接 Intiface Central
- ✅ 基本震動控制
- ✅ 10 種震動模式（Vibration / Pulse / Wave / Massage / Cha Cha / Heartbeat / Step / Ramp / Tease / Tempo）
- ✅ Esc 急停
- ✅ 安全詞（預設：停、stop、紅燈、red，可自行新增）
- ✅ 連續震動 30 秒超時自動停止
- ✅ 最大強度限制（預設 0.85）

---

## 快速開始（Phase 1）

### 1. 安裝依賴

```bash
cd ai-toy-controller
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. 啟動 Intiface Central

1. 開啟 [Intiface Central](https://intiface.com/central)
2. 點擊 **Start Server**
3. 連接你的玩具，或新增 **Simulated Device** 測試

### 3. 執行

```bash
python main.py
```

### 4. 常用指令

```
v 60 5          # 60% 強度震動 5 秒
p pulse 70 8    # 播放 Pulse 模式，70% 基準強度，8 秒
p heartbeat 65  # Heartbeat 模式
p tease         # Tease 模式
s / stop / 停   # 停止
patterns        # 列出所有模式
safeword 香蕉   # 新增安全詞
max 80          # 設定最大強度 80%
status          # 查看狀態
q               # 離開
```

**急停**：按 `Esc` 鍵

---

## 專案結構

```
ai-toy-controller/
├── main.py                 # Phase 1 主程式（文字控制）
├── config.py               # 設定
├── toy_controller.py       # Buttplug 控制 + 安全層
├── patterns.py             # 震動模式定義
├── prompts.py              # DeepSeek System Prompt + Tools
├── requirements.txt
└── README.md
```

---

## 震動模式說明

| 模式        | 說明                     |
|-------------|--------------------------|
| vibration   | 持續固定強度             |
| pulse       | 有節奏脈衝               |
| wave        | 波浪式強弱變化           |
| massage     | 按摩式連續變化           |
| cha_cha     | 短促節奏                 |
| heartbeat   | 心跳節奏 (lub-dub)       |
| step        | 階梯式強度               |
| ramp        | 逐漸加強                 |
| tease       | 挑逗式不規律斷續         |
| tempo       | 節奏性強弱交替           |

---

## 後續 Phase 計劃

### Phase 2：DeepSeek 接駁
- DeepSeek Tool Calling
- System Prompt（廣東話 + Denial 邏輯）
- 文字輸入 → AI 自動決定模式與強度

### Phase 3：語音輸入
- RealtimeSTT
- 連續聽 + Push-to-Talk
- 語音安全詞

### Phase 4：AI 語音回覆
- edge-TTS（香港廣東話）
- AI 一邊控制、一邊講嘢

### Phase 5：推薦話語按鈕
- 快捷台詞選項
- 簡單 UI

---

## 安全設計

1. **急停優先**：Esc 或安全詞 → 即時停止
2. **自訂安全詞**：可隨時新增
3. **超時保護**：連續震動超過 30 秒自動停
4. **強度上限**：預設最高 85%
5. **Denial 邏輯**（Phase 2 實作）：表達想停但未用安全詞 → 加強力度

---

## 注意事項

- 本軟體僅供同意的成年人私人使用
- 開發時建議先用 Intiface 模擬裝置測試
- 請適時休息，注意身體狀況
```