# Upstream Capability Audit

This audit records the capability surface inherited from upstream Academic Research Skills before CNU-specific localization work begins.

## Summary

- The fork contains 4 skills, 23 declared modes, and 14 slash commands.
- Static command coverage is intact: every slash command points to an existing skill, mode, or implementation script.
- The upstream Chinese-language support is real but limited: it covers APA 7 Chinese citation conventions, bilingual abstracts, mixed Chinese-English references, CJK fonts, and DOCX/PDF/LaTeX output guidance.
- The upstream project does not yet provide mainland Chinese undergraduate thesis formatting rules such as cover-page structure, table-of-contents layout, margins, line spacing, heading hierarchy, or GB/T 7714 as the default citation norm.

## Skill And Mode Coverage

Legend:

- Registry: mode appears in `MODE_REGISTRY.md`.
- Skill doc: mode has trigger, routing, or workflow coverage in the corresponding `SKILL.md`.
- Slash command: a direct `/ars-*` command exists. `No` means the mode is reached by natural-language routing or a broader command.
- Full verification: whether complete validation requires an interactive model run rather than static inspection.

### deep-research

| Mode | Example trigger | Registry | Skill doc | Slash command | Full verification |
|---|---|---:|---:|---:|---:|
| `full` | "研究 AI 对高等教育的影响" | Yes | Yes | No | Yes |
| `quick` | "给我一份 X 的快速摘要" | Yes | Yes | No | Yes |
| `systematic-review` | "帮我做 X 的系统性文献回顾，含 PRISMA" | Yes | Yes | No | Yes |
| `socratic` | "引导我研究 X" | Yes | Yes | No | Yes |
| `fact-check` | "帮我核查这些说法" | Yes | Yes | No | Yes |
| `lit-review` | "帮我做文献回顾" | Yes | Yes | No | Yes |
| `review` | "审查这篇论文的研究质量" | Yes | Yes | No | Yes |

`deep-research` has no dedicated slash command per mode. It is loaded through natural-language routing or through the full pipeline.

### academic-paper

| Mode | Example trigger | Registry | Skill doc | Slash command | Full verification |
|---|---|---:|---:|---:|---:|
| `full` | "帮我写一篇论文" | Yes | Yes | No | Yes |
| `plan` | "引导我写论文" | Yes | Yes | `/ars-plan` | Yes |
| `outline-only` | "先帮我搭论文大纲" | Yes | Yes | `/ars-outline` | Yes |
| `revision` | "我有初稿，这是审稿意见" | Yes | Yes | `/ars-revision` | Yes |
| `revision-coach` | "帮我整理这些审稿意见成修订路线图" | Yes | Yes | `/ars-revision-coach` | Yes |
| `abstract-only` | "帮我写这篇的摘要" | Yes | Yes | `/ars-abstract` | Yes |
| `lit-review` | "把这批数据写成文献回顾论文" | Yes | Yes | `/ars-lit-review` | Yes |
| `format-convert` | "转换成 LaTeX" / "引用格式转 IEEE" | Yes | Yes | `/ars-format-convert` | Yes |
| `citation-check` | "检查引用格式" | Yes | Yes | `/ars-citation-check` | Yes |
| `disclosure` | "帮我生成 NeurIPS 的 AI 使用声明" | Yes | Yes | `/ars-disclosure` | Yes |

`academic-paper` full mode is present but does not have a dedicated slash command. It is selected by natural-language routing or by `academic-pipeline`.

### academic-paper-reviewer

| Mode | Example trigger | Registry | Skill doc | Slash command | Full verification |
|---|---|---:|---:|---:|---:|
| `full` | "审查这篇论文" | Yes | Yes | `/ars-reviewer` | Yes |
| `quick` | "快速评估这篇论文" | Yes | Yes | `/ars-reviewer` with explicit mode | Yes |
| `guided` | "引导我改进这篇论文" | Yes | Yes | `/ars-reviewer` with explicit mode | Yes |
| `methodology-focus` | "检查研究方法" | Yes | Yes | `/ars-reviewer` with explicit mode | Yes |
| `re-review` | "验收修订" | Yes | Yes | `/ars-reviewer` with explicit mode | Yes |
| `calibration` | "用我的 gold set 校准 reviewer" | Yes | Yes | `/ars-reviewer` with explicit mode | Yes |

