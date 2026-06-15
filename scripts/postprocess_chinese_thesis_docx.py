"""Post-process a Pandoc-generated DOCX to add Chinese thesis formatting.

Pandoc's DOCX pipeline cannot produce:
- Different headers on different sections
- Mixed Roman/Arabic page numbering
- Table of contents fields
- Three-line table format (三线表)
- Chapter page breaks

This script uses python-docx to add these elements after Pandoc generation.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from html import escape
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Cm, Pt


# Profile-specific settings — fallback only; primary source is PROFICES from export_chinese_thesis.
PROFILE_HEADER_TEXT: dict[str, str] = {
    "mainland-fallback": "本科毕业论文",
    "guangxi-undergrad": "广西大学本科毕业论文",
    "sichuan-grad": "四川大学硕士学位论文",
}

PROFILE_TOC_TITLE: dict[str, str] = {
    "mainland-fallback": "目　录",
    "guangxi-undergrad": "目　录",
    "sichuan-grad": "目　录",
}

# Import PROFILES lazily so the module can be used standalone.
_PROFILES: dict | None = None


def _get_export_profiles():
    """Lazy import of PROFILES to avoid circular import at module load time."""
    global _PROFILES
    if _PROFILES is None:
        try:
            from scripts.export_chinese_thesis import PROFILES as _p
            _PROFILES = _p
        except ImportError:
            _PROFILES = {}
    return _PROFILES


def _profile_header_text(profile_id: str) -> str:
    """Get header text from the profile object, falling back to the static dict."""
    profiles = _get_export_profiles()
    p = profiles.get(profile_id)
    if p is not None:
        return p.header_text
    return PROFILE_HEADER_TEXT.get(profile_id, "本科毕业论文")


def _profile_toc_title(profile_id: str) -> str:
    """Get TOC title from the profile object, falling back to the static dict."""
    profiles = _get_export_profiles()
    p = profiles.get(profile_id)
    if p is not None:
        return p.toc_title
    return PROFILE_TOC_TITLE.get(profile_id, "目  录")

COVER_FIELD_KEYS: tuple[str, ...] = (
    "title",
    "college",
    "major",
    "class-name",
    "student-id",
    "author",
    "advisor",
    "date",
)

COVER_LABEL_TO_FIELD: dict[str, str] = {
    "课题名称": "title",
    "学院": "college",
    "专业": "major",
    "班级": "class-name",
    "学号": "student-id",
    "姓名": "author",
    "指导老师": "advisor",
    "指导教师": "advisor",
}


def _set_cell_font(run, font_name: str, font_size: Pt) -> None:
    """Set font on a run element."""
    run.font.name = font_name
    run.font.size = font_size
    r = run._element
    rPr = r.find(qn("w:rPr"))
    if rPr is None:
        rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
        r.insert(0, rPr)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")}></w:rFonts>')
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:eastAsia"), font_name)
    rFonts.set(qn("w:ascii"), font_name)
    rFonts.set(qn("w:hAnsi"), font_name)


def _find_title(doc: Document) -> str:
    """Extract paper title from the document."""
    for para in doc.paragraphs:
        text = para.text.strip()
        if text and len(text) > 4:
            return text[:60]
    return "论文题目"


def _set_cell_text(cell, text: str) -> None:
    """Replace a table cell's text while keeping the cell container."""
    cell.text = text


def _normalized_label(text: str) -> str:
    return re.sub(r"[\s:：]+", "", text)


def _fill_cover_doc(cover_doc: Document, cover_fields: dict[str, str]) -> None:
    """Fill known official cover fields without inventing missing values."""
    for table in cover_doc.tables:
        for row in table.rows:
            if len(row.cells) < 2:
                continue
            label = _normalized_label(row.cells[0].text)
            field = COVER_LABEL_TO_FIELD.get(label)
            if field and cover_fields.get(field):
                _set_cell_text(row.cells[1], cover_fields[field])

    date = cover_fields.get("date", "")
    if date:
        for para in reversed(cover_doc.paragraphs):
            text = para.text.strip()
            if not text or re.match(r"^[二〇零一二三四五六七八九十\d]{4}年", text):
                para.text = date
                break


def _body_children_without_section(doc: Document) -> list:
    return [child for child in doc.element.body if child.tag != qn("w:sectPr")]


def _strip_section_properties(element) -> None:
    """Remove copied section references that point to another DOCX package."""
    for sect_pr in list(element.findall(".//" + qn("w:sectPr"))):
        parent = sect_pr.getparent()
        if parent is not None:
            parent.remove(sect_pr)


def _insert_cover(doc: Document, cover_docx: Path, cover_fields: dict[str, str]) -> int:
    """Prepend a filled DOCX cover template before the generated thesis body."""
    cover_doc = Document(str(cover_docx))
    _fill_cover_doc(cover_doc, cover_fields)

    body = doc.element.body
    insert_at = 0
    for element in _body_children_without_section(cover_doc):
        copied = deepcopy(element)
        _strip_section_properties(copied)
        body.insert(insert_at, copied)
        insert_at += 1

    page_break = parse_xml(
        f'<w:p {nsdecls("w")}>'
        f'  <w:r><w:br w:type="page"/></w:r>'
        f"</w:p>"
    )
    body.insert(insert_at, page_break)
    return insert_at + 1


def _run_properties_xml(
    *,
    bold: bool = False,
    size: int | None = None,
    east_asia_font: str = "宋体",
    ascii_font: str = "Times New Roman",
) -> str:
    rpr_parts = [
        f'<w:rFonts w:eastAsia="{east_asia_font}" w:ascii="{ascii_font}" w:hAnsi="{ascii_font}"/>'
    ]
    if bold:
        rpr_parts.append("<w:b/>")
    if size:
        rpr_parts.append(f'<w:sz w:val="{size}"/>')
        rpr_parts.append(f'<w:szCs w:val="{size}"/>')
    return f"<w:rPr>{''.join(rpr_parts)}</w:rPr>"


def _paragraph_xml(
    text: str,
    *,
    align: str | None = None,
    bold: bool = False,
    size: int | None = None,
    east_asia_font: str = "宋体",
    ascii_font: str = "Times New Roman",
    before: int | None = None,
    after: int | None = None,
    first_line_chars: int | None = None,
    outline_lvl: int | None = None,
) -> str:
    ppr_parts: list[str] = []
    spacing_attrs = ['w:line="400"', 'w:lineRule="exact"']
    if before is not None:
        spacing_attrs.append(f'w:before="{before}"')
    if after is not None:
        spacing_attrs.append(f'w:after="{after}"')
    ppr_parts.append(f"<w:spacing {' '.join(spacing_attrs)}/>")
    if first_line_chars is not None:
        ppr_parts.append(f'<w:ind w:firstLineChars="{first_line_chars}"/>')
    if align:
        ppr_parts.append(f'<w:jc w:val="{align}"/>')
    if outline_lvl is not None:
        ppr_parts.append(f'<w:outlineLvl w:val="{outline_lvl}"/>')
    rpr = _run_properties_xml(
        bold=bold,
        size=size,
        east_asia_font=east_asia_font,
        ascii_font=ascii_font,
    )
    ppr = f"<w:pPr>{''.join(ppr_parts)}{rpr}</w:pPr>" if ppr_parts or rpr else ""
    return f'<w:p {nsdecls("w")}>{ppr}<w:r>{rpr}<w:t>{escape(text)}</w:t></w:r></w:p>'


