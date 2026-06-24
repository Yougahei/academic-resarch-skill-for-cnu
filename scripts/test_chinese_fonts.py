from __future__ import annotations

from scripts.chinese_fonts import (
    CANONICAL_TO_PLATFORM,
    detect_font_platform,
    latex_font_vars,
    resolve_cjk_font,
)


def test_detect_font_platform_returns_known() -> None:
    assert detect_font_platform() in {"windows", "macos", "linux"}


def test_resolve_cjk_font_windows() -> None:
    assert resolve_cjk_font("宋体", "windows") == "SimSun"
    assert resolve_cjk_font("黑体", "windows") == "SimHei"
    assert resolve_cjk_font("楷体", "windows") == "KaiTi"
    assert resolve_cjk_font("隶书", "windows") == "LiSu"


def test_resolve_cjk_font_macos() -> None:
    assert resolve_cjk_font("宋体", "macos") == "Songti SC"
    assert resolve_cjk_font("黑体", "macos") == "Heiti SC"
    assert resolve_cjk_font("楷体", "macos") == "Kaiti SC"
    assert resolve_cjk_font("隶书", "macos") == "STLiti"


def test_resolve_cjk_font_unknown_canonical_falls_back() -> None:
    assert resolve_cjk_font("未知字体", "windows") == "未知字体"


def test_latex_font_vars_windows() -> None:
    vars_ = latex_font_vars("windows")
    assert vars_["cjkfont"] == "SimSun"
    assert vars_["cjkboldfont"] == "SimHei"
    assert vars_["cjkitalicfont"] == "KaiTi"
    assert vars_["cjksansfont"] == "SimHei"
    assert vars_["cjkmonofont"] == "KaiTi"


def test_latex_font_vars_macos() -> None:
    vars_ = latex_font_vars("macos")
    assert vars_["cjkfont"] == "Songti SC"
    assert vars_["cjkboldfont"] == "Heiti SC"


def test_canonical_to_platform_covers_all_fonts() -> None:
    for canonical in ("宋体", "黑体", "楷体", "隶书"):
        assert "windows" in CANONICAL_TO_PLATFORM[canonical]
        assert "macos" in CANONICAL_TO_PLATFORM[canonical]


def test_resolve_cjk_font_linux() -> None:
    assert resolve_cjk_font("宋体", "linux") == "Noto Serif CJK SC"
    assert resolve_cjk_font("黑体", "linux") == "Noto Sans CJK SC"
    assert resolve_cjk_font("楷体", "linux") == "Noto Serif CJK SC"
    assert resolve_cjk_font("隶书", "linux") == "Noto Serif CJK SC"


def test_latex_font_vars_linux() -> None:
    vars_ = latex_font_vars("linux")
    assert vars_["cjkfont"] == "Noto Serif CJK SC"
    assert vars_["cjkboldfont"] == "Noto Sans CJK SC"


def test_normalise_font_covers_all_platform_aliases() -> None:
    from scripts.postprocess_chinese_thesis_docx import _normalise_font

    assert _normalise_font("SimSun") == "宋体"
    assert _normalise_font("Songti SC") == "宋体"
    assert _normalise_font("Noto Serif CJK SC") == "宋体"
    assert _normalise_font("SimHei") == "黑体"
    assert _normalise_font("Heiti SC") == "黑体"
    assert _normalise_font("Noto Sans CJK SC") == "黑体"
    assert _normalise_font("STLiti") == "隶书"
