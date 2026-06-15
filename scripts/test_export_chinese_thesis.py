from __future__ import annotations

from pathlib import Path
import zipfile

from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

import scripts.build_chinese_reference_docx as build_ref
import scripts.export_chinese_thesis as export
from scripts.postprocess_chinese_thesis_docx import (
    _add_section_breaks_and_page_breaks,
    _is_chapter_heading,
    _paragraph_text,
    postprocess,
)


def test_profile_assets_exist() -> None:
    for profile in export.PROFILES.values():
        assert profile.tex_template.exists()
        assert profile.reference_docx.exists()
        if profile.cover_docx:
            assert profile.cover_docx.exists()


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


def test_docx_cover_files_are_valid_zip_archives() -> None:
    profile = export.PROFILES["guangxi-undergrad"]
    assert profile.cover_docx is not None
    with zipfile.ZipFile(profile.cover_docx) as archive:
        names = set(archive.namelist())
        assert "[Content_Types].xml" in names
        assert "word/document.xml" in names
    doc = Document(str(profile.cover_docx))
    text = _all_docx_text(doc)
    assert "本科毕业论文" in text
    assert "摘要" not in text


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


def test_extract_cover_fields_uses_frontmatter_and_h1_fallback(tmp_path: Path) -> None:
    paper = tmp_path / "paper.md"
    paper.write_text(
        "\n".join(
            [
                "---",
                "college: 管理学院",
                "major: 信息管理",
                "class-name: 信管 2201",
                "student-id: 20260001",
                "author: 张三",
                "advisor: 李老师",
                "date: 二〇二六年六月",
                "---",
                "# LLM 时代企业知识基础设施研究",
                "",
                "## 第1章 绪论",
            ]
        ),
        encoding="utf-8",
    )

    fields = export.extract_cover_fields(paper, export.PROFILES["guangxi-undergrad"])

    assert fields["title"] == "LLM 时代企业知识基础设施研究"
    assert fields["college"] == "管理学院"
    assert fields["student-id"] == "20260001"
    assert fields["paper-type"] == "本科毕业论文"


def test_prepare_markdown_uses_frontmatter_abstracts_and_removes_h1(tmp_path: Path) -> None:
    paper = tmp_path / "paper.md"
    paper.write_text(
        "\n".join(
            [
                "---",
                "title: 元数据标题",
                "title-en: Metadata Title",
                "abstract-zh: 中文摘要内容。",
                "keywords-zh: 关键词一；关键词二",
                "abstract-en: English abstract content.",
                "keywords-en: keyword one; keyword two",
                "---",
                "# 正文里不应重复的标题",
                "",
                "## 第1章 绪论",
                "正文内容",
            ]
        ),
        encoding="utf-8",
    )

    prepared = export.prepare_markdown_for_export(paper, tmp_path)
    normalized = prepared.path.read_text(encoding="utf-8")

    assert prepared.metadata["title"] == "元数据标题"
    assert prepared.metadata["abstract-zh"] == "中文摘要内容。"
    assert "# 正文里不应重复的标题" not in normalized
    assert "## 第1章 绪论" in normalized


def test_prepare_markdown_extracts_inline_abstract_blocks(tmp_path: Path) -> None:
    paper = tmp_path / "paper.md"
    paper.write_text(
        "\n".join(
            [
                "# 论文题目",
                "",
                "## 摘要",
                "中文摘要第一段。",
                "",
                "**关键词**：本体；大模型",
                "",
                "## ABSTRACT",
                "English abstract paragraph.",
                "",
                "Keywords: ontology; LLM",
                "",
                "## 第1章 绪论",
                "正文内容",
            ]
        ),
        encoding="utf-8",
    )

    prepared = export.prepare_markdown_for_export(paper, tmp_path)
    normalized = prepared.path.read_text(encoding="utf-8")

    assert prepared.metadata["title"] == "论文题目"
    assert prepared.metadata["abstract-zh"] == "中文摘要第一段。"
    assert prepared.metadata["keywords-zh"] == "本体；大模型"
    assert prepared.metadata["abstract-en"] == "English abstract paragraph."
    assert prepared.metadata["keywords-en"] == "ontology; LLM"
    assert "## 摘要" not in normalized
    assert "## ABSTRACT" not in normalized
    assert "# 论文题目" not in normalized
    assert "## 第1章 绪论" in normalized