`/ars-reviewer` directly dispatches full review by default and honors explicit alternate reviewer modes.

### academic-pipeline

| Entry | Example trigger | Registry | Skill doc | Slash command | Full verification |
|---|---|---:|---:|---:|---:|
| Stage 1 full pipeline | "我想做一篇完整的研究论文" | Yes | Yes | `/ars-full` | Yes |
| Stage 2.5 mid-entry | "我已经有论文，帮我审查" | Yes | Yes | `/ars-full` or natural-language routing | Yes |
| Stage 4 revision entry | "我收到审稿意见了" | Yes | Yes | `/ars-full` or natural-language routing | Yes |

The pipeline is an orchestrator, not a regular named mode. It dispatches `deep-research`, `academic-paper`, and `academic-paper-reviewer` through staged handoffs.

## Slash Command Coverage

| Command | Target | Direct script | Static status |
|---|---|---:|---:|
| `/ars-full` | `academic-pipeline` full workflow | No | OK |
| `/ars-plan` | `academic-paper` `plan` | No | OK |
| `/ars-outline` | `academic-paper` `outline-only` | No | OK |
| `/ars-revision` | `academic-paper` `revision` | No | OK |
| `/ars-revision-coach` | `academic-paper` `revision-coach` | No | OK |
| `/ars-abstract` | `academic-paper` `abstract-only` | No | OK |
| `/ars-lit-review` | `academic-paper` `lit-review` | No | OK |
| `/ars-reviewer` | `academic-paper-reviewer` `full` plus explicit alternates | No | OK |
| `/ars-format-convert` | `academic-paper` `format-convert` | No | OK |
| `/ars-citation-check` | `academic-paper` `citation-check` | No | OK |
| `/ars-disclosure` | `academic-paper` `disclosure` | No | OK |
| `/ars-mark-read` | Human-read citation signal | `scripts/ars_mark_read.py` | OK |
| `/ars-unmark-read` | Rescind human-read signal | `scripts/ars_mark_read.py --unmark` | OK |
| `/ars-cache-invalidate` | Citation verification cache invalidation | `scripts/ars_cache_invalidate.py` | OK |

## Upstream Chinese Capability Boundary

Existing upstream support:

- `academic-paper/references/apa7_chinese_citation_guide.md` provides APA 7 Chinese citation guidance based on Taiwan academic conventions.
- `academic-paper/references/citation_format_switcher.md` includes an APA 7 Chinese format section and mixed Chinese-English reference handling.
- README files document bilingual abstracts, Chinese output, Source Han Serif / CJK font setup, DOCX via Pandoc, and PDF/LaTeX via tectonic.
- `academic-paper` supports bilingual abstracts and citation style conversion across APA, Chicago, MLA, IEEE, and Vancouver.

Not present upstream:

- Mainland Chinese undergraduate thesis formatting defaults.
- GB/T 7714 as the default Chinese university citation standard.
- University-specific Word template parsing.
- Cover page, declaration page, table-of-contents, margin, line spacing, page-numbering, heading hierarchy, appendix, acknowledgement, and defense-material rules for Chinese universities.

## Verification Notes

Static verification already performed for this audit:

- Plugin JSON parses successfully.
- `skills/` plugin symlinks resolve to all 4 skill directories.
- Top-level plugin agents exist for `synthesis_agent`, `research_architect_agent`, and `report_compiler_agent`.
- Slash command references resolve to existing skills, modes, or scripts.
- `scripts/ars_cache_invalidate.py --help` and `scripts/ars_mark_read.py --help` start successfully.
- `scripts/announce-ars-loaded.sh` lists all 14 slash commands.

Full behavior still requires live agent sessions because most modes are prompt-driven and interactive.
