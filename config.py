"""
AI Toy Controller - Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ======================
# DeepSeek
# ======================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-pro"  # or deepseek-v4-flash

# ======================
# Intiface / Buttplug
# ======================
INTIFACE_URL = os.getenv("INTIFACE_URL", "ws://127.0.0.1:12345")

# ======================
# Safety
# ======================
# Maximum intensity (0.0 ~ 1.0)
MAX_INTENSITY = float(os.getenv("MAX_INTENSITY", "0.85"))

# Continuous vibration timeout in seconds (auto stop)
CONTINUOUS_TIMEOUT_SECONDS = int(os.getenv("CONTINUOUS_TIMEOUT_SECONDS", "30"))

# Default safewords (user can change at runtime)
DEFAULT_SAFEWORDS = ["停", "stop", "紅燈", "red"]

# ======================
# Patterns
# ======================
# Default pattern duration when not specified
DEFAULT_PATTERN_DURATION = 8.0

# ======================
# TTS
# ======================
TTS_VOICE = "zh-HK-HiuMaanNeural"  # 香港廣東話女聲 (edge-tts)
# Alternatives:
#   zh-HK-HiuGaaiNeural (另一個女聲)
#   zh-HK-WanLungNeural (男聲)
#   zh-CN-XiaoxiaoNeural (普通話)

# ======================
# STT
# ======================
# "continuous" or "ptt"
STT_MODE = "continuous"

# ======================
# Misc
# ======================
CLIENT_NAME = "AI-Toy-Controller"
LOG_LEVEL = "INFO"