def test_validate_abstract_metadata_requires_bilingual_abstracts() -> None:
    try:
        export.validate_abstract_metadata({"abstract-zh": "中文摘要"})
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected missing abstract metadata to fail")

    assert "abstract-en" in message
    assert "keywords-zh" in message
    assert "Run the abstract generation flow first" in message


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


def _write_minimal_generated_docx(path: Path, include_toc: bool = True) -> None:
    doc = Document()
    if include_toc:
        doc.add_paragraph("目  录")
    doc.add_paragraph("第1章 绪论")
    doc.add_paragraph("正文内容")
    doc.save(path)


def _write_generated_docx_with_pandoc_title(path: Path, title: str) -> None:
    doc = Document()
    doc.add_paragraph(title)
    doc.add_paragraph("第1章 绪论")
    doc.add_paragraph("正文内容")
    doc.save(path)


def _all_docx_text(doc: Document) -> str:
    parts = [para.text for para in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    return "\n".join(parts)


def test_postprocess_inserts_guangxi_cover_before_toc(tmp_path: Path) -> None:
    input_docx = tmp_path / "input.docx"
    output_docx = tmp_path / "output.docx"
    _write_minimal_generated_docx(input_docx)
    profile = export.PROFILES["guangxi-undergrad"]
    assert profile.cover_docx is not None

    postprocess(
        input_docx=input_docx,
        output_docx=output_docx,
        profile=profile.id,
        cover_docx=profile.cover_docx,
        cover_fields={
            "title": "LLM 时代企业知识基础设施研究",
            "college": "管理学院",
            "major": "信息管理",
            "class-name": "信管 2201",
            "student-id": "20260001",
            "author": "张三",
            "advisor": "李老师",
            "date": "二〇二六年六月",
        },
    )

    doc = Document(str(output_docx))
    paragraph_texts = [para.text for para in doc.paragraphs]
    assert paragraph_texts.index("本科毕业论文") < paragraph_texts.index("目  录")

    all_text = _all_docx_text(doc)
    assert "LLM 时代企业知识基础设施研究" in all_text
    assert "管理学院" in all_text
    assert "20260001" in all_text
    assert "二〇二六年六月" in all_text


def test_postprocess_inserts_abstract_pages_between_cover_and_toc(tmp_path: Path) -> None:
    input_docx = tmp_path / "input.docx"
    output_docx = tmp_path / "output.docx"
    _write_generated_docx_with_pandoc_title(input_docx, "封面标题")
    profile = export.PROFILES["guangxi-undergrad"]
    assert profile.cover_docx is not None

    postprocess(
        input_docx=input_docx,
        output_docx=output_docx,
        profile=profile.id,
        cover_docx=profile.cover_docx,
        cover_fields={"title": "封面标题"},
        abstract_fields={
            "abstract-zh": "中文摘要内容。",
            "keywords-zh": "本体；大模型",
            "abstract-en": "English abstract content.",
            "keywords-en": "ontology; LLM",
        },
    )

    doc = Document(str(output_docx))
    paragraph_texts = [para.text for para in doc.paragraphs]
    assert paragraph_texts.index("本科毕业论文") < paragraph_texts.index("摘要")
    assert paragraph_texts.index("摘要") < paragraph_texts.index("ABSTRACT")
    assert paragraph_texts.index("ABSTRACT") < paragraph_texts.index("目  录")
    assert paragraph_texts.index("目  录") < paragraph_texts.index("第1章 绪论")
    assert "封面标题" not in paragraph_texts
    all_text = _all_docx_text(doc)
    assert "中文摘要内容。" in all_text
    assert "English abstract content." in all_text


def test_postprocess_adds_missing_toc_after_cover(tmp_path: Path) -> None:
    input_docx = tmp_path / "input.docx"
    output_docx = tmp_path / "output.docx"
    _write_minimal_generated_docx(input_docx, include_toc=False)
    profile = export.PROFILES["guangxi-undergrad"]
    assert profile.cover_docx is not None

    postprocess(
        input_docx=input_docx,
        output_docx=output_docx,
        profile=profile.id,
        cover_docx=profile.cover_docx,
        cover_fields={"title": "真实导出无目录场景"},
    )

    doc = Document(str(output_docx))
    paragraph_texts = [para.text for para in doc.paragraphs]
    assert paragraph_texts.index("本科毕业论文") < paragraph_texts.index("目  录")
    assert paragraph_texts.index("目  录") < paragraph_texts.index("第1章 绪论")


def test_postprocess_keeps_missing_cover_fields_blank(tmp_path: Path) -> None:
    input_docx = tmp_path / "input.docx"
    output_docx = tmp_path / "output.docx"
    _write_minimal_generated_docx(input_docx)
    profile = export.PROFILES["guangxi-undergrad"]
    assert profile.cover_docx is not None

    postprocess(
        input_docx=input_docx,
        output_docx=output_docx,
        profile=profile.id,
        cover_docx=profile.cover_docx,
        cover_fields={"title": "只填标题"},
    )

    doc = Document(str(output_docx))
    cover_info = doc.tables[1]
    values_by_label = {row.cells[0].text.strip(): row.cells[1].text for row in cover_info.rows}
    assert values_by_label["专业："] == ""
    assert values_by_label["班级："] == ""
    assert values_by_label["学号："] == ""
    assert values_by_label["姓名："] == ""
    assert values_by_label["指导老师："] == ""


def test_postprocess_without_cover_does_not_insert_guangxi_cover(tmp_path: Path) -> None:
    input_docx = tmp_path / "input.docx"
    output_docx = tmp_path / "output.docx"
    _write_minimal_generated_docx(input_docx)

    postprocess(
        input_docx=input_docx,
        output_docx=output_docx,
        profile="sichuan-grad",
    )

    doc = Document(str(output_docx))
    assert "本科毕业论文" not in _all_docx_text(doc)


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


# ---------------------------------------------------------------------------
# Chapter page break tests
# ---------------------------------------------------------------------------

def _has_page_break_before(para) -> bool:
    pPr = para._element.find(qn("w:pPr"))
    if pPr is None:
        return False
    return pPr.find(qn("w:pageBreakBefore")) is not None


def _has_section_break_before(elem) -> bool:
    pPr = elem.find(qn("w:pPr"))
    if pPr is None:
        return False
    return pPr.find(qn("w:sectPr")) is not None


def test_is_chapter_heading_variants() -> None:
    assert _is_chapter_heading("第1章 绪论")
    assert _is_chapter_heading("第10章 讨论")
    assert _is_chapter_heading("第一章 引言")
    assert _is_chapter_heading("参考文献")
    assert _is_chapter_heading("致  谢")
    assert _is_chapter_heading("致谢")
    assert _is_chapter_heading("附录")
    assert _is_chapter_heading("附录A 调查问卷")


def test_is_chapter_heading_non_matches() -> None:
    assert not _is_chapter_heading("摘要")
    assert not _is_chapter_heading("ABSTRACT")
    assert not _is_chapter_heading("目  录")
    assert not _is_chapter_heading("关键词：本体；大模型")
    assert not _is_chapter_heading("Keywords: ontology; LLM")
    assert not _is_chapter_heading("1.1 背景介绍")
    assert not _is_chapter_heading("")


def test_add_section_breaks_and_page_breaks_first_chapter(tmp_path: Path) -> None:
    doc = Document()
    doc.add_paragraph("目  录")
    p1 = doc.add_paragraph("第1章 绪论")
    doc.add_paragraph("绪论正文")
    p2 = doc.add_paragraph("第2章 文献综述")
    doc.add_paragraph("文献综述正文")

    _add_section_breaks_and_page_breaks(doc)

    # First chapter should have a section break before it
    first_heading = body_paragraph_by_text(doc, "第1章 绪论")
    assert first_heading is not None
    assert not _has_page_break_before(p1), "first chapter must not get pageBreakBefore"

    # There should be a section break paragraph somewhere before first chapter
    body = doc.element.body
    first_chapter_index = None
    for i, elem in enumerate(body):
        if elem.tag == qn("w:p"):
            text = _paragraph_text(elem)
            if text == "第1章 绪论":
                first_chapter_index = i
                break

    assert first_chapter_index is not None and first_chapter_index > 0
    prev = body[first_chapter_index - 1]
    assert _has_section_break_before(prev), "expected section break before first chapter"


def body_paragraph_by_text(doc: Document, text: str):
    """Find first body paragraph in doc by exact text match."""
    body = doc.element.body
    for elem in body:
        if elem.tag == qn("w:p"):
            if _paragraph_text(elem) == text:
                return elem
    return None


def test_add_section_breaks_and_page_breaks_subsequent_chapters(tmp_path: Path) -> None:
    doc = Document()
    doc.add_paragraph("目  录")
    p_ch1 = doc.add_paragraph("第1章 绪论")
    doc.add_paragraph("绪论正文")
    p_ch2 = doc.add_paragraph("第2章 文献综述")
    doc.add_paragraph("文献综述正文")
    p_ch3 = doc.add_paragraph("第3章 研究方法")
    doc.add_paragraph("研究方法正文")

    _add_section_breaks_and_page_breaks(doc)

    assert not _has_page_break_before(p_ch1), "first chapter must not get pageBreakBefore"
    assert _has_page_break_before(p_ch2), "chapter 2 must get pageBreakBefore"
    assert _has_page_break_before(p_ch3), "chapter 3 must get pageBreakBefore"


def test_add_section_breaks_and_page_breaks_references_and_appendix(tmp_path: Path) -> None:
    doc = Document()
    doc.add_paragraph("目  录")
    doc.add_paragraph("第1章 绪论")
    doc.add_paragraph("绪论正文")
    p_ref = doc.add_paragraph("参考文献")
    p_app = doc.add_paragraph("附录A 调查问卷")

    _add_section_breaks_and_page_breaks(doc)

    assert _has_page_break_before(p_ref), "参考文献 must get pageBreakBefore"
    assert _has_page_break_before(p_app), "附录 must get pageBreakBefore"


def test_add_section_breaks_and_page_breaks_no_chapter(tmp_path: Path) -> None:
    doc = Document()
    doc.add_paragraph("摘要")
    doc.add_paragraph("ABSTRACT")
    doc.add_paragraph("正文内容")

    # Must not crash
    _add_section_breaks_and_page_breaks(doc)


def test_add_section_breaks_toc_entries_skipped(tmp_path: Path) -> None:
    doc = Document()
    doc.add_paragraph("目  录")
    # Add a TOC-style paragraph (simulating what Pandoc generates)
    p_toc = doc.add_paragraph("第1章 绪论")
    p_toc.style = doc.styles["Normal"]
    # Override to TOC style
    pPr = p_toc._element.find(qn("w:pPr"))
    if pPr is None:
        pPr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
        p_toc._element.insert(0, pPr)
    pPr.append(parse_xml(f'<w:pStyle {nsdecls("w")} w:val="toc 1"/>'))

    p_ch1 = doc.add_paragraph("第1章 绪论")  # real heading
    doc.add_paragraph("绪论正文")
    p_ch2 = doc.add_paragraph("第2章 文献综述")
    doc.add_paragraph("文献综述正文")

    _add_section_breaks_and_page_breaks(doc)

    # TOC entry should NOT be detected as chapter heading
    assert not _has_page_break_before(p_ch1), "first chapter still no break"
    assert _has_page_break_before(p_ch2), "chapter 2 must get pageBreakBefore"
