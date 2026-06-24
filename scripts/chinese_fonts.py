from __future__ import annotations

import platform

_PLATFORM_MAP = {"Windows": "windows", "Darwin": "macos", "Linux": "linux"}


def detect_font_platform() -> str:
    return _PLATFORM_MAP.get(platform.system(), "windows")


CANONICAL_TO_PLATFORM: dict[str, dict[str, str]] = {
    "宋体": {"windows": "SimSun", "macos": "Songti SC", "linux": "Noto Serif CJK SC"},
    "黑体": {"windows": "SimHei", "macos": "Heiti SC", "linux": "Noto Sans CJK SC"},
    "楷体": {"windows": "KaiTi", "macos": "Kaiti SC", "linux": "Noto Serif CJK SC"},
    "隶书": {"windows": "LiSu", "macos": "STLiti", "linux": "Noto Serif CJK SC"},
}


def resolve_cjk_font(canonical: str, platform: str | None = None) -> str:
    pf = platform or detect_font_platform()
    return CANONICAL_TO_PLATFORM.get(canonical, {}).get(pf, canonical)


PLATFORM_LATEX_FONTS: dict[str, dict[str, str]] = {
    "windows": {"cjkfont": "SimSun", "cjkboldfont": "SimHei", "cjkitalicfont": "KaiTi", "cjksansfont": "SimHei", "cjkmonofont": "KaiTi"},
    "macos": {"cjkfont": "Songti SC", "cjkboldfont": "Heiti SC", "cjkitalicfont": "Kaiti SC", "cjksansfont": "Heiti SC", "cjkmonofont": "Kaiti SC"},
    "linux": {"cjkfont": "Noto Serif CJK SC", "cjkboldfont": "Noto Sans CJK SC", "cjkitalicfont": "Noto Serif CJK SC", "cjksansfont": "Noto Sans CJK SC", "cjkmonofont": "Noto Serif CJK SC"},
}


def latex_font_vars(platform: str | None = None) -> dict[str, str]:
    pf = platform or detect_font_platform()
    return dict(PLATFORM_LATEX_FONTS.get(pf, PLATFORM_LATEX_FONTS["windows"]))