def _blank_line_xml() -> str:
    return (
        f'<w:p {nsdecls("w")}>'
        f'  <w:pPr><w:spacing w:line="400" w:lineRule="exact"/></w:pPr>'
        f"</w:p>"
    )


def _strip_trailing_punctuation(text: str) -> str:
    return text.strip().rstrip("；;，,。.")


def _capitalize_english_keywords(text: str) -> str:
    terms = []
    for term in re.split(r"\s*;\s*", _strip_trailing_punctuation(text)):
        term = term.strip()
        if not term:
            continue
        terms.append(term[:1].upper() + term[1:])
    return "; ".join(terms)


def _capitalize_english_title(text: str) -> str:
    words = []
    for word in text.split():
        words.append(word if word.isupper() else word[:1].upper() + word[1:])
    return " ".join(words)


def _keyword_paragraph_xml(
    label: str,
    terms: str,
    *,
    label_east_asia_font: str,
    term_east_asia_font: str,
    ascii_font: str = "Times New Roman",
    first_line_chars: int | None = None,
) -> str:
    ppr_parts = ['<w:spacing w:line="400" w:lineRule="exact"/>']
    if first_line_chars is not None:
        ppr_parts.append(f'<w:ind w:firstLineChars="{first_line_chars}"/>')
    label_rpr = _run_properties_xml(
        bold=True,
        size=24,
        east_asia_font=label_east_asia_font,
        ascii_font=ascii_font,
    )
    term_rpr = _run_properties_xml(
        bold=False,
        size=24,
        east_asia_font=term_east_asia_font,
        ascii_font=ascii_font,
    )
    return (
        f'<w:p {nsdecls("w")}>'
        f'  <w:pPr>{"".join(ppr_parts)}{term_rpr}</w:pPr>'
        f'  <w:r>{label_rpr}<w:t>{escape(label)}</w:t></w:r>'
        f'  <w:r>{term_rpr}<w:t>{escape(terms)}</w:t></w:r>'
        f"</w:p>"
    )


def _page_break_xml() -> str:
    return f'<w:p {nsdecls("w")}><w:r><w:br w:type="page"/></w:r></w:p>'


def _insert_xml_elements(doc: Document, insert_at: int, xml_chunks: list[str]) -> int:
    body = doc.element.body
    for chunk in xml_chunks:
        body.insert(insert_at, parse_xml(chunk))
        insert_at += 1
    return insert_at


def _split_abstract_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def _insert_abstract_pages(doc: Document, insert_at: int, abstract_fields: dict[str, str]) -> int:
    """Insert Chinese and English abstract pages after the cover."""
    title_en = abstract_fields.get("title-en", "").strip()
    abstract_zh = abstract_fields.get("abstract-zh", "").strip()
    keywords_zh = _strip_trailing_punctuation(abstract_fields.get("keywords-zh", ""))
    abstract_en = abstract_fields.get("abstract-en", "").strip()
    keywords_en = _capitalize_english_keywords(abstract_fields.get("keywords-en", ""))

    chunks: list[str] = [
        _blank_line_xml(),
        _paragraph_xml("摘　要", align="center", bold=True, size=32, east_asia_font="黑体", outline_lvl=1),
        _blank_line_xml(),
    ]
    chunks.extend(
        _paragraph_xml(paragraph, first_line_chars=200)
        for paragraph in _split_abstract_paragraphs(abstract_zh)
    )
    chunks.append(_blank_line_xml())
    chunks.append(
        _keyword_paragraph_xml(
            "关键词：",
            keywords_zh,
            label_east_asia_font="黑体",
            term_east_asia_font="宋体",
            first_line_chars=200,
        )
    )
    chunks.append(_page_break_xml())
    if title_en:
        chunks.append(
            _paragraph_xml(
                _capitalize_english_title(title_en),
                align="center",
                size=32,
                east_asia_font="Times New Roman",
                ascii_font="Times New Roman",
            )
        )
        chunks.append(_blank_line_xml())
    chunks.append(
        _paragraph_xml(
            "ABSTRACT",
            align="center",
            bold=True,
            size=32,
            east_asia_font="Times New Roman",
            ascii_font="Times New Roman",
            outline_lvl=1,
        )
    )
    chunks.append(_blank_line_xml())
    chunks.extend(
        _paragraph_xml(
            paragraph,
            first_line_chars=400,
            east_asia_font="Times New Roman",
            ascii_font="Times New Roman",
        )
        for paragraph in _split_abstract_paragraphs(abstract_en)
    )
    chunks.append(_blank_line_xml())
    chunks.append(
        _keyword_paragraph_xml(
            "Keywords: ",
            keywords_en,
            label_east_asia_font="Times New Roman",
            term_east_asia_font="Times New Roman",
            ascii_font="Times New Roman",
        )
    )
    chunks.append(_page_break_xml())
    return _insert_xml_elements(doc, insert_at, chunks)


def _is_cover_metadata_table(table) -> bool:
    labels = {_normalized_label(cell.text) for row in table.rows for cell in row.cells}
    return bool({"课题名称", "学院", "专业", "班级", "学号", "姓名", "指导老师"} & labels)


def _paragraph_text(element) -> str:
    texts = element.findall(".//" + qn("w:t"))
    return "".join(t.text or "" for t in texts).strip()


def _remove_generated_title_paragraph(doc: Document, title: str) -> None:
    """Remove Pandoc's generated metadata title paragraph from the body."""
    if not title:
        return
    body = doc.element.body
    for elem in list(body):
        if elem.tag != qn("w:p"):
            continue
        text = _paragraph_text(elem)
        if not text:
            continue
        if text == title:
            body.remove(elem)
        return


def _add_header_to_section(section, header_text: str, title_text: str) -> None:
    """Add header with university name (left) and title (right), 隶书小四号."""
    header = section.header
    header.is_linked_to_previous = False

    for p in header.paragraphs:
        p.clear()

    para = header.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    run_left = para.add_run(header_text)
    _set_cell_font(run_left, "隶书", Pt(12))

    tab_stops = para.paragraph_format.tab_stops
    if tab_stops:
        try:
            tab_stops.add_tab_stop(Cm(14.7), alignment=WD_ALIGN_PARAGRAPH.RIGHT)
        except Exception:
            pass

    run_tab = para.add_run("\t")
    run_right = para.add_run(title_text)
    _set_cell_font(run_right, "隶书", Pt(12))

    pPr = para._element.find(qn("w:pPr"))
    if pPr is None:
        pPr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
        para._element.insert(0, pPr)
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="12" w:space="1" w:color="000000"/>'
        f"</w:pBdr>"
    )
    pPr.append(pBdr)


