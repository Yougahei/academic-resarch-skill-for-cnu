"""Export a Chinese university thesis draft through Pandoc profiles.

This script is a thin convenience wrapper around Pandoc. Formatting rules
remain in LaTeX templates and DOCX reference documents; this script only
selects the right assets and writes a small report for the student.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ExportProfile:
    id: str
    label: str
    tex_template: Path
    reference_docx: Path
    school_label: str
    degree_label: str
    paper_type_label: str
    cover_docx: Path | None = None
    header_text: str = "本科毕业论文"
    toc_title: str = "目  录"


DOCX_TEMPLATE_DIR = ROOT / "academic-paper" / "templates" / "docx"
TEX_TEMPLATE_DIR = ROOT / "academic-paper" / "templates"


def _profile_id_from_stem(stem: str) -> str:
    """Convert filename stem like 'fudan_undergrad' to profile id 'fudan-undergrad'."""
    return stem.replace("_", "-")


def _read_json_sidecar(path: Path) -> dict:
    """Read JSON sidecar file, returning {} if missing or invalid."""
    if path.exists() and path.suffix == ".json":
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def discover_profiles() -> dict[str, ExportProfile]:
    """Scan templates/docx/ directory for reference docx files and discover profiles.

    Each *reference.docx file paired with an optional {stem}.json sidecar file
    creates a profile. Hardcoded profiles in this file take priority when an id
    overlaps (so they can't be overridden by accidental file drops).
    """
    discovered: dict[str, ExportProfile] = {}

    if not DOCX_TEMPLATE_DIR.is_dir():
        return discovered

    for ref_path in sorted(DOCX_TEMPLATE_DIR.glob("*_reference.docx")):
        stem = ref_path.stem.replace("_reference", "")
        pid = _profile_id_from_stem(stem)

        # Read optional sidecar JSON (filename without _reference suffix)
        meta = _read_json_sidecar(ref_path.parent / f"{stem}.json")

        # Try to infer tex template
        tex_stem = f"chinese_thesis_{stem}_template.tex"
        tex_candidate = TEX_TEMPLATE_DIR / tex_stem
        tex_path = tex_candidate if tex_candidate.exists() else TEX_TEMPLATE_DIR / "chinese_thesis_guangxi_undergrad_template.tex"

        # Try to infer cover docx
        cover_path = DOCX_TEMPLATE_DIR / "covers" / f"{stem}_thesis_cover.docx"
        cover = cover_path if cover_path.exists() else None

        discovered[pid] = ExportProfile(
            id=pid,
            label=meta.get("label", f"Chinese University Thesis ({pid})"),
            tex_template=tex_path,
            reference_docx=ref_path,
            school_label=meta.get("school_label", ""),
            degree_label=meta.get("degree_label", ""),
            paper_type_label=meta.get("paper_type_label", ""),
            cover_docx=cover,
            header_text=meta.get("header_text", "本科毕业论文"),
            toc_title=meta.get("toc_title", "目  录"),
        )

    return discovered


# Hardcoded built-in profiles — take priority over discovered.
_BUILTIN_PROFILES: dict[str, ExportProfile] = {
    "mainland-fallback": ExportProfile(
        id="mainland-fallback",
        label="Mainland China University Thesis Fallback",
        tex_template=ROOT / "academic-paper/templates/chinese_thesis_guangxi_undergrad_template.tex",
        reference_docx=ROOT / "academic-paper/templates/docx/mainland_fallback_reference.docx",
        school_label="Mainland China University",
        degree_label="Unspecified",
        paper_type_label="Thesis",
        header_text="本科毕业论文",
        toc_title="目录",
    ),
    "guangxi-undergrad": ExportProfile(
        id="guangxi-undergrad",
        label="Guangxi University Undergraduate Thesis/Design",
        tex_template=ROOT / "academic-paper/templates/chinese_thesis_guangxi_undergrad_template.tex",
        reference_docx=ROOT / "academic-paper/templates/docx/guangxi_undergrad_reference.docx",
        school_label="广西大学",
        degree_label="本科",
        paper_type_label="本科毕业论文",
        cover_docx=ROOT / "academic-paper/templates/docx/covers/guangxi_undergrad_thesis_cover.docx",
        header_text="广西大学本科毕业论文",
        toc_title="目  录",
    ),
    "sichuan-grad": ExportProfile(
        id="sichuan-grad",
        label="Sichuan University Master/Doctoral Dissertation",
        tex_template=ROOT / "academic-paper/templates/chinese_thesis_sichuan_grad_template.tex",
        reference_docx=ROOT / "academic-paper/templates/docx/sichuan_grad_reference.docx",
        school_label="四川大学",
        degree_label="硕士/博士",
        paper_type_label="学位论文",
        header_text="四川大学硕士学位论文",
        toc_title="目  录",
    ),
}


# Merge: built-in profiles take priority over discovered ones with the same id.
def _build_profiles() -> dict[str, ExportProfile]:
    merged = discover_profiles()
    merged.update(_BUILTIN_PROFILES)
    return merged


PROFILES: dict[str, ExportProfile] = _build_profiles()

COVER_FIELD_KEYS: tuple[str, ...] = (
    "title",
    "college",
    "major",
    "class-name",
    "student-id",
    "author",
    "advisor",
    "date",
    "paper-type",
)

THESIS_METADATA_KEYS: tuple[str, ...] = (
    "title",
    "title-en",
    "abstract-zh",
    "keywords-zh",
    "abstract-en",
    "keywords-en",
)

REQUIRED_ABSTRACT_KEYS: tuple[str, ...] = (
    "abstract-zh",
    "keywords-zh",
    "abstract-en",
    "keywords-en",
)


@dataclass(frozen=True)
class PreparedMarkdown:
    path: Path
    metadata: dict[str, str]
    source_path: Path


def find_pandoc() -> str:
    env_path = os.environ.get("PANDOC")
    if env_path and Path(env_path).exists():
        return env_path
    path = shutil.which("pandoc")
    if path:
        return path
    try:
        import pypandoc  # type: ignore

        return str(pypandoc.get_pandoc_path())
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Pandoc not found. Install pandoc or pypandoc_binary first."
        ) from exc


def build_tool_env() -> dict[str, str]:
    """Return an environment that can see a user-local TeX Live if present."""
    env = os.environ.copy()
    candidates = [
        Path.home() / "texlive/2026-ars/bin/universal-darwin",
        Path.home() / "texlive/2026/bin/universal-darwin",
        Path.home() / "texlive/2025/bin/universal-darwin",
        Path.home() / "texlive/2024/bin/universal-darwin",
    ]
    for root in sorted((Path.home() / "texlive").glob("*/bin/*"), reverse=True):
        candidates.append(root)
    current = env.get("PATH", "")
    for candidate in candidates:
        if (candidate / "xelatex").exists() and str(candidate) not in current.split(os.pathsep):
            current = str(candidate) + os.pathsep + current
    env["PATH"] = current
    return env


def _check_asset(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")


def _parse_simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return {}
    raw = match.group(1)
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(raw) or {}
        if not isinstance(loaded, dict):
            return {}
        return {str(key): str(value) for key, value in loaded.items() if value is not None}
    except Exception:
        # Fallback line-by-line parser: splits on the first colon in each line.
        # Limitations: cannot parse multi-line values, lists, nested mappings,
        # YAML comments, or values containing colons. Suitable only for simple
        # flat frontmatter with thesis metadata.
        fields: dict[str, str] = {}
        for line in raw.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            value = value.strip().strip("'\"")
            if value:
                fields[key.strip()] = value
        return fields


def _frontmatter_bounds(text: str) -> tuple[int, int] | None:
    if not text.startswith("---"):
        return None
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return None
    return match.span()


def _strip_frontmatter(text: str) -> str:
    bounds = _frontmatter_bounds(text)
    if bounds is None:
        return text
    return text[bounds[1]:]


def _find_markdown_h1(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return ""


def _strip_initial_h1(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    stripped = False
    for line in lines:
        if not stripped and re.match(r"^#\s+.+?\s*$", line):
            stripped = True
            continue
        if stripped and not output and not line.strip():
            continue
        output.append(line)
    return "\n".join(output).strip() + "\n"


def _heading_level(line: str) -> int | None:
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
    if not match:
        return None
    return len(match.group(1))


def _heading_title(line: str) -> str:
    match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
    return match.group(1).strip() if match else ""


def _is_zh_abstract_heading(title: str) -> bool:
    return re.sub(r"\s+", "", title) in {"摘要", "中文摘要"}


def _is_en_abstract_heading(title: str) -> bool:
    return re.sub(r"\s+", "", title).upper() in {"ABSTRACT", "ENGLISHABSTRACT"}


def _clean_abstract_block(lines: list[str], *, english: bool) -> tuple[str, str]:
    abstract_lines: list[str] = []
    keywords = ""
    keyword_pattern = (
        r"^\s*(?:\*\*)?\s*(?:KEYWORDS?|Keywords?)\s*(?:\*\*)?\s*[:：]\s*(.+?)\s*$"
        if english
        else r"^\s*(?:\*\*)?\s*关键词\s*(?:\*\*)?\s*[:：]\s*(.+?)\s*$"
    )
    for line in lines:
        match = re.match(keyword_pattern, line)
        if match:
            keywords = match.group(1).strip()
            continue
        abstract_lines.append(line)
    abstract = "\n".join(abstract_lines).strip()
    return abstract, keywords


def extract_inline_abstract_blocks(body: str) -> tuple[dict[str, str], str]:
    """Extract ## 摘要 / ## ABSTRACT blocks and remove them from body markdown."""
    lines = body.splitlines()
    metadata: dict[str, str] = {}
    output: list[str] = []
    i = 0
    while i < len(lines):
        level = _heading_level(lines[i])
        title = _heading_title(lines[i]) if level else ""
        is_zh = bool(level and _is_zh_abstract_heading(title))
        is_en = bool(level and _is_en_abstract_heading(title))
        if not (is_zh or is_en):
            output.append(lines[i])
            i += 1
            continue

        i += 1
        block: list[str] = []
        while i < len(lines):
            next_level = _heading_level(lines[i])
            if next_level is not None and next_level <= level:
                break
            block.append(lines[i])
            i += 1
        abstract, keywords = _clean_abstract_block(block, english=is_en)
        if is_zh:
            if abstract:
                metadata["abstract-zh"] = abstract
            if keywords:
                metadata["keywords-zh"] = keywords
        else:
            if abstract:
                metadata["abstract-en"] = abstract
            if keywords:
                metadata["keywords-en"] = keywords

    cleaned = "\n".join(output).strip() + "\n"
    return metadata, cleaned


def _yaml_quote(value: str) -> str:
    """Quote a string value for safe inline YAML.

    Prefers yaml.dump() when available for correctness; falls back to manual
    escaping that handles the most common cases (backslash, double quote). The
    fallback does NOT handle tabs, leading special characters (:, #), or values
    containing triple-double-quotes — these are unlikely in thesis metadata.
    """
    try:
        import yaml  # type: ignore

        dumped = yaml.dump(value, allow_unicode=True, default_flow_style=False)
        return dumped.rstrip("\n")
    except Exception:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'


def _render_yaml_metadata(metadata: dict[str, str]) -> str:
    lines = ["---"]
    for key in THESIS_METADATA_KEYS:
        value = metadata.get(key, "")
        if not value:
            continue
        if "\n" in value:
            lines.append(f"{key}: |")
            lines.extend(f"  {line}" if line else "" for line in value.splitlines())
        else:
            lines.append(f"{key}: {_yaml_quote(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


# Alias map for backward-compatible cover field names.
_COVER_FIELD_ALIASES: dict[str, str] = {
    "supervisor": "advisor",
    "class": "class-name",
    "student_number": "student-id",
    "student_id": "student-id",
    "supervisor_name": "advisor",
    "college_name": "college",
    "department": "college",
    "school": "college",
}


def _normalize_cover_fields(fields: dict[str, str]) -> dict[str, str]:
    """Normalize alias field names to canonical keys defined in COVER_FIELD_KEYS."""
    normalized = {}
    for key, value in fields.items():
        canonical = _COVER_FIELD_ALIASES.get(key, key)
        normalized[canonical] = value
    return normalized


def prepare_markdown_for_export(input_path: Path, output_dir: Path) -> PreparedMarkdown:
    """Normalize thesis metadata and remove title/abstract blocks from body."""
    text = input_path.read_text(encoding="utf-8")
    frontmatter = _parse_simple_frontmatter(text)
    frontmatter = _normalize_cover_fields(frontmatter)
    body = _strip_frontmatter(text)
    title = frontmatter.get("title") or _find_markdown_h1(body)
    inline_metadata, body_without_abstracts = extract_inline_abstract_blocks(body)
    retained_keys = set(THESIS_METADATA_KEYS) | set(COVER_FIELD_KEYS)
    metadata = {
        **inline_metadata,
        **{key: value for key, value in frontmatter.items() if key in retained_keys},
    }
    if title:
        metadata["title"] = title
    # Only strip first H1 if it matches the frontmatter title (avoids eating chapter headings)
    first_h1 = _find_markdown_h1(body_without_abstracts)
    if first_h1 and title and first_h1.strip() == title.strip():
        body_without_title = _strip_initial_h1(body_without_abstracts)
    else:
        body_without_title = body_without_abstracts
    normalized = _render_yaml_metadata(metadata) + body_without_title
    normalized_path = output_dir / f"{input_path.stem}.normalized.md"
    normalized_path.write_text(normalized, encoding="utf-8")
    return PreparedMarkdown(
        path=normalized_path,
        metadata=metadata,
        source_path=input_path,
    )


def validate_abstract_metadata(metadata: dict[str, str]) -> None:
    missing = [key for key in REQUIRED_ABSTRACT_KEYS if not metadata.get(key)]
    if missing:
        raise ValueError(
            "Chinese thesis export requires existing bilingual abstracts before formatting. "
            f"Missing: {', '.join(missing)}. Run the abstract generation flow first, "
            "or add abstract-zh, keywords-zh, abstract-en, and keywords-en to the Markdown frontmatter."
        )


def extract_cover_fields(input_path: Path, profile: ExportProfile) -> dict[str, str]:
    """Extract cover metadata from Markdown frontmatter and H1 fallback."""
    text = input_path.read_text(encoding="utf-8")
    fields = _normalize_cover_fields(_parse_simple_frontmatter(text))
    title = fields.get("title") or _find_markdown_h1(text)
    if title:
        fields["title"] = title
    fields.setdefault("paper-type", profile.paper_type_label)
    return {key: value for key, value in fields.items() if key in COVER_FIELD_KEYS and value}


def cover_fields_from_metadata(metadata: dict[str, str], profile: ExportProfile) -> dict[str, str]:
    fields = _normalize_cover_fields(
        {key: value for key, value in metadata.items() if key in COVER_FIELD_KEYS and value}
    )
    fields.setdefault("paper-type", profile.paper_type_label)
    return fields


def cover_field_status(fields: dict[str, str]) -> tuple[list[str], list[str]]:
    required = [key for key in COVER_FIELD_KEYS if key != "paper-type"]
    filled = [key for key in required if fields.get(key)]
    missing = [key for key in required if not fields.get(key)]
    return filled, missing


def build_pandoc_args(
    *,
    pandoc: str,
    input_path: Path,
    output_path: Path,
    output_format: str,
    profile: ExportProfile,
    reference_docx: Path | None = None,
    tex_template: Path | None = None,
    bibliography: Path | None = None,
    csl: Path | None = None,
    citeproc: bool = True,
) -> list[str]:
    args = [pandoc, str(input_path), "-o", str(output_path)]
    if output_format == "docx":
        ref = reference_docx or profile.reference_docx
        args.extend(["--reference-doc", str(ref)])
    elif output_format == "pdf":
        template = tex_template or profile.tex_template
        args.extend(
            [
                "--template",
                str(template),
                "--pdf-engine",
                "xelatex",
                "--top-level-division",
                "chapter",
            ]
        )
    elif output_format == "latex":
        template = tex_template or profile.tex_template
        args.extend(
            [
                "-t",
                "latex",
                "--standalone",
                "--template",
                str(template),
                "--top-level-division",
                "chapter",
            ]
        )
    else:
        raise ValueError(f"unsupported output format: {output_format}")

    if citeproc and (bibliography or csl):
        args.append("--citeproc")
        args.extend(["--reference-location", "section"])
    if bibliography:
        args.extend(["--bibliography", str(bibliography)])
    if csl:
        args.extend(["--csl", str(csl)])
    return args


def write_report(
    *,
    report_path: Path,
    input_path: Path,
    output_path: Path,
    output_format: str,
    profile: ExportProfile,
    command: list[str],
    cover_docx: Path | None = None,
    cover_fields: dict[str, str] | None = None,
) -> None:
    field_note = ""
    if output_format == "docx":
        filled, missing = cover_field_status(cover_fields or {})
        cover_note = "\n## Cover Template\n"
        if cover_docx:
            cover_note += (
                f"- Cover source: `{cover_docx}`\n"
                f"- Filled fields: {', '.join(filled) if filled else 'none'}\n"
                f"- Fields left for manual completion: {', '.join(missing) if missing else 'none'}\n"
            )
        else:
            cover_note += "- Cover source: not configured for this profile.\n"
        field_note = (
            cover_note
            +
            "\n## Word/WPS Manual Refresh\n"
            "Open the generated DOCX in Word/WPS/LibreOffice, select all, "
            "refresh fields, then inspect the table of contents, page numbers, "
            "captions, headers, and final pagination.\n"
            "\nHeaders, footers, page numbers, and TOC were added by the "
            "auto post-processing step (scripts/postprocess_chinese_thesis_docx.py).\n"
            "If they appear incorrect, open the DOCX and manually adjust:\n"
            "  - Headers: 广西大学本科毕业论文 (left) + title (right), 隶书 小四号\n"
            "  - Footers: Roman numerals (front matter), Arabic (body)\n"
            "  - TOC: Right-click > Update Field > Update entire table\n"
        )
    report_path.write_text(
        "\n".join(
            [
                "# Chinese Thesis Export Report",
                "",
                f"- Profile: `{profile.id}` ({profile.label})",
                f"- Input: `{input_path}`",
                f"- Output: `{output_path}`",
                f"- Format: `{output_format}`",
                f"- School: `{profile.school_label}`",
                f"- Degree level: `{profile.degree_label}`",
                f"- Paper type: `{profile.paper_type_label}`",
                "",
                "## Pandoc Command",
                "",
                "```bash",
                " ".join(command),
                "```",
                field_note,
                "## Priority Reminder",
                "",
                "User-provided official school/college templates override built-in fallback templates.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def export_once(args: argparse.Namespace, output_format: str) -> Path:
    profile = PROFILES[args.profile]
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    if args.format == "all":
        output_path = output_path.with_suffix(f".{output_format if output_format != 'latex' else 'tex'}")

    if output_path.exists() and not args.force:
        raise FileExistsError(f"Refusing to overwrite existing output: {output_path}")

    _check_asset(input_path, "input")
    with tempfile.TemporaryDirectory(prefix="ars-thesis-export-") as tmp:
        prepared = prepare_markdown_for_export(input_path, Path(tmp))
        validate_abstract_metadata(prepared.metadata)
        pandoc = find_pandoc()
        reference_docx = Path(args.reference_docx).resolve() if args.reference_docx else None
        tex_template = Path(args.tex_template).resolve() if args.tex_template else None
        cover_docx = Path(args.cover_docx).resolve() if args.cover_docx else profile.cover_docx
        bibliography = Path(args.bibliography).resolve() if args.bibliography else None
        csl = Path(args.csl).resolve() if args.csl else None
        cover_fields = cover_fields_from_metadata(prepared.metadata, profile)

        if output_format == "docx":
            _check_asset(reference_docx or profile.reference_docx, "reference DOCX")
            if cover_docx:
                _check_asset(cover_docx, "cover DOCX")
        if output_format in {"pdf", "latex"}:
            _check_asset(tex_template or profile.tex_template, "LaTeX template")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        command = build_pandoc_args(
            pandoc=pandoc,
            input_path=prepared.path,
            output_path=output_path,
            output_format=output_format,
            profile=profile,
            reference_docx=reference_docx,
            tex_template=tex_template,
            bibliography=bibliography,
            csl=csl,
            citeproc=not args.no_citeproc,
        )
        subprocess.run(command, check=True, env=build_tool_env())

        # Post-process DOCX to add cover, abstracts, headers, footers, and TOC.
        if output_format == "docx":
            try:
                sys.path.insert(0, str(ROOT))
                from scripts.postprocess_chinese_thesis_docx import postprocess

                postprocess(
                    input_docx=output_path,
                    output_docx=output_path,
                    profile=profile.id,
                    cover_docx=cover_docx,
                    cover_fields=cover_fields,
                    abstract_fields=prepared.metadata,
                )
            except Exception as exc:
                if not args.keep_on_post_process_fail:
                    if output_path.exists():
                        output_path.unlink()
                    raise RuntimeError(
                        f"DOCX post-processing failed and output has been removed. "
                        f"Fix the cause and re-run. Original error: {exc}"
                    ) from exc
                print(f"WARNING: DOCX post-processing failed: {exc}", file=sys.stderr)
                print("The raw Pandoc DOCX was saved; you can re-run post-processing manually.", file=sys.stderr)

        if args.report:
            report = Path(args.report).resolve()
        else:
            report = output_path.with_suffix(output_path.suffix + ".format_report.md")
        write_report(
            report_path=report,
            input_path=input_path,
            output_path=output_path,
            output_format=output_format,
            profile=profile,
            command=command,
            cover_docx=cover_docx if output_format == "docx" else None,
            cover_fields=cover_fields if output_format == "docx" else None,
        )
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Input Markdown file.")
    parser.add_argument("--output", required=True, help="Output file path.")
    parser.add_argument(
        "--profile",
        required=True,
        choices=sorted(PROFILES),
        help="Chinese thesis formatting profile.",
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=["docx", "pdf", "latex", "all"],
        help="Output format. `all` writes .docx, .pdf, and .tex siblings.",
    )
    parser.add_argument("--reference-docx", help="Override DOCX reference template.")
    parser.add_argument("--cover-docx", help="Override DOCX cover template.")
    parser.add_argument("--tex-template", help="Override LaTeX/PDF template.")
    parser.add_argument("--bibliography", help="Optional BibTeX bibliography.")
    parser.add_argument("--csl", help="Optional CSL file, for example GB/T 7714.")
    parser.add_argument("--no-citeproc", action="store_true", help="Disable Pandoc citeproc.")
    parser.add_argument("--report", help="Report path. With --format all, use per-output reports.")
    parser.add_argument("--force", action="store_true", help="Overwrite output if it already exists.")
    parser.add_argument(
        "--keep-on-post-process-fail",
        action="store_true",
        help="Keep incomplete DOCX output even if post-processing fails.",
    )
    args = parser.parse_args()

    formats = ["docx", "pdf", "latex"] if args.format == "all" else [args.format]
    if args.format == "all" and args.report:
        parser.error("--report cannot be combined with --format all")
    try:
        for output_format in formats:
            output = export_once(args, output_format)
            print(output)
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
