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


# Profile-specific settings
PROFILE_HEADER_TEXT: dict[str, str] = {
    "mainland-fallback": "本科毕业论文",
    "guangxi-undergrad": "广西大学本科毕业论文",
    "sichuan-grad": "四川大学硕士学位论文",
}

PROFILE_TOC_TITLE: dict[str, str] = {
    "mainland-fallback": "目录",
    "guangxi-undergrad": "目  录",
    "sichuan-grad": "目  录",
}

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


def _paragraph_xml(text: str, *, align: str | None = None, bold: bool = False, size: int | None = None) -> str:
    ppr_parts: list[str] = []
    rpr_parts: list[str] = []
    if align:
        ppr_parts.append(f'<w:jc w:val="{align}"/>')
    if bold:
        rpr_parts.append("<w:b/>")
    if size:
        rpr_parts.append(f'<w:sz w:val="{size}"/>')
    ppr = f"<w:pPr>{''.join(ppr_parts)}<w:rPr>{''.join(rpr_parts)}</w:rPr></w:pPr>" if ppr_parts or rpr_parts else ""
    rpr = f"<w:rPr>{''.join(rpr_parts)}</w:rPr>" if rpr_parts else ""
    return f'<w:p {nsdecls("w")}>{ppr}<w:r>{rpr}<w:t>{escape(text)}</w:t></w:r></w:p>'


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
    abstract_zh = abstract_fields.get("abstract-zh", "").strip()
    keywords_zh = abstract_fields.get("keywords-zh", "").strip()
    abstract_en = abstract_fields.get("abstract-en", "").strip()
    keywords_en = abstract_fields.get("keywords-en", "").strip()

    chunks: list[str] = [
        _paragraph_xml("摘要", align="center", bold=True, size=32),
    ]
    chunks.extend(_paragraph_xml(paragraph) for paragraph in _split_abstract_paragraphs(abstract_zh))
    chunks.append(_paragraph_xml(f"关键词：{keywords_zh}", bold=True))
    chunks.append(_page_break_xml())
    chunks.append(_paragraph_xml("ABSTRACT", align="center", bold=True, size=32))
    chunks.extend(_paragraph_xml(paragraph) for paragraph in _split_abstract_paragraphs(abstract_en))
    chunks.append(_paragraph_xml(f"Keywords: {keywords_en}", bold=True))
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


def _add_toc(doc: Document, toc_title: str) -> None:
    """Add a TOC field after the heading that matches the TOC title.

    Scans for a paragraph whose text matches the TOC title, inserts
    a TOC field in the next paragraph.
    """
    toc_heading = None
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if re.sub(r"\s+", "", text) == re.sub(r"\s+", "", toc_title):
            toc_heading = para
            break

    if toc_heading is None:
        body_elem = doc.element.body
        insert_idx = 0
        for i, elem in enumerate(body_elem):
            if elem.tag != qn("w:p") or _is_toc_paragraph(elem):
                continue
            texts = elem.findall(".//" + qn("w:t"))
            text = "".join(t.text or "" for t in texts).strip()
            if _is_chapter_heading(text):
                insert_idx = i
                break
        toc_heading_xml = parse_xml(
            f'<w:p {nsdecls("w")}>'
            f'  <w:pPr><w:jc w:val="center"/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:pPr>'
            f'  <w:r><w:rPr><w:b/><w:sz w:val="32"/></w:rPr><w:t>{toc_title}</w:t></w:r>'
            f"</w:p>"
        )
        body_elem.insert(insert_idx, toc_heading_xml)
        toc_element = toc_heading_xml
        parent = body_elem
        idx = insert_idx
    else:
        toc_element = toc_heading._element
        parent = toc_element.getparent()
        idx = list(parent).index(toc_element)

    toc_xml = parse_xml(
        f'<w:p {nsdecls("w")}>'
        f'  <w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        f'  <w:r><w:instrText xml:space="preserve">'
        f"    TOC \\o \"1-3\" \\h \\z \\u "
        f"  </w:instrText></w:r>"
        f'  <w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f'  <w:r><w:t>[请在Word中右键更新目录]</w:t></w:r>'
        f'  <w:r><w:fldChar w:fldCharType="end"/></w:r>'
        f"</w:p>"
    )
    parent.insert(idx + 1, toc_xml)


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

    Section 0 (front matter): Roman page numbers (upperRoman), no header
    Subsequent sections (body): Arabic page numbers (decimal), header
    """
    sections = doc.sections
    for i, section in enumerate(sections):
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

        # Set page number format via section properties
        _set_section_page_number_format(
            section._sectPr,
            "upperRoman" if i == 0 else "decimal",
        )

        if i == 0:
            # Front matter: Roman page numbers, no header
            _add_page_number_footer(section, is_roman=True)
            for p in section.header.paragraphs:
                p.clear()
        else:
            # Body: header + Arabic page numbers
            _add_header_to_section(section, header_text, title)
            _add_page_number_footer(section, is_roman=False)


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
    header_text = PROFILE_HEADER_TEXT.get(profile, "本科毕业论文")
    toc_title = PROFILE_TOC_TITLE.get(profile, "目  录")

    if explicit_title:
        _remove_generated_title_paragraph(doc, explicit_title)

    insert_at = 0

    # 0. Insert selected school cover before generated front matter/body.
    if cover_docx is not None:
        insert_at = _insert_cover(doc, cover_docx, fields)

    # 0b. Insert required Chinese/English abstract pages after the cover.
    if abstract_fields:
        insert_at = _insert_abstract_pages(doc, insert_at, abstract_fields)

    # 1. Add section breaks and chapter page breaks
    _add_section_breaks_and_page_breaks(doc)

    # 2. Format all tables as three-line tables (三线表)
    _format_tables_three_line(doc)

    # 2.2 Format table captions and cell content (font, spacing, indent)
    _format_table_captions_and_content(doc)

    # 2.5 Format figure captions (centered, bold, 10.5pt, spacing)
    _format_figure_captions(doc)

    # 3. Set headers and footers on each section
    _set_section_headers_footers(doc, header_text, title)

    # 4. Add TOC field
    _add_toc(doc, toc_title)

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