def _add_page_number_footer(section, is_roman: bool = True) -> None:
    """Add page number footer: Times New Roman, centered."""
    footer = section.footer
    footer.is_linked_to_previous = False

    for p in footer.paragraphs:
        p.clear()

    para = footer.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = para.add_run()
    _set_cell_font(run, "Times New Roman", Pt(10.5))
    fld_char_begin = parse_xml(
        f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>'
    )
    run._element.append(fld_char_begin)

    run2 = para.add_run()
    _set_cell_font(run2, "Times New Roman", Pt(10.5))
    instr = ""
    if is_roman:
        instr = 'PAGE  \\* ROMAN'
    else:
        instr = "PAGE"
    instr_text = parse_xml(
        f'<w:instrText {nsdecls("w")} xml:space="preserve">{instr}</w:instrText>'
    )
    run2._element.append(instr_text)

    run3 = para.add_run()
    _set_cell_font(run3, "Times New Roman", Pt(10.5))
    fld_char_end = parse_xml(
        f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>'
    )
    run3._element.append(fld_char_end)


def _is_figure_table(table) -> bool:
    """Check if a table is a Pandoc figure-fallback table."""
    tbl = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        return False
    tblStyle = tblPr.find(qn("w:tblStyle"))
    if tblStyle is None:
        return False
    return tblStyle.get(qn("w:val")) == "FigureTable"


def _format_tables_three_line(doc: Document) -> None:
    """Format all tables as 三线表 (three-line table).

    三线表 rules:
    - Top border: thick (1.5 pt, sz=24)
    - Bottom border: thick (1.5 pt, sz=24)
    - Header row bottom border: thin (0.5 pt, sz=6)
    - No left, right, inside vertical, or inside horizontal borders
    - Header row: bold
    """
    for table in doc.tables:
        if _is_cover_metadata_table(table) or _is_figure_table(table):
            continue
        if not table.rows:
            continue

        tbl = table._tbl
        tblPr = tbl.find(qn("w:tblPr"))
        if tblPr is None:
            tblPr = parse_xml(f'<w:tblPr {nsdecls("w")}></w:tblPr>')
            tbl.insert(0, tblPr)

        # Remove existing borders element if any
        existing_borders = tblPr.find(qn("w:tblBorders"))
        if existing_borders is not None:
            tblPr.remove(existing_borders)

        # Build three-line borders
        borders_xml = (
            f'<w:tblBorders {nsdecls("w")}>'
            f'  <w:top w:val="single" w:sz="24" w:space="0" w:color="000000"/>'
            f'  <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'  <w:bottom w:val="single" w:sz="24" w:space="0" w:color="000000"/>'
            f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'  <w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'  <w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(parse_xml(borders_xml))

        # Set table width to 100% of page
        tblW = tblPr.find(qn("w:tblW"))
        if tblW is None:
            tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>')
            tblPr.append(tblW)
        else:
            tblW.set(qn("w:w"), "5000")
            tblW.set(qn("w:type"), "pct")

        # Add bottom border to header row (first row) — thin line
        if len(table.rows) > 1:
            first_row = table.rows[0]
            for cell in first_row.cells:
                tc = cell._tc
                tcPr = tc.find(qn("w:tcPr"))
                if tcPr is None:
                    tcPr = parse_xml(f'<w:tcPr {nsdecls("w")}></w:tcPr>')
                    tc.insert(0, tcPr)

                # Remove existing cell borders
                existing = tcPr.find(qn("w:tcBorders"))
                if existing is not None:
                    tcPr.remove(existing)

                cell_borders = parse_xml(
                    f'<w:tcBorders {nsdecls("w")}>'
                    f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                    f'</w:tcBorders>'
                )
                tcPr.append(cell_borders)

            # Bold header row
            for cell in first_row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.bold = True


def _format_table_caption_paragraph(caption_elem) -> None:
    """Apply Guangxi University formatting to a table caption paragraph."""
    cap_pPr = caption_elem.find(qn("w:pPr"))
    if cap_pPr is None:
        cap_pPr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
        caption_elem.insert(0, cap_pPr)

    # Center alignment
    if cap_pPr.find(qn("w:jc")) is None:
        cap_pPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))

    # Fixed 20 pt line spacing (400 twips)
    spacing = cap_pPr.find(qn("w:spacing"))
    if spacing is None:
        cap_pPr.append(
            parse_xml(f'<w:spacing {nsdecls("w")} w:line="400" w:lineRule="exact"/>')
        )
    else:
        spacing.set(qn("w:line"), "400")
        spacing.set(qn("w:lineRule"), "exact")

    # Bold + 五号 (10.5pt = 21 half-pts) on all runs
    for run in caption_elem.findall(qn("w:r")):
        rPr = run.find(qn("w:rPr"))
        if rPr is None:
            rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
            run.insert(0, rPr)
        if rPr.find(qn("w:b")) is None:
            rPr.append(parse_xml(f'<w:b {nsdecls("w")}/>'))
        sz = rPr.find(qn("w:sz"))
        if sz is None:
            rPr.append(parse_xml(f'<w:sz {nsdecls("w")} w:val="21"/>'))
        szCs = rPr.find(qn("w:szCs"))
        if szCs is None:
            rPr.append(parse_xml(f'<w:szCs {nsdecls("w")} w:val="21"/>'))


def _format_table_cell_content(table) -> None:
    """Set table cell font, line spacing, and remove first-line indent."""
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                pPr = para._element.find(qn("w:pPr"))
                if pPr is not None:
                    # Remove first-line indent
                    ind = pPr.find(qn("w:ind"))
                    if ind is not None:
                        ind.set(qn("w:firstLineChars"), "0")
                        ind.set(qn("w:firstLine"), "0")
                    # Fixed 20 pt line spacing
                    spacing = pPr.find(qn("w:spacing"))
                    if spacing is None:
                        pPr.append(
                            parse_xml(f'<w:spacing {nsdecls("w")} w:line="400" w:lineRule="exact"/>')
                        )
                    else:
                        spacing.set(qn("w:line"), "400")
                        spacing.set(qn("w:lineRule"), "exact")

                # Set font on all runs
                for run in para.runs:
                    _set_cell_font(run, "宋体", Pt(10.5))


