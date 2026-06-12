"""Export a Chinese university thesis draft through Pandoc profiles.

This script is a thin convenience wrapper around Pandoc. Formatting rules
remain in LaTeX templates and DOCX reference documents; this script only
selects the right assets and writes a small report for the student.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ExportProfile:
    id: str
    label: str
    tex_template: Path
    reference_docx: Path


PROFILES: dict[str, ExportProfile] = {
    "mainland-fallback": ExportProfile(
        id="mainland-fallback",
        label="Mainland China University Thesis Fallback",
        tex_template=ROOT / "academic-paper/templates/chinese_thesis_guangxi_undergrad_template.tex",
        reference_docx=ROOT / "academic-paper/templates/docx/mainland_fallback_reference.docx",
    ),
    "guangxi-undergrad": ExportProfile(
        id="guangxi-undergrad",
        label="Guangxi University Undergraduate Thesis/Design",
        tex_template=ROOT / "academic-paper/templates/chinese_thesis_guangxi_undergrad_template.tex",
        reference_docx=ROOT / "academic-paper/templates/docx/guangxi_undergrad_reference.docx",
    ),
    "sichuan-grad": ExportProfile(
        id="sichuan-grad",
        label="Sichuan University Master/Doctoral Dissertation",
        tex_template=ROOT / "academic-paper/templates/chinese_thesis_sichuan_grad_template.tex",
        reference_docx=ROOT / "academic-paper/templates/docx/sichuan_grad_reference.docx",
    ),
}


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
) -> None:
    field_note = ""
    if output_format == "docx":
        field_note = (
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

    pandoc = find_pandoc()
    reference_docx = Path(args.reference_docx).resolve() if args.reference_docx else None
    tex_template = Path(args.tex_template).resolve() if args.tex_template else None
    bibliography = Path(args.bibliography).resolve() if args.bibliography else None
    csl = Path(args.csl).resolve() if args.csl else None

    _check_asset(input_path, "input")
    if output_format == "docx":
        _check_asset(reference_docx or profile.reference_docx, "reference DOCX")
    if output_format in {"pdf", "latex"}:
        _check_asset(tex_template or profile.tex_template, "LaTeX template")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_pandoc_args(
        pandoc=pandoc,
        input_path=input_path,
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

    # Post-process DOCX to add headers, footers, TOC (Issue #13)
    if output_format == "docx":
        try:
            sys.path.insert(0, str(ROOT))
            from scripts.postprocess_chinese_thesis_docx import postprocess

            postprocess(
                input_docx=output_path,
                output_docx=output_path,
                profile=profile.id,
            )
        except Exception as exc:
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
    parser.add_argument("--tex-template", help="Override LaTeX/PDF template.")
    parser.add_argument("--bibliography", help="Optional BibTeX bibliography.")
    parser.add_argument("--csl", help="Optional CSL file, for example GB/T 7714.")
    parser.add_argument("--no-citeproc", action="store_true", help="Disable Pandoc citeproc.")
    parser.add_argument("--report", help="Report path. With --format all, use per-output reports.")
    parser.add_argument("--force", action="store_true", help="Overwrite output if it already exists.")
    args = parser.parse_args()

    formats = ["docx", "pdf", "latex"] if args.format == "all" else [args.format]
    if args.format == "all" and args.report:
        parser.error("--report cannot be combined with --format all")
    try:
        for output_format in formats:
            output = export_once(args, output_format)
            print(output)
    except (FileExistsError, FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
