"""
AI Toy Controller - Phase 1
Text input testing + Toy control + Safety
"""

import asyncio
import logging
import sys
import threading

try:
    import keyboard
except ImportError:
    keyboard = None

from toy_controller import ToyController
import config
from patterns import list_patterns

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("main")


def print_help():
    print("""
==============================
 AI Toy Controller - Phase 1
==============================
指令：
  v <0-100> [秒]     持續震動 (例如 v 60 5)
  p <模式> [強度] [秒]  播放模式
  s / stop           停止
  patterns           列出所有模式
  safeword <詞>      新增安全詞
  max <0-100>        設定最大強度
  status             顯示狀態
  help               說明
  q / quit           離開

支援模式：
""" + ", ".join(list_patterns()) + """

急停：按 Esc 鍵 或 輸入 stop / 停
""")


async def main():
    controller = ToyController()

    # Esc 急停
    if keyboard:
        def on_esc():
            logger.warning("🚨 Esc pressed → Emergency Stop")
            asyncio.create_task(controller.stop())

        keyboard.on_press_key("esc", lambda _: on_esc())
        logger.info("Esc 急停已啟用")
    else:
        logger.warning("keyboard 模組未安裝，Esc 急停不可用（可用 stop 指令）")

    print("正在連接 Intiface Central...")
    ok = await controller.connect()
    if not ok:
        print("❌ 無法連接 Intiface。請確認：")
        print("  1. Intiface Central 已啟動")
        print("  2. Server 已開啟 (預設 ws://127.0.0.1:12345)")
        print("  3. 可先用模擬裝置測試")
        return

    if not controller.has_devices():
        print("⚠️ 目前沒有偵測到裝置。可在 Intiface 加入 Simulated Device 測試。")
    else:
        print(f"✅ 已連接 {len(controller.devices)} 個裝置")

    print_help()

    loop = asyncio.get_event_loop()

    while True:
        try:
            # 用 executor 避免 block event loop
            user_input = await loop.run_in_executor(None, lambda: input("> ").strip())
        except (EOFError, KeyboardInterrupt):
            break

        if not user_input:
            continue

        lower = user_input.lower()

        # 安全詞檢查
        if controller.is_safeword(user_input):
            print("🛑 偵測到安全詞 → 停止")
            await controller.stop()
            continue

        if lower in ("q", "quit", "exit"):
            break

        if lower in ("s", "stop", "停"):
            await controller.stop()
            continue

        if lower == "help":
            print_help()
            continue

        if lower == "patterns":
            print("可用模式：", ", ".join(list_patterns()))
            continue

        if lower == "status":
            print(f"  裝置數量: {len(controller.devices)}")
            print(f"  正在震動: {controller.is_vibrating()}")
            print(f"  最大強度: {controller.max_intensity}")
            print(f"  超時秒數: {controller.timeout_seconds}")
            print(f"  安全詞: {controller.safewords}")
            continue

        if lower.startswith("safeword "):
            word = user_input[9:].strip()
            if word:
                controller.safewords.append(word.lower())
                print(f"✅ 已加入安全詞: {word}")
            continue

        if lower.startswith("max "):
            try:
                val = int(lower.split()[1])
                controller.set_max_intensity(val / 100.0)
                print(f"✅ 最大強度設為 {val}%")
            except Exception:
                print("用法: max <0-100>")
            continue

        if lower.startswith("v "):
            parts = lower.split()
            try:
                percent = int(parts[1])
                duration = float(parts[2]) if len(parts) > 2 else 5.0
                intensity = percent / 100.0
                print(f"▶ 震動 {percent}% × {duration}s")
                await controller.vibrate(intensity, duration)
            except Exception as e:
                print(f"用法: v <0-100> [秒]  ({e})")
            continue

        if lower.startswith("p "):
            parts = user_input.split()
            try:
                name = parts[1]
                intensity = float(parts[2]) / 100.0 if len(parts) > 2 else 0.6
                duration = float(parts[3]) if len(parts) > 3 else 6.0
                print(f"▶ 模式 {name} @ {intensity*100:.0f}% × {duration}s")
                await controller.play_pattern(name, intensity, duration)
            except Exception as e:
                print(f"用法: p <模式> [強度0-100] [秒]  ({e})")
            continue

        print("未知指令，輸入 help 查看說明")

    print("正在關閉...")
    await controller.disconnect()
    print("再見。")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n已中斷")