"""Post-process a Pandoc-generated DOCX to add Chinese thesis formatting.

Pandoc's DOCX pipeline cannot produce:
- Different headers on different sections
- Mixed Roman/Arabic page numbering
- Table of contents fields

This script uses python-docx to add these elements after Pandoc generation.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.shared import Cm, Emu, Pt


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


def _add_header_to_section(section, header_text: str, title_text: str) -> None:
    """Add header with university name (left) and title (right), 隶书小四号."""
    header = section.header
    header.is_linked_to_previous = False

    # Clear default paragraphs
    for p in header.paragraphs:
        p.clear()

    # Use a single paragraph with a tab stop for left-right alignment
    para = header.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Add left-aligned text: university name
    run_left = para.add_run(header_text)
    _set_cell_font(run_left, "隶书", Pt(12))  # 小四号 = 12pt

    # Add tab stop at right margin for right-aligned title
    tab_stops = para.paragraph_format.tab_stops
    if tab_stops:
        try:
            tab_stops.add_tab_stop(Cm(14.7), alignment=WD_ALIGN_PARAGRAPH.RIGHT)
        except Exception:
            pass

    run_tab = para.add_run("\t")
    run_right = para.add_run(title_text)
    _set_cell_font(run_right, "隶书", Pt(12))

    # Add bottom border line below header
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

    # PAGE field
    run = para.add_run()
    _set_cell_font(run, "Times New Roman", Pt(10.5))  # 五号 = 10.5pt
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


def _add_toc(doc: Document, toc_title: str) -> None:
    """Add a TOC field after the heading that matches the TOC title.

    Scans for a paragraph whose text matches the TOC title, inserts
    a TOC field in the next paragraph.
    """
    toc_heading = None
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        # Match "目  录" or "目录"
        if re.sub(r"\s+", "", text) == re.sub(r"\s+", "", toc_title):
            toc_heading = para
            break

    if toc_heading is None:
        # No existing TOC heading — add one at the start
        para = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = para.add_run(toc_title)
        run.bold = True
        run.font.size = Pt(16)
        toc_heading = para

    # Add TOC field after the heading
    toc_element = toc_heading._element
    parent = toc_element.getparent()
    idx = list(parent).index(toc_element)

    # Build TOC field XML
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


def _add_section_break(doc: Document) -> None:
    """Add a section break after front matter (before Chapter 1 or first body section).

    The first section in a DOCX already exists. We need to add a section break
    at the transition point from front matter to body.
    """
    body_elem = doc.element.body

    # Find where body content starts: look for "第一章" or "第1章" or "1 " heading
    section_added = False
    paragraphs = list(body_elem)
    for i, elem in enumerate(paragraphs):
        if elem.tag == qn("w:p"):
            texts = elem.findall(".//" + qn("w:t"))
            text = "".join(t.text or "" for t in texts).strip()
            if re.match(r"^第[一二三四五六七八九十]+章", text) or re.match(
                r"^第\d+章", text
            ):
                # Insert section break before this paragraph
                sect_pr = parse_xml(
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
                body_elem.insert(list(body_elem).index(elem), sect_pr)
                section_added = True
                break

    if not section_added:
        # No chapter heading found — add section break before first heading
        for i, elem in enumerate(body_elem):
            if elem.tag == qn("w:p"):
                texts = elem.findall(".//" + qn("w:t"))
                text = "".join(t.text or "" for t in texts).strip()
                if text and any(
                    style == "Heading" and text[0].isdigit()
                    for style in ["Heading"]
                ):
                    sect_pr = parse_xml(
                        f'<w:p {nsdecls("w")}>'
                        f'  <w:pPr><w:sectPr/></w:pPr>'
                        f"</w:p>"
                    )
                    body_elem.insert(list(body_elem).index(elem), sect_pr)
                    section_added = True
                    break

    if not section_added:
        # Fallback: add section break right before the last element
        last = body_elem[-1]
        # If last is sectPr, insert before it
        if last.tag == qn("w:sectPr"):
            sect_pr = parse_xml(
                f'<w:p {nsdecls("w")}>'
                f'  <w:pPr><w:sectPr/></w:pPr>'
                f"</w:p>"
            )
            body_elem.insert(list(body_elem).index(last), sect_pr)


def postprocess(
    input_docx: Path,
    output_docx: Path,
    profile: str,
) -> Path:
    """Add headers, footers, TOC, section breaks to a Chinese thesis DOCX."""
    doc = Document(str(input_docx))
    title = _find_title(doc)
    header_text = PROFILE_HEADER_TEXT.get(profile, "本科毕业论文")
    toc_title = PROFILE_TOC_TITLE.get(profile, "目  录")

    # 1. Add section break between front matter and body
    _add_section_break(doc)

    # 2. Set headers and footers on each section
    sections = doc.sections
    for i, section in enumerate(sections):
        if i == 0:
            # Front matter: no header, Roman page numbers
            _add_page_number_footer(section, is_roman=True)
        else:
            # Body: header + Arabic page numbers
            _add_header_to_section(section, header_text, title)
            _add_page_number_footer(section, is_roman=False)

    # 3. Add TOC field
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
    args = parser.parse_args()

    try:
        result = postprocess(
            input_docx=Path(args.input),
            output_docx=Path(args.output),
            profile=args.profile,
        )
        print(result)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