def _format_table_captions_and_content(doc: Document) -> None:
    """Format table captions and cell content per Guangxi University requirements.

    - Caption above table, centered, 五号 (10.5pt) bold, fixed 20 pt line spacing
    - One blank line before caption and after table
    - Table content: 五号 (10.5pt) 宋体, no first-line indent
    """
    body = doc.element.body
    children = list(body)

    # Collect (caption_idx, table_idx) pairs for captioned tables
    pairs: list[tuple[int, int]] = []
    i = 0
    while i < len(children):
        elem = children[i]
        if elem.tag == qn("w:p"):
            pPr = elem.find(qn("w:pPr"))
            if pPr is not None:
                pStyle = pPr.find(qn("w:pStyle"))
                if pStyle is not None and pStyle.get(qn("w:val")) == "TableCaption":
                    if i + 1 < len(children) and children[i + 1].tag == qn("w:tbl"):
                        pairs.append((i, i + 1))
                        i += 2
                        continue
        i += 1

    # Format cell content for all non-excluded tables
    for table in doc.tables:
        if _is_cover_metadata_table(table):
            continue
        _format_table_cell_content(table)

    if not pairs:
        return

    # Process captions in reverse order
    blank = parse_xml(
        f'<w:p {nsdecls("w")}>'
        f'  <w:pPr><w:spacing w:line="400" w:lineRule="exact"/></w:pPr>'
        f"</w:p>"
    )
    for cap_idx, tbl_idx in reversed(pairs):
        caption_elem = children[cap_idx]
        _format_table_caption_paragraph(caption_elem)

        # Insert blank before caption
        body.insert(cap_idx, deepcopy(blank))
        # Insert blank after table (tbl_idx+1 because cap_idx insert shifted tbl_idx by 1)
        body.insert(tbl_idx + 1, deepcopy(blank))


def _format_figure_captions(doc: Document) -> None:
    """Format figure captions per university requirements.

    - Caption below the figure, centered, 五号 (10.5pt) bold, fixed 20 pt line spacing
    - One blank line before the figure and after the caption

    Pandoc generates figures as CaptionedFigure + ImageCaption paragraph pairs.
    """
    body = doc.element.body
    children = list(body)

    pairs: list[tuple[int, int]] = []
    i = 0
    while i < len(children):
        elem = children[i]
        if elem.tag != qn("w:p"):
            i += 1
            continue
        pPr = elem.find(qn("w:pPr"))
        if pPr is not None:
            pStyle = pPr.find(qn("w:pStyle"))
            if pStyle is not None and pStyle.get(qn("w:val")) == "CaptionedFigure":
                if i + 1 < len(children):
                    next_elem = children[i + 1]
                    if next_elem.tag == qn("w:p"):
                        next_pPr = next_elem.find(qn("w:pPr"))
                        if next_pPr is not None:
                            next_pStyle = next_pPr.find(qn("w:pStyle"))
                            if next_pStyle is not None and next_pStyle.get(qn("w:val")) == "ImageCaption":
                                pairs.append((i, i + 1))
                                i += 2
                                continue
        i += 1

    if not pairs:
        return

    for fig_idx, cap_idx in reversed(pairs):
        caption_elem = children[cap_idx]
        cap_pPr = caption_elem.find(qn("w:pPr"))
        if cap_pPr is None:
            cap_pPr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
            caption_elem.insert(0, cap_pPr)
        if cap_pPr.find(qn("w:jc")) is None:
            cap_pPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
        spacing = cap_pPr.find(qn("w:spacing"))
        if spacing is None:
            cap_pPr.append(parse_xml(f'<w:spacing {nsdecls("w")} w:line="400" w:lineRule="exact"/>'))
        else:
            spacing.set(qn("w:line"), "400")
            spacing.set(qn("w:lineRule"), "exact")
        for run in caption_elem.findall(qn("w:r")):
            rPr = run.find(qn("w:rPr"))
            if rPr is None:
                rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
                run.insert(0, rPr)
            if rPr.find(qn("w:b")) is None:
                rPr.append(parse_xml(f'<w:b {nsdecls("w")}/>'))
            sz = rPr.find(qn("w:sz"))
            if sz is None:
                sz = parse_xml(f'<w:sz {nsdecls("w")} w:val="21"/>')
                rPr.append(sz)
            szCs = rPr.find(qn("w:szCs"))
            if szCs is None:
                szCs = parse_xml(f'<w:szCs {nsdecls("w")} w:val="21"/>')
                rPr.append(szCs)
        blank = (
            f'<w:p {nsdecls("w")}>'
            f'  <w:pPr><w:spacing w:line="400" w:lineRule="exact"/></w:pPr>'
            f"</w:p>"
        )
        body.insert(cap_idx + 1, parse_xml(blank))
        body.insert(fig_idx, parse_xml(blank))


def _format_equation_numbers(doc: Document) -> None:
    """Add sequential equation numbers at the right margin for display equations.

    Pandoc converts $$...$$ to w:p containing m:oMathPara. This function adds
    right-aligned equation numbers on the same line via a right tab stop.
    """
    body = doc.element.body

    # Read page dimensions from the first sectPr
    sectPr = body.find(qn("w:sectPr"))
    if sectPr is None:
        return

    pgSz = sectPr.find(qn("w:pgSz"))
    pgMar = sectPr.find(qn("w:pgMar"))

    page_width = 11906  # A4 default in twips
    left_margin = 1701  # ~3cm default
    right_margin = 1701

    if pgSz is not None:
        w = pgSz.get(qn("w:w"))
        if w is not None:
            page_width = int(w)
    if pgMar is not None:
        left = pgMar.get(qn("w:left"))
        right = pgMar.get(qn("w:right"))
        if left is not None:
            left_margin = int(left)
        if right is not None:
            right_margin = int(right)

    right_tab_pos = page_width - right_margin
    if right_tab_pos <= left_margin:
        right_tab_pos = 9638  # sensible fallback

    eq_counter = 0

    for elem in body:
        if elem.tag != qn("w:p"):
            continue
        omath_para = elem.find(qn("m:oMathPara"))
        if omath_para is None:
            continue

        eq_counter += 1

        # Add right-aligned tab stop in paragraph properties
        pPr = elem.find(qn("w:pPr"))
        if pPr is None:
            pPr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
            elem.insert(0, pPr)

        tabs = pPr.find(qn("w:tabs"))
        if tabs is None:
            tabs = parse_xml(f'<w:tabs {nsdecls("w")}></w:tabs>')
            pPr.append(tabs)
        tabs.append(parse_xml(
            f'<w:tab {nsdecls("w")} w:val="right" w:pos="{right_tab_pos}"/>'
        ))

        # Ensure fixed 20pt line spacing
        spacing = pPr.find(qn("w:spacing"))
        if spacing is None:
            pPr.append(parse_xml(
                f'<w:spacing {nsdecls("w")} w:line="400" w:lineRule="exact"/>'
            ))
        else:
            spacing.set(qn("w:line"), "400")
            spacing.set(qn("w:lineRule"), "exact")

        # Insert tab character + equation number after oMathPara
        num_text = f"({eq_counter})"
        run_xml = (
            f'<w:r {nsdecls("w")}>'
            f'  <w:rPr>'
            f'    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
            f'    <w:sz w:val="21"/>'
            f'    <w:szCs w:val="21"/>'
            f'  </w:rPr>'
            f'  <w:tab/>'
            f'  <w:t xml:space="preserve">{num_text}</w:t>'
            f'</w:r>'
        )
        omath_para.addnext(parse_xml(run_xml))


