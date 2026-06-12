from __future__ import annotations

from pathlib import Path
import zipfile

import scripts.build_chinese_reference_docx as build_ref
import scripts.export_chinese_thesis as export


def test_profile_assets_exist() -> None:
    for profile in export.PROFILES.values():
        assert profile.tex_template.exists()
        assert profile.reference_docx.exists()


def test_docx_reference_files_are_valid_zip_archives() -> None:
    for profile in export.PROFILES.values():
        with zipfile.ZipFile(profile.reference_docx) as archive:
            names = set(archive.namelist())
            assert "[Content_Types].xml" in names
            assert "word/styles.xml" in names
            styles = archive.read("word/styles.xml").decode("utf-8")
            assert "Times New Roman" in styles
            assert "宋体" in styles
            assert "黑体" in styles


def test_build_pandoc_args_docx_uses_reference_docx(tmp_path: Path) -> None:
    profile = export.PROFILES["guangxi-undergrad"]
    args = export.build_pandoc_args(
        pandoc="pandoc",
        input_path=tmp_path / "paper.md",
        output_path=tmp_path / "paper.docx",
        output_format="docx",
        profile=profile,
    )
    assert "--reference-doc" in args
    assert str(profile.reference_docx) in args
    assert "--template" not in args


def test_build_pandoc_args_pdf_uses_tex_template(tmp_path: Path) -> None:
    profile = export.PROFILES["sichuan-grad"]
    args = export.build_pandoc_args(
        pandoc="pandoc",
        input_path=tmp_path / "paper.md",
        output_path=tmp_path / "paper.pdf",
        output_format="pdf",
        profile=profile,
    )
    assert "--template" in args
    assert str(profile.tex_template) in args
    assert "--pdf-engine" in args
    assert "xelatex" in args


def test_build_tool_env_returns_path() -> None:
    env = export.build_tool_env()
    assert "PATH" in env
    assert isinstance(env["PATH"], str)


def test_patch_styles_xml_sets_chinese_fonts() -> None:
    xml = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
    </w:styles>
    """
    patched = build_ref.patch_styles_xml(xml, build_ref.PROFILES["mainland-fallback"]).decode("utf-8")
    assert "Times New Roman" in patched
    assert "宋体" in patched
    assert "黑体" in patched
    assert "firstLineChars" in patched
