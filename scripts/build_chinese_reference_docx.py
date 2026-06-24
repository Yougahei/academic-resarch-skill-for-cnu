"""Build Pandoc reference DOCX files for Chinese thesis profiles.

The generated files are style reference documents, not official school
templates. They are used by Pandoc's `--reference-doc` path for DOCX output.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

from scripts.export_chinese_thesis import find_pandoc


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
ET.register_namespace("w", NS["w"])


@dataclass(frozen=True)
class DocxProfile:
    id: str
    filename: str
    title: str
    normal_east_asia: str = "宋体"
    heading_east_asia: str = "黑体"
    latin: str = "Times New Roman"
    # Paper size in hundredths of mm (page width, page height).
    # Default: A4 (210mm × 297mm = 11906 × 16838 twips).
    # 16开: 184mm × 260mm = 10430 × 14740 twips.
    paper_w_twips: int = 11906
    paper_h_twips: int = 16838
    # Margins in hundredths of mm for w:pgMar
    margin_top: int = 2540  # 2.54 cm
    margin_bottom: int = 2540
    margin_left: int = 2540
    margin_right: int = 2540
    margin_header: int = 720
    margin_footer: int = 720


# Convert cm to EMU
def _cm_to_emu(cm: float) -> int:
    return int(cm * 360000)


def _hundredths_mm_to_twips(val: int) -> int:
    """Convert hundredths of mm to twips for OOXML pgMar attributes."""
    return int(val * 1440 / 2540)


PROFILES: dict[str, DocxProfile] = {
    "mainland-fallback": DocxProfile(
        id="mainland-fallback",
        filename="mainland_fallback_reference.docx",
        title="Mainland China University Thesis Fallback Reference DOCX",
        margin_left=2540,
        margin_right=2540,
    ),
    "guangxi-undergrad": DocxProfile(
        id="guangxi-undergrad",
        filename="guangxi_undergrad_reference.docx",
        title="Guangxi University Undergraduate Thesis Reference DOCX",
        # Guangxi spec: top/bottom 2.54 cm, left/right 2.2 cm
        margin_left=2200,   # 2.2 cm in hundredths of mm
        margin_right=2200,  # 2.2 cm
    ),
    "sichuan-grad": DocxProfile(
        id="sichuan-grad",
        filename="sichuan_grad_reference.docx",
        title="Sichuan University Graduate Dissertation Reference DOCX",
        # 16开: 184mm × 260mm
        paper_w_twips=10430,
        paper_h_twips=14740,
        # Spec: top/bottom 2.5 cm, left 2.8 cm, right 2.2 cm
        margin_top=2500,
        margin_bottom=2500,
        margin_left=2800,
        margin_right=2200,
    ),
}


def _w(tag: str) -> str:
    return f"{{{NS['w']}}}{tag}"


def _val(value: str) -> str:
    return f"{{{NS['w']}}}val", value


def _ensure(parent: ET.Element, tag: str) -> ET.Element:
    found = parent.find(f"w:{tag}", NS)
    if found is not None:
        return found
    elem = ET.SubElement(parent, _w(tag))
    return elem


def _set_attr(elem: ET.Element, name: str, value: str) -> None:
    elem.set(f"{{{NS['w']}}}{name}", value)


def _style(root: ET.Element, style_id: str) -> ET.Element | None:
    for style in root.findall("w:style", NS):
        if style.get(f"{{{NS['w']}}}styleId") == style_id:
            return style
    return None


def _ensure_style(root: ET.Element, style_id: str, name: str) -> ET.Element:
    style = _style(root, style_id)
    if style is not None:
        return style
    style = ET.SubElement(root, _w("style"))
    _set_attr(style, "type", "paragraph")
    _set_attr(style, "styleId", style_id)
    name_elem = ET.SubElement(style, _w("name"))
    _set_attr(name_elem, "val", name)
    return style


def _set_style(
    root: ET.Element,
    style_id: str,
    *,
    name: str,
    ascii_font: str,
    east_asia_font: str,
    size_half_points: int,
    bold: bool = False,
    outline_level: int | None = None,
    alignment: str | None = None,
    first_line_chars: int | None = None,
    line_twips: int | None = None,
    before: int | None = None,
    after: int | None = None,
) -> None:
    style = _ensure_style(root, style_id, name)
    p_pr = _ensure(style, "pPr")
    if alignment:
        jc = _ensure(p_pr, "jc")
        _set_attr(jc, "val", alignment)
    if outline_level is not None:
        outline = _ensure(p_pr, "outlineLvl")
        _set_attr(outline, "val", str(outline_level))
    if first_line_chars is not None:
        ind = _ensure(p_pr, "ind")
        _set_attr(ind, "firstLineChars", str(first_line_chars))
    if line_twips is not None or before is not None or after is not None:
        spacing = _ensure(p_pr, "spacing")
        if line_twips is not None:
            _set_attr(spacing, "line", str(line_twips))
            _set_attr(spacing, "lineRule", "auto")
        if before is not None:
            _set_attr(spacing, "before", str(before))
        if after is not None:
            _set_attr(spacing, "after", str(after))

    r_pr = _ensure(style, "rPr")
    fonts = _ensure(r_pr, "rFonts")
    _set_attr(fonts, "ascii", ascii_font)
    _set_attr(fonts, "hAnsi", ascii_font)
    _set_attr(fonts, "eastAsia", east_asia_font)
    size = _ensure(r_pr, "sz")
    _set_attr(size, "val", str(size_half_points))
    size_cs = _ensure(r_pr, "szCs")
    _set_attr(size_cs, "val", str(size_half_points))
    if bold:
        _ensure(r_pr, "b")
        _ensure(r_pr, "bCs")


def patch_styles_xml(styles_xml: bytes, profile: DocxProfile) -> bytes:
    root = ET.fromstring(styles_xml)

    doc_defaults = _ensure(root, "docDefaults")
    r_pr_default = _ensure(_ensure(doc_defaults, "rPrDefault"), "rPr")
    fonts = _ensure(r_pr_default, "rFonts")
    _set_attr(fonts, "ascii", profile.latin)
    _set_attr(fonts, "hAnsi", profile.latin)
    _set_attr(fonts, "eastAsia", profile.normal_east_asia)
    default_size = _ensure(r_pr_default, "sz")
    _set_attr(default_size, "val", "24")
    default_size_cs = _ensure(r_pr_default, "szCs")
    _set_attr(default_size_cs, "val", "24")

    _set_style(
        root,
        "Normal",
        name="Normal",
        ascii_font=profile.latin,
        east_asia_font=profile.normal_east_asia,
        size_half_points=24,
        first_line_chars=200,
        line_twips=360,
        after=0,
    )
    _set_style(
        root,
        "BodyText",
        name="Body Text",
        ascii_font=profile.latin,
        east_asia_font=profile.normal_east_asia,
        size_half_points=24,
        first_line_chars=200,
        line_twips=360,
        after=0,
    )
    _set_style(
        root,
        "Title",
        name="Title",
        ascii_font=profile.latin,
        east_asia_font=profile.heading_east_asia,
        size_half_points=32,
        bold=True,
        alignment="center",
        before=240,
        after=240,
    )
    for style_id, size, level in (
        ("Heading1", 32, 0),
        ("Heading2", 28, 1),
        ("Heading3", 24, 2),
        ("Heading4", 24, 3),
    ):
        _set_style(
            root,
            style_id,
            name=style_id.replace("Heading", "Heading "),
            ascii_font=profile.latin,
            east_asia_font=profile.heading_east_asia,
            size_half_points=size,
            bold=True,
            outline_level=level,
            before=240 if level == 0 else 180,
            after=120,
        )
    _set_style(
        root,
        "Caption",
        name="Caption",
        ascii_font=profile.latin,
        east_asia_font=profile.normal_east_asia,
        size_half_points=21,
        alignment="center",
        after=120,
    )

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_document_xml(document_xml: bytes, profile: DocxProfile) -> bytes:
    """Patch the document body's sectPr with profile-specific page size and margins.

    Margins in DocxProfile are stored in hundredths of mm; OOXML pgMar uses
    twips (1/20 point, 1440 per inch).  Paper size is stored in twips directly.
    """
    root = ET.fromstring(document_xml)
    body = root.find(f"{{{NS['w']}}}body")
    if body is None:
        return document_xml

    sect_pr = body.find(f"{{{NS['w']}}}sectPr")
    if sect_pr is None:
        return document_xml

    # Paper size — necessary for 16开 profiles like Sichuan.
    pg_sz = _ensure(sect_pr, "pgSz")
    _set_attr(pg_sz, "w", str(profile.paper_w_twips))
    _set_attr(pg_sz, "h", str(profile.paper_h_twips))

    pg_mar = _ensure(sect_pr, "pgMar")
    _set_attr(pg_mar, "top", str(_hundredths_mm_to_twips(profile.margin_top)))
    _set_attr(pg_mar, "bottom", str(_hundredths_mm_to_twips(profile.margin_bottom)))
    _set_attr(pg_mar, "left", str(_hundredths_mm_to_twips(profile.margin_left)))
    _set_attr(pg_mar, "right", str(_hundredths_mm_to_twips(profile.margin_right)))
    _set_attr(pg_mar, "header", str(profile.margin_header))
    _set_attr(pg_mar, "footer", str(profile.margin_footer))
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def build_reference_docx(profile: DocxProfile, output_dir: Path, pandoc: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / profile.filename
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "reference.docx"
        with base.open("wb") as handle:
            subprocess.run(
                [pandoc, "--print-default-data-file", "reference.docx"],
                check=True,
                stdout=handle,
            )
        patched = Path(tmp) / "patched.docx"
        with zipfile.ZipFile(base, "r") as src, zipfile.ZipFile(
            patched, "w", zipfile.ZIP_DEFLATED
        ) as dst:
            for info in src.infolist():
                data = src.read(info.filename)
                if info.filename == "word/styles.xml":
                    data = patch_styles_xml(data, profile)
                elif info.filename == "word/document.xml":
                    data = patch_document_xml(data, profile)
                dst.writestr(info, data)
        output.write_bytes(patched.read_bytes())
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default="academic-paper/templates/docx",
        help="Directory for generated reference DOCX files.",
    )
    parser.add_argument(
        "--profile",
        action="append",
        choices=sorted(PROFILES),
        help="Profile to build. May be passed multiple times. Defaults to all.",
    )
    args = parser.parse_args()

    profiles = [PROFILES[p] for p in (args.profile or sorted(PROFILES))]
    pandoc = find_pandoc()
    for profile in profiles:
        output = build_reference_docx(profile, Path(args.output_dir), pandoc)
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