def _add_toc(doc: Document, toc_title: str) -> None:
    """Add a TOC field after the heading that matches the TOC title.

    Inserts the TOC before the front-matter-to-body section break so that
    the section break properly starts Chapter 1 on a new page.
    TOC field shows only Level 1 and Level 2 (backslash o "1-2").
    """
    body_elem = doc.element.body
    children = list(body_elem)

    # Find existing TOC heading in document
    toc_heading = None
    for para in doc.paragraphs:
        text = para.text.strip()
        if re.sub(r"\s+", "", text) == re.sub(r"\s+", "", toc_title):
            toc_heading = para
            break

    # Find the section-break paragraph that separates front matter from body
    sect_break_idx = None
    for i, elem in enumerate(children):
        if elem.tag != qn("w:p"):
            continue
        pPr = elem.find(qn("w:pPr"))
        if pPr is not None and pPr.find(qn("w:sectPr")) is not None:
            sect_break_idx = i
            break

    # Find first chapter heading (fallback for insert position)
    first_chap_idx = None
    for i, elem in enumerate(children):
        if elem.tag != qn("w:p") or _is_toc_paragraph(elem):
            continue
        texts = elem.findall(".//" + qn("w:t"))
        text = "".join(t.text or "" for t in texts).strip()
        if _is_chapter_heading(text):
            first_chap_idx = i
            break

    if toc_heading is not None:
        # Existing heading — insert TOC field after it, ensure break after
        toc_element = toc_heading._element
        parent = toc_element.getparent()
        idx = list(parent).index(toc_element)
    else:
        # Insert TOC heading before the section break (or before first chapter)
        insert_at = sect_break_idx if sect_break_idx is not None else (first_chap_idx or 0)

        # Blank line before
        body_elem.insert(insert_at, parse_xml(_blank_line_xml()))
        insert_at += 1

        # TOC heading: 黑体 三号(32pt), centered, blank line after in spacing
        heading_xml = parse_xml(
            f'<w:p {nsdecls("w")}>'
            f'  <w:pPr>'
            f'    <w:jc w:val="center"/>'
            f'    <w:spacing w:before="400" w:after="400" w:line="400" w:lineRule="exact"/>'
            f'    <w:rPr><w:rFonts w:eastAsia="黑体" w:ascii="黑体" w:hAnsi="黑体"/>'
            f'      <w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>'
            f'  </w:pPr>'
            f'  <w:r><w:rPr><w:rFonts w:eastAsia="黑体" w:ascii="黑体" w:hAnsi="黑体"/>'
            f'      <w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>'
            f'    <w:t>{toc_title}</w:t></w:r>'
            f"</w:p>"
        )
        body_elem.insert(insert_at, heading_xml)
        toc_element = heading_xml
        parent = body_elem
        idx = insert_at

    # TOC field paragraph (level 1-2 only)
    toc_xml = parse_xml(
        f'<w:p {nsdecls("w")}>'
        f'  <w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        f'  <w:r><w:instrText xml:space="preserve">'
        f"    TOC \\o \"1-2\" \\h \\z \\u "
        f"  </w:instrText></w:r>"
        f'  <w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f'  <w:r><w:t>[请在Word中右键更新目录]</w:t></w:r>'
        f'  <w:r><w:fldChar w:fldCharType="end"/></w:r>'
        f"</w:p>"
    )
    parent.insert(idx + 1, toc_xml)

    # Ensure first chapter has pageBreakBefore (covers the case where TOC was
    # inserted between the section break and the first chapter heading)
    if first_chap_idx is not None:
        first_chap_elem = children[first_chap_idx]
        pPr = first_chap_elem.find(qn("w:pPr"))
        if pPr is None:
            pPr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
            first_chap_elem.insert(0, pPr)
        if pPr.find(qn("w:pageBreakBefore")) is None:
            pPr.append(parse_xml(f'<w:pageBreakBefore {nsdecls("w")}/>'))


def _format_toc_entries(doc: Document) -> None:
    """Add 'toc 1' and 'toc 2' styles so Word generates correctly-formatted TOC entries.

    When the user updates the TOC field in Word, entries use these styles.
    宋体 小四(12pt), left-aligned, no indent, fixed 20pt line spacing.
    """
    TOC_STYLE_XML = {
        "toc1": (
            f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="toc1">'
            f'  <w:name w:val="toc 1"/>'
            f'  <w:basedOn w:val="Normal"/>'
            f'  <w:pPr>'
            f'    <w:jc w:val="left"/>'
            f'    <w:spacing w:line="400" w:lineRule="exact"/>'
            f'  </w:pPr>'
            f'  <w:rPr>'
            f'    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"'
            f'               w:eastAsia="宋体"/>'
            f'    <w:sz w:val="24"/><w:szCs w:val="24"/>'
            f'  </w:rPr>'
            f'</w:style>'
        ),
        "toc2": (
            f'<w:style {nsdecls("w")} w:type="paragraph" w:styleId="toc2">'
            f'  <w:name w:val="toc 2"/>'
            f'  <w:basedOn w:val="Normal"/>'
            f'  <w:pPr>'
            f'    <w:jc w:val="left"/>'
            f'    <w:spacing w:line="400" w:lineRule="exact"/>'
            f'  </w:pPr>'
            f'  <w:rPr>'
            f'    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"'
            f'               w:eastAsia="宋体"/>'
            f'    <w:sz w:val="24"/><w:szCs w:val="24"/>'
            f'  </w:rPr>'
            f'</w:style>'
        ),
    }
    styles_elem = doc.styles.element
    existing_ids = {s.get(qn("w:styleId")) for s in styles_elem}
    for sid, xml in TOC_STYLE_XML.items():
        if sid not in existing_ids:
            styles_elem.append(parse_xml(xml))

    # Also format any existing TOC entry paragraphs (if Pandoc pre-generated them)
    TOC_STYLES = {"toc 1", "toc 2", "toc 3"}
    for para in doc.paragraphs:
        pPr = para._element.find(qn("w:pPr"))
        if pPr is None:
            continue
        pStyle = pPr.find(qn("w:pStyle"))
        if pStyle is None:
            continue
        style = pStyle.get(qn("w:val"))
        if style not in TOC_STYLES:
            continue
        _set_para_alignment(pPr, "left")
        ind = pPr.find(qn("w:ind"))
        if ind is not None:
            pPr.remove(ind)
        for run in para.runs:
            _set_run_font(run, east_asia="宋体", ascii="Times New Roman",
                          sz="24", bold=False)
        _set_para_line_spacing_fixed_20pt(pPr)


