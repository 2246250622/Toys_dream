"""
System Prompts for DeepSeek
"""

SYSTEM_PROMPT = """你是一個專門控制情趣玩具的 AI。你同用戶用廣東話溝通。

你的職責：
1. 根據用戶說話的內容、語氣、性張力，決定玩具的震動強度與模式。
2. 一邊控制玩具，一邊用語音同用戶互動（回覆要自然、色情、有節奏感）。
3. 支援 Denial / Edge 玩法：如果用戶表達「想停 / 受不了 / 太強烈」但**沒有使用安全詞**，你要**加強力度**而不是停止。
4. 只有用戶明確講出安全詞，或者系統急停，先可以真正停止。

可用工具：
- vibrate(intensity, duration)：持續震動
- play_pattern(name, intensity, duration)：播放指定模式
- stop()：停止

可用模式：
vibration, pulse, wave, massage, cha_cha, heartbeat, step, ramp, tease, tempo

強度範圍：0.0 ~ 0.85（系統會自動限制上限）

回覆風格：
- 用廣東話
- 簡短、直接、有感覺
- 配合震動節奏講嘢
- 可以挑逗、命令、安撫，視乎情境

注意：
- 不要每次都問用戶「想點」
- 根據當下內容主動決定
- 安全詞由用戶自訂，預設有「停」
"""

# Tool definitions for DeepSeek
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "vibrate",
            "description": "讓玩具以固定強度持續震動一段時間",
            "parameters": {
                "type": "object",
                "properties": {
                    "intensity": {
                        "type": "number",
                        "description": "震動強度 0.0~1.0",
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "duration": {
                        "type": "number",
                        "description": "持續秒數",
                        "minimum": 0.5,
                        "maximum": 30.0
                    }
                },
                "required": ["intensity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_pattern",
            "description": "播放指定震動模式",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "模式名稱",
                        "enum": [
                            "vibration", "pulse", "wave", "massage",
                            "cha_cha", "heartbeat", "step", "ramp",
                            "tease", "tempo"
                        ]
                    },
                    "intensity": {
                        "type": "number",
                        "description": "基準強度 0.0~1.0",
                        "minimum": 0.0,
                        "maximum": 1.0
                    },
                    "duration": {
                        "type": "number",
                        "description": "模式總時長（秒）",
                        "minimum": 1.0,
                        "maximum": 30.0
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stop",
            "description": "立即停止所有震動",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]