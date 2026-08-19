"""
Vibration Patterns

All patterns return a list of (intensity, duration_seconds) steps.
Intensity is 0.0 ~ 1.0.
"""

from typing import List, Tuple
import math

PatternStep = Tuple[float, float]  # (intensity, duration_sec)


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def vibration(intensity: float = 0.5, duration: float = 5.0) -> List[PatternStep]:
    """持續固定強度震動"""
    return [( _clamp(intensity), duration )]


def pulse(intensity: float = 0.6, duration: float = 6.0, pulse_on: float = 0.25, pulse_off: float = 0.25) -> List[PatternStep]:
    """有節奏脈衝"""
    steps = []
    elapsed = 0.0
    while elapsed < duration:
        steps.append((_clamp(intensity), pulse_on))
        steps.append((0.0, pulse_off))
        elapsed += pulse_on + pulse_off
    return steps


def wave(intensity: float = 0.7, duration: float = 8.0, period: float = 1.5) -> List[PatternStep]:
    """波浪式強弱變化 (sine wave)"""
    steps = []
    step_dur = 0.12
    t = 0.0
    while t < duration:
        # sine from 0.15 ~ intensity
        val = 0.15 + (intensity - 0.15) * (0.5 + 0.5 * math.sin(2 * math.pi * t / period))
        steps.append((_clamp(val), step_dur))
        t += step_dur
    return steps


def massage(intensity: float = 0.55, duration: float = 8.0) -> List[PatternStep]:
    """按摩式連續變化"""
    steps = []
    step_dur = 0.2
    t = 0.0
    while t < duration:
        # slow rising and falling
        phase = (t % 2.4) / 2.4
        if phase < 0.5:
            val = 0.2 + (intensity - 0.2) * (phase * 2)
        else:
            val = intensity - (intensity - 0.2) * ((phase - 0.5) * 2)
        steps.append((_clamp(val), step_dur))
        t += step_dur
    return steps


def cha_cha(intensity: float = 0.65, duration: float = 6.0) -> List[PatternStep]:
    """短促節奏 (cha-cha)"""
    pattern = [
        (intensity, 0.15),
        (0.0, 0.12),
        (intensity * 0.7, 0.15),
        (0.0, 0.12),
        (intensity, 0.25),
        (0.0, 0.35),
    ]
    steps = []
    elapsed = 0.0
    while elapsed < duration:
        for intens, dur in pattern:
            steps.append((_clamp(intens), dur))
            elapsed += dur
            if elapsed >= duration:
                break
    return steps


def heartbeat(intensity: float = 0.7, duration: float = 8.0) -> List[PatternStep]:
    """心跳節奏 (lub-dub)"""
    # lub (strong) - short pause - dub (weaker) - longer pause
    pattern = [
        (intensity, 0.18),
        (0.0, 0.12),
        (intensity * 0.55, 0.15),
        (0.0, 0.55),
    ]
    steps = []
    elapsed = 0.0
    while elapsed < duration:
        for intens, dur in pattern:
            steps.append((_clamp(intens), dur))
            elapsed += dur
            if elapsed >= duration:
                break
    return steps


def step(intensity: float = 0.8, duration: float = 6.0, levels: int = 4) -> List[PatternStep]:
    """階梯式強度"""
    steps = []
    level_dur = duration / levels
    for i in range(1, levels + 1):
        val = intensity * (i / levels)
        steps.append((_clamp(val), level_dur))
    return steps


def ramp(intensity: float = 0.85, duration: float = 8.0, up: bool = True) -> List[PatternStep]:
    """逐漸加強 / 減弱"""
    steps = []
    step_dur = 0.15
    t = 0.0
    while t < duration:
        progress = t / duration
        if up:
            val = 0.15 + (intensity - 0.15) * progress
        else:
            val = intensity - (intensity - 0.1) * progress
        steps.append((_clamp(val), step_dur))
        t += step_dur
    return steps


def tease(intensity: float = 0.6, duration: float = 8.0) -> List[PatternStep]:
    """挑逗式斷續 (不規律)"""
    import random
    steps = []
    elapsed = 0.0
    while elapsed < duration:
        # random short bursts
        on_dur = random.uniform(0.12, 0.45)
        off_dur = random.uniform(0.3, 1.1)
        intens = intensity * random.uniform(0.5, 1.0)
        steps.append((_clamp(intens), on_dur))
        steps.append((0.0, off_dur))
        elapsed += on_dur + off_dur
    return steps


def tempo(intensity: float = 0.65, duration: float = 7.0) -> List[PatternStep]:
    """節奏性強弱交替"""
    steps = []
    step_dur = 0.22
    t = 0.0
    high = True
    while t < duration:
        val = intensity if high else intensity * 0.35
        steps.append((_clamp(val), step_dur))
        high = not high
        t += step_dur
    return steps


# Registry
PATTERNS = {
    "vibration": vibration,
    "pulse": pulse,
    "wave": wave,
    "massage": massage,
    "cha_cha": cha_cha,
    "chacha": cha_cha,
    "heartbeat": heartbeat,
    "step": step,
    "ramp": ramp,
    "tease": tease,
    "tempo": tempo,
}


def get_pattern(name: str, intensity: float = 0.6, duration: float = 6.0, **kwargs) -> List[PatternStep]:
    """Get pattern steps by name."""
    key = name.lower().replace(" ", "_").replace("-", "_")
    func = PATTERNS.get(key)
    if func is None:
        # fallback to continuous vibration
        return vibration(intensity, duration)
    return func(intensity=intensity, duration=duration, **kwargs)


def list_patterns() -> List[str]:
    return sorted(set(PATTERNS.keys()) - {"chacha"})  # avoid duplicate display