def _format_bibliography_entries(doc: Document) -> None:
    """Format Bibliography entries: 宋体 小四(12pt), fixed line spacing."""
    for para in doc.paragraphs:
        pPr = para._element.find(qn("w:pPr"))
        if pPr is None:
            continue
        pStyle = pPr.find(qn("w:pStyle"))
        if pStyle is None:
            continue
        if pStyle.get(qn("w:val")) != "Bibliography":
            continue
        for run in para.runs:
            _set_run_font(run, east_asia="宋体", ascii="Times New Roman",
                          sz="24", bold=False)
        _set_para_line_spacing_fixed_20pt(pPr)


def _reorder_bibliography_before_thanks(doc: Document) -> None:
    """Move Bibliography paragraphs after 致谢 to before 致谢.

    Pandoc citeproc places the reference list at the document end by default.
    This function moves Bibliography-styled paragraphs to before the 致谢
    heading (which should follow 参考文献 in the input markdown).
    """
    body = doc.element.body
    children = list(body)

    refs_heading_idx = None
    thanks_heading_idx = None
    for i, elem in enumerate(children):
        if elem.tag != qn("w:p"):
            continue
        pPr = elem.find(qn("w:pPr"))
        if pPr is None:
            continue
        pStyle = pPr.find(qn("w:pStyle"))
        if pStyle is None:
            continue
        style = pStyle.get(qn("w:val"))
        text = "".join(
            t.text or "" for t in elem.findall(".//" + qn("w:t"))
        ).strip()
        if style == "Heading1":
            if re.sub(r"\s+", "", text) == "参考文献":
                refs_heading_idx = i
            elif re.sub(r"\s+", "", text) == "致谢":
                thanks_heading_idx = i

    if refs_heading_idx is None or thanks_heading_idx is None:
        return  # nothing to reorder

    # Collect Bibliography paragraphs that are AFTER 致谢
    bib_elems = []
    for elem in children[thanks_heading_idx:]:
        if elem.tag != qn("w:p"):
            continue
        pPr = elem.find(qn("w:pPr"))
        if pPr is None:
            continue
        pStyle = pPr.find(qn("w:pStyle"))
        if pStyle is None:
            continue
        if pStyle.get(qn("w:val")) == "Bibliography":
            bib_elems.append(elem)

    if not bib_elems:
        return

    # Move each Bibliography element to just before 致谢 heading
    for elem in bib_elems:
        body.remove(elem)
        body.insert(children.index(children[thanks_heading_idx]), elem)


def _format_headings_and_body(doc: Document) -> None:
    """Format headings and body paragraphs per Guangxi heading hierarchy.

    Level 1 (Heading1 / 第一章): 黑体 小二(18pt), centered, one blank line before/after
    Level 2 (Heading2 / 1.1):     黑体 小三(15pt), left-aligned, no extra space
    Level 3 (Heading3 / 1.1.1):   黑体 四号(14pt), left-aligned, no extra space
    Level 4 (Heading4 / 1.1.1.1): 黑体 小四(12pt), left-aligned, no extra space
    Body (Normal/BodyText/FirstParagraph): 宋体 小四(12pt), fixed 20pt, first-line indent 2 chars
    """
    HEADING_FMT: dict[str, dict[str, str]] = {
        "Heading1": {"sz": "36", "align": "center", "before": "400", "after": "400"},
        "Heading2": {"sz": "30", "align": "left",   "before": "0",   "after": "0"},
        "Heading3": {"sz": "28", "align": "left",   "before": "0",   "after": "0"},
        "Heading4": {"sz": "24", "align": "left",   "before": "0",   "after": "0"},
    }
    BODY_STYLES = {"Normal", "BodyText", "FirstParagraph"}
    EXCLUDED_BODY = {"Bibliography", "toc 1", "toc 2", "toc 3",
                     "Compact", "TableCaption", "ImageCaption",
                     "CaptionedFigure", "toc"}

    for para in doc.paragraphs:
        pPr = para._element.find(qn("w:pPr"))
        if pPr is None:
            continue
        pStyle_elem = pPr.find(qn("w:pStyle"))
        style = pStyle_elem.get(qn("w:val")) if pStyle_elem is not None else ""

        if style in HEADING_FMT:
            # Special headings (参考文献/致谢) use 黑体 三号(16pt), not 小二(18pt)
            clean_text = re.sub(r"\s+", "", para.text.strip())
            if clean_text in ("参考文献", "致谢"):
                _set_para_spacing(pPr, before="400", after="400")
                _set_para_alignment(pPr, "center")
                _set_para_line_spacing_fixed_20pt(pPr)
                for run in para.runs:
                    _set_run_font(run, east_asia="黑体", ascii="黑体",
                                  sz="32", bold=True)
                continue
            fmt = HEADING_FMT[style]
            # --- paragraph properties ---
            _set_para_spacing(pPr, before=fmt["before"], after=fmt["after"])
            _set_para_alignment(pPr, fmt["align"])
            _set_para_line_spacing_fixed_20pt(pPr)
            # --- run properties ---
            for run in para.runs:
                _set_run_font(run, east_asia="黑体", ascii="黑体",
                              sz=fmt["sz"], bold=True)
        elif style in BODY_STYLES:
            if style in EXCLUDED_BODY:
                continue
            _set_para_alignment(pPr, "both")
            _set_para_line_spacing_fixed_20pt(pPr)
            _set_first_line_indent(pPr, chars=2)
            for run in para.runs:
                _set_run_font(run, east_asia="宋体", ascii="Times New Roman",
                              sz="24", bold=False)


def _set_para_spacing(pPr, before: str, after: str) -> None:
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = parse_xml(
            f'<w:spacing {nsdecls("w")} w:before="{before}" w:after="{after}"/>'
        )
        pPr.append(spacing)
    else:
        spacing.set(qn("w:before"), before)
        spacing.set(qn("w:after"), after)


def _set_para_alignment(pPr, align: str) -> None:
    jc = pPr.find(qn("w:jc"))
    if jc is None:
        jc = parse_xml(f'<w:jc {nsdecls("w")} w:val="{align}"/>')
        pPr.append(jc)
    else:
        jc.set(qn("w:val"), align)


def _set_para_line_spacing_fixed_20pt(pPr) -> None:
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = parse_xml(
            f'<w:spacing {nsdecls("w")} w:line="400" w:lineRule="exact"/>'
        )
        pPr.append(spacing)
    else:
        spacing.set(qn("w:line"), "400")
        spacing.set(qn("w:lineRule"), "exact")


def _set_first_line_indent(pPr, chars: int = 2) -> None:
    ind = pPr.find(qn("w:ind"))
    if ind is None:
        ind = parse_xml(
            f'<w:ind {nsdecls("w")} w:firstLineChars="{chars * 100}"/>'
        )
        pPr.append(ind)
    else:
        ind.set(qn("w:firstLineChars"), str(chars * 100))


def _set_run_font(run, east_asia: str, ascii: str, sz: str, bold: bool) -> None:
    rPr = run._element.find(qn("w:rPr"))
    if rPr is None:
        rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
        run._element.insert(0, rPr)
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = parse_xml(
            f'<w:rFonts {nsdecls("w")} '
            f'  w:eastAsia="{east_asia}" w:ascii="{ascii}" w:hAnsi="{ascii}"/>'
        )
        rPr.append(rFonts)
    else:
        rFonts.set(qn("w:eastAsia"), east_asia)
        rFonts.set(qn("w:ascii"), ascii)
        rFonts.set(qn("w:hAnsi"), ascii)
    sz_elem = rPr.find(qn("w:sz"))
    if sz_elem is None:
        sz_elem = parse_xml(f'<w:sz {nsdecls("w")} w:val="{sz}"/>')
        rPr.append(sz_elem)
    else:
        sz_elem.set(qn("w:val"), sz)
    szCs = rPr.find(qn("w:szCs"))
    if szCs is None:
        szCs = parse_xml(f'<w:szCs {nsdecls("w")} w:val="{sz}"/>')
        rPr.append(szCs)
    else:
        szCs.set(qn("w:val"), sz)
    b_elem = rPr.find(qn("w:b"))
    if bold:
        if b_elem is None:
            rPr.append(parse_xml(f'<w:b {nsdecls("w")}/>'))
    else:
        if b_elem is not None:
            rPr.remove(b_elem)


def _is_chapter_heading(text: str) -> bool:
    """Check if paragraph text is a chapter-level heading.

    Matches patterns like:
    - 第1章 / 第N章 / 第一章
    - 参考文献, 致谢, 附录, 附录A

    Whitespace is normalized before matching so that spacing variants
    like "致  谢" are also recognized.
    """
    normalized = re.sub(r"\s+", "", text)
    if re.match(r"^第[一二三四五六七八九十\d]+章", normalized):
        return True
    if normalized.startswith("参考文献"):
        return True
    if normalized.startswith("致谢"):
        return True
    if normalized.startswith("附录"):
        return True
    return False


def _is_toc_paragraph(elem) -> bool:
    """Check if a paragraph element is a TOC entry (not a real heading).

    TOC entries have styles like 'toc 1', 'toc 2', 'toc 3' or 'Compact'.
    """
    pPr = elem.find(qn("w:pPr"))
    if pPr is None:
        return False
    pStyle = pPr.find(qn("w:pStyle"))
    if pStyle is None:
        return False
    style_val = pStyle.get(qn("w:val"), "")
    if style_val.startswith("toc") or style_val == "Compact":
        return True
    return False


def _set_section_page_number_format(sect_pr, fmt: str) -> None:
    """Set page number format on a section's sectPr element."""
    pgNumType = sect_pr.find(qn("w:pgNumType"))
    if pgNumType is not None:
        sect_pr.remove(pgNumType)
    pgNumType = parse_xml(
        f'<w:pgNumType {nsdecls("w")} w:fmt="{fmt}"/>'
    )
    sect_pr.append(pgNumType)


def _add_section_breaks_and_page_breaks(doc: Document) -> None:
    """Add section breaks and page breaks for proper chapter separation.

    Creates a section break before the first chapter heading to separate
    front matter (Roman page numbers, no header) from body (Arabic page
    numbers, header). Adds pageBreakBefore to each subsequent chapter heading.
    Only actual headings are considered — TOC entries are ignored.
    """
    body_elem = doc.element.body
    paragraphs = list(body_elem)

    first_chapter_idx = None
    first_chapter_elem = None

    # Find the first ACTUAL chapter heading (skip TOC entries)
    for i, elem in enumerate(paragraphs):
        if elem.tag != qn("w:p"):
            continue
        if _is_toc_paragraph(elem):
            continue
        texts = elem.findall(".//" + qn("w:t"))
        text = "".join(t.text or "" for t in texts).strip()
        if _is_chapter_heading(text):
            first_chapter_idx = i
            first_chapter_elem = elem
            break

    if first_chapter_elem is None:
        # No chapter heading found — add section break before last sectPr
        last_sect = body_elem.find(qn("w:sectPr"))
        if last_sect is not None:
            sect_para = parse_xml(
                f'<w:p {nsdecls("w")}>'
                f'  <w:pPr><w:sectPr/></w:pPr>'
                f"</w:p>"
            )
            body_elem.insert(list(body_elem).index(last_sect), sect_para)
        return

    # Ensure the first chapter has a section break before it
    prev_elem = paragraphs[first_chapter_idx - 1] if first_chapter_idx > 0 else None

    has_sect_before = False
    if prev_elem is not None and prev_elem.tag == qn("w:p"):
        pPr = prev_elem.find(qn("w:pPr"))
        if pPr is not None and pPr.find(qn("w:sectPr")) is not None:
            has_sect_before = True

    if not has_sect_before:
        sect_para = parse_xml(
            f'<w:p {nsdecls("w")}>'
            f'  <w:pPr>'
            f'    <w:sectPr>'
            f'      <w:pgSz w:w="11906" w:h="16838"/>'
            f'      <w:pgMar w:top="1440" w:bottom="1440"'
            f'              w:left="1440" w:right="1440"/>'
            f'    </w:sectPr>'
            f'  </w:pPr>'
            f"</w:p>"
        )
        body_elem.insert(list(body_elem).index(first_chapter_elem), sect_para)

    # Add pageBreakBefore to subsequent chapters (skip TOC entries)
    chapter_count = 0
    for elem in body_elem:
        if elem.tag != qn("w:p"):
            continue
        if _is_toc_paragraph(elem):
            continue
        texts = elem.findall(".//" + qn("w:t"))
        text = "".join(t.text or "" for t in texts).strip()
        if _is_chapter_heading(text):
            chapter_count += 1
            if chapter_count > 1:
                pPr = elem.find(qn("w:pPr"))
                if pPr is None:
                    pPr = parse_xml(f'<w:pPr {nsdecls("w")}></w:pPr>')
                    elem.insert(0, pPr)
                if pPr.find(qn("w:pageBreakBefore")) is None:
                    pPr.append(
                        parse_xml(f'<w:pageBreakBefore {nsdecls("w")}/>')
                    )


def _set_section_headers_footers(doc: Document, header_text: str, title: str) -> None:
    """Set headers and footers on each section appropriately.

    Section 0 (front matter): no visible page numbers, no header
    Subsequent sections (body): Arabic page numbers starting from 1, header
    """
    sections = doc.sections
    for i, section in enumerate(sections):
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

        if i == 0:
            # Front matter: no visible page numbers, no header
            for p in section.header.paragraphs:
                p.clear()
            for p in section.footer.paragraphs:
                p.clear()
            _set_section_page_number_format(section._sectPr, "upperRoman")
        else:
            # Body: header + Arabic page numbers
            _add_header_to_section(section, header_text, title)
            _add_page_number_footer(section, is_roman=False)
            _set_section_page_number_format(section._sectPr, "decimal")
            # Restart numbering at 1 for the first body section
            if i == 1:
                pgNumType = section._sectPr.find(qn("w:pgNumType"))
                if pgNumType is not None:
                    pgNumType.set(qn("w:start"), "1")


def _auto_number_headings(doc: Document) -> None:
    """Add chapter and multi-level heading numbering to headings.

    Heading1: 第一章, 第二章, ... (Chinese numeral; skip 参考文献/致谢/附录)
    Heading2: 1.1, 1.2, ...
    Heading3: 1.1.1, 1.2.1, ...
    Heading4: 1.1.1.1, ...

    Strips any existing "第N章" or "N.N" prefix before adding fresh numbering.
    """
    CHAPTER_NUMERALS = [
        "零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
        "十一", "十二", "十三", "十四", "十五",
    ]
    EXISTING_CHAP = re.compile(r"^第[一二三四五六七八九十\d]+章\s*")
    EXISTING_SEC = re.compile(r"^(\d+\.)*\d+\s+")
    NO_NUMBER = {"参考文献", "致谢"}

    chap_counter = 0
    # [section, subsection, subsubsection] counters within current chapter
    sec = [0, 0, 0]

    for para in doc.paragraphs:
        pPr = para._element.find(qn("w:pPr"))
        if pPr is None:
            continue
        pStyle_elem = pPr.find(qn("w:pStyle"))
        style = pStyle_elem.get(qn("w:val")) if pStyle_elem is not None else ""
        text = para.text.strip()
        if not text:
            continue

        if style == "Heading1":
            clean = re.sub(r"\s+", "", text)
            clean = EXISTING_CHAP.sub("", clean)
            if clean in NO_NUMBER or clean.startswith("附录"):
                continue
            chap_counter += 1
            sec = [0, 0, 0]
            stripped = EXISTING_CHAP.sub("", text).strip()
            new_text = f"第{CHAPTER_NUMERALS[chap_counter]}章 {stripped}"
            _replace_para_text(para, new_text)

        elif style == "Heading2" and chap_counter > 0:
            sec[0] += 1
            sec[1] = 0
            sec[2] = 0
            stripped = EXISTING_SEC.sub("", text).strip()
            new_text = f"{chap_counter}.{sec[0]} {stripped}"
            _replace_para_text(para, new_text)

        elif style == "Heading3" and chap_counter > 0:
            sec[1] += 1
            sec[2] = 0
            stripped = EXISTING_SEC.sub("", text).strip()
            new_text = f"{chap_counter}.{sec[0]}.{sec[1]} {stripped}"
            _replace_para_text(para, new_text)

        elif style == "Heading4" and chap_counter > 0:
            sec[2] += 1
            stripped = EXISTING_SEC.sub("", text).strip()
            new_text = f"{chap_counter}.{sec[0]}.{sec[1]}.{sec[2]} {stripped}"
            _replace_para_text(para, new_text)


def _replace_para_text(para, new_text: str) -> None:
    """Replace paragraph text, preserving existing runs for formatting."""
    runs = para.runs
    if runs:
        runs[0].text = new_text
        for run in runs[1:]:
            run.text = ""
    else:
        rPr = parse_xml(f'<w:rPr {nsdecls("w")}></w:rPr>')
        run_xml = (
            f'<w:r {nsdecls("w")}>{rPr}'
            f'<w:t xml:space="preserve">{escape(new_text)}</w:t></w:r>'
        )
        para._element.append(parse_xml(run_xml))


def postprocess(
    input_docx: Path,
    output_docx: Path,
    profile: str,
    cover_docx: Path | None = None,
    cover_fields: dict[str, str] | None = None,
    abstract_fields: dict[str, str] | None = None,
) -> Path:
    """Add cover, headers, footers, TOC, section breaks, and table formatting."""
    doc = Document(str(input_docx))
    fields = {key: value for key, value in (cover_fields or {}).items() if value}
    explicit_title = fields.get("title", "")
    title = explicit_title or _find_title(doc)
    fields.setdefault("title", title)
    header_text = _profile_header_text(profile)
    toc_title = _profile_toc_title(profile)

    if explicit_title:
        _remove_generated_title_paragraph(doc, explicit_title)

    insert_at = 0

    # 0. Insert selected school cover before generated front matter/body.
    if cover_docx is not None:
        insert_at = _insert_cover(doc, cover_docx, fields)

    # 0b. Insert required Chinese/English abstract pages after the cover.
    if abstract_fields:
        insert_at = _insert_abstract_pages(doc, insert_at, abstract_fields)

    # 0.5 Add chapter/section numbering (第一章, 1.1, 1.1.1, ...) before section breaks
    _auto_number_headings(doc)

    # 1. Add section breaks and chapter page breaks
    _add_section_breaks_and_page_breaks(doc)

    # 2. Format all tables as three-line tables (三线表)
    _format_tables_three_line(doc)

    # 2.2 Format table captions and cell content (font, spacing, indent)
    _format_table_captions_and_content(doc)

    # 2.5 Format figure captions (centered, bold, 10.5pt, spacing)
    _format_figure_captions(doc)

    # 2.8 Format equation numbers (right-aligned, sequential numbering)
    _format_equation_numbers(doc)

    # 2.9 Format headings (一级/二级/三级/四级) and body text per Guangxi spec
    _format_headings_and_body(doc)

    # 3. Set headers and footers on each section
    _set_section_headers_footers(doc, header_text, title)

    # 4. Add TOC field
    _add_toc(doc, toc_title)

    # 4.5 Format TOC entries (宋体 小四, left-aligned, no indent)
    _format_toc_entries(doc)

    # 4.6 Move Bibliography entries before 致谢 (Pandoc puts refs at document end)
    _reorder_bibliography_before_thanks(doc)

    # 4.7 Format Bibliography entries (宋体 小四)
    _format_bibliography_entries(doc)

    # Save
    output_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_docx))
    return output_docx


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Pandoc-generated DOCX.")
    parser.add_argument("--output", required=True, help="Output DOCX path.")
    parser.add_argument(
        "--profile",
        required=True,
        choices=sorted(PROFILE_HEADER_TEXT),
        help="Chinese thesis formatting profile.",
    )
    parser.add_argument("--cover-docx", help="Optional DOCX cover template to insert.")
    args = parser.parse_args()

    try:
        result = postprocess(
            input_docx=Path(args.input),
            output_docx=Path(args.output),
            profile=args.profile,
            cover_docx=Path(args.cover_docx) if args.cover_docx else None,
        )
        print(result)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
