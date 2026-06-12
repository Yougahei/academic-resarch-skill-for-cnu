# Chinese Higher Education Thesis Formatting Reference

This reference adds mainland Chinese university thesis and dissertation formatting profiles to ARS. It extends the original ARS reference-based format system; it does not replace APA 7, APA 7 Chinese citation guidance, Chicago, MLA, IEEE, Vancouver, LaTeX, DOCX, or PDF output support.

Use this file when the user explicitly asks for mainland Chinese university thesis formatting, Chinese undergraduate thesis formatting, graduate dissertation formatting, GB/T 7714-oriented checking, or school-template alignment.

---

## Rule Priority

Apply formatting rules in this order:

1. User-provided university, graduate school, college, or department official thesis template.
2. User-provided advisor, program, defense, archive, or inspection requirements.
3. User-provided sample documents from the same school and year.
4. A school profile in this reference.
5. The mainland China university thesis fallback profile in this reference.

If two rules conflict, do not silently merge them. Report the conflict, name the competing rules, and ask the user which official requirement should control.

This reference is not a national mandatory standard. It is a fallback and profile guide for formatting review and future `format-convert` / `citation-check` work.

## Boundary From Existing ARS Formats

ARS already supports:

- APA 7.
- APA 7 Chinese citation guidance based mainly on Taiwan academic conventions.
- Chicago, MLA, IEEE, and Vancouver.
- LaTeX, DOCX, and PDF output guidance.

Keep all of those capabilities. Mainland Chinese university formatting is an additional profile, not a global replacement.

For mainland Chinese university theses, GB/T 7714 is usually the safer fallback citation family when no school rule is provided. The APA 7 Chinese guide remains useful for Taiwan-style or APA-requested Chinese papers, but it is not the default mainland university thesis norm.

## Source Profiles

This reference was drafted from local user-provided formatting materials. The original Word, PDF, and image files are not committed to the repository.

| Profile | Source material | Use as |
|---------|-----------------|--------|
| Mainland China University Thesis Fallback | Cross-school synthesis from the source materials below | Fallback only when no school-specific rule is available |
| Guangxi University Undergraduate Thesis/Design | Guangxi University undergraduate thesis/design basic requirements, format specification, templates, review notes, and inspection feedback | School profile for undergraduate thesis/design work |
| Sichuan University Master/Doctoral Dissertation | Sichuan University master and doctoral dissertation format file | School profile for graduate dissertation work |

One Guangxi University management PDF appears to be scanned and was not OCR'd for this issue. It is listed as source context, but text rules in this reference come from extractable Word/DOCX materials and manually inspected content.

---

## Mainland China University Thesis Fallback

Use this profile only when the user has not supplied a school or college template.

### Common Document Parts

Common mainland Chinese university thesis materials may include:

- Cover page.
- Title page.
- Originality, academic integrity, or honesty statement.
- Thesis use authorization statement.
- Chinese abstract and keywords.
- English abstract and keywords.
- Table of contents.
- Main text.
- References.
- Appendices.
- Acknowledgements.
- Process materials, when required by the school: task book, opening report, midterm check, review forms, defense records, duplicate-check report, or archive checklist.

Do not invent cover fields, logo placement, signature blocks, or school mottos. Copy those details from the official template when available.

### Abstracts And Keywords

Chinese abstract:

- Usually covers research background, objective, methods, process, results, and conclusion.
- Should avoid unsupported contribution claims and self-evaluation.
- Keywords normally follow the abstract and should be searchable academic terms.

English abstract:

- Should correspond to the Chinese abstract in meaning.
- Use consistent discipline terminology.
- Keep the keyword set aligned with the Chinese version.

Common labels:

```text
摘要
关键词：
Abstract
Keywords:
```

### Table Of Contents And Pagination

Common fallback checks:

- Front matter and main text often use separate pagination.
- Chinese and English abstract pages may use Roman numerals.
- Main text usually starts with Arabic page numbers.
- Page numbers are commonly centered in the footer, but the school template controls the exact placement.
- The table of contents should match the final heading hierarchy and page numbers.

Do not infer pagination when a Word template is supplied.

### Headings

Common heading systems include:

```text
一、标题
（一）标题
1. 标题
（1）标题
```

```text
第一章 标题
第一节 标题
一、标题
（一）标题
1. 标题
```

```text
第一章 标题
1.1 标题
1.1.1 标题
```

Use one system consistently. Do not mix Chinese numeral and decimal systems unless the official template does so.

### Body Formatting

Common fallback checks:

- Chinese body text often uses Songti/SimSun.
- English text and numbers often use Times New Roman.
- Body size is commonly 小四.
- First-line indent is commonly two Chinese characters.
- Line spacing is commonly fixed or 1.5 lines, but varies by school.
- Paragraph spacing is controlled by the official template.

These are not authoritative values. The official school template wins.

### Figures, Tables, And Equations

Figures:

- Number figures consistently, often by chapter.
- Place figure captions according to the template; many mainland thesis templates place figure captions below figures.
- Cite every figure in the text before or near placement.
- Avoid screenshots when a drawn, exported, or data-based figure is expected.

Tables:

- Number tables consistently, often by chapter.
- Place table titles according to the template; many mainland thesis templates place table titles above tables.
- Use clear units and notes.
- Three-line tables are common in many Chinese university formats.

Equations:

- Put important equations on separate centered lines.
- Number equations that are referenced later.
- Define symbols and units close to first use.

### References And GB/T 7714

Use GB/T 7714 as the fallback mainland Chinese university citation family unless the school specifies APA, MLA, IEEE, Chicago, Vancouver, or another style.

Minimum checks:

- Every in-text citation has a corresponding reference-list entry.
- Every reference-list entry is cited unless the school explicitly allows uncited bibliography items.
- Citation numbering or author-year style matches the selected GB/T 7714 variant.
- Chinese and English references follow the same selected standard rather than mixing APA and GB/T rules.
- DOI, URL, access date, volume, issue, and page data are included when required by source type and school rule.

Common source categories include journal articles, books, book chapters, dissertations, conference papers, standards, patents, reports, electronic resources, and datasets.

---

## Guangxi University Undergraduate Thesis/Design

Use this profile when the user asks for Guangxi University undergraduate thesis or undergraduate design formatting and no newer official file supersedes these rules.

### Required Materials And Archive Structure

The materials may include:

1. Cover.
2. Chinese abstract and keywords.
3. Foreign-language abstract and keywords.
4. Table of contents.
5. Main text.
6. References.
7. Appendix.
8. Acknowledgements.
9. Task book.
10. Opening report.
11. Midterm assessment.
12. Review forms.
13. Format review form.
14. Defense process record.
15. Defense grade and comments.
16. Integrity pledge.
17. Plagiarism or academic misconduct check result.
18. Foreign literature translation or reading notes.

Common binding pattern:

- First volume: items 1-8.
- Second volume: items 9-17.
- Drawings are not necessarily bound with the thesis.
- Foreign literature translation or reading notes may be separate or bound according to college requirements.

### Page Setup And Printing

Source: `07.论文审查心得及注意事项.docx` §2.1

- Paper: A4 (210 mm × 297 mm).
- Margins: top 2.54 cm, bottom 2.54 cm, left 2.2 cm, right 2.2 cm.
- Header distance from top: 2 cm.
- Footer distance from bottom: 1.75 cm.
- Overall line spacing: fixed 20 pt unless a specific element requires otherwise.
- Cover, abstracts, and table of contents: single-sided printing.
- Main text, references, appendices, and acknowledgements: double-sided printing.
- Section break after cover (not page break via carriage returns).

### Header And Footer

Source: `07.论文审查心得及注意事项.docx` §2.2, §2.3

- Header left: "广西大学本科毕业论文" or "广西大学本科毕业设计".
- Header right: paper title.
- Header font: 隶书 小四号 (12pt). If 隶书 unavailable, use 楷体 as substitute.
- Header underline: 0.4 pt horizontal rule.
- Header starts from main body Chapter 1.
- Odd and even pages use the same header content.
- Page number (front matter): Roman numerals (Ⅰ, Ⅱ, Ⅲ...), bottom center, Times New Roman 五号 (10.5pt).
- Page number (main body): Arabic numerals (1, 2, 3...), bottom center, Times New Roman 五号 (10.5pt).

### Cover

Source: `07.论文审查心得及注意事项.docx` §3

- Thesis title: 黑体 一号 (26pt), centered.
- Title max 25 characters; if split across two lines, second line left-aligned with first.
- Other info (college, major, class, student ID, name, advisor): 宋体 四号 (14pt), centered.
- Advisor name followed by two spaces then title (e.g., "教授").
- College and major names use standard full names, not abbreviations.
- Date: format "二〇二六年五月", uses "〇" not "0" or "O".
- Section break after cover.

### Chinese Abstract

Source: `07.论文审查心得及注意事项.docx` §4

- Chinese paper title above abstract: 黑体 三号 (16pt), centered, fixed 20 pt line spacing, one line space before/after.
- "摘 要" (one space between characters): 黑体 三号 (16pt), centered, fixed 20 pt, one line space before/after.
- One blank line below "摘要" before body text.
- Abstract body: 宋体 小四 (12pt), fixed 20 pt line spacing, first-line indent two Chinese characters.
- Length: 400–600 Chinese characters.
- Content structure: purpose (~100 chars), methods (~200 chars), results (~200+ chars), conclusion (~100 chars).
- Use third-person, objective tone; no first-person pronouns.
- "关键词": 黑体 小四 (12pt), left-aligned with two-character indent, on same line as keywords.
- Keywords: 宋体 小四 (12pt), 3–8 terms (recommended 5), separated by "；", no trailing punctuation.
- Section break after Chinese abstract.

### English Abstract

Source: `07.论文审查心得及注意事项.docx` §5

- All English text: Times New Roman.
- Paper title: ALL CAPS, 三号 (16pt), bold, centered.
- "ABSTRACT": 三号 (16pt), bold, centered, one blank line above and below.
- Body: Times New Roman 小四 (12pt), fixed 20 pt line spacing.
- Each paragraph: four-character-space indent; minimum five-character-space margin on each side.
- "KEYWORDS" (not "KEY WORDS", all caps, with "S"): bold, left-aligned, no indent.
- Keywords: first letter capitalized, separated by ";", no trailing punctuation.
- Section break after English abstract.

### Table Of Contents

Source: `07.论文审查心得及注意事项.docx` §6

- "目 录" (one space between characters): 黑体 三号 (16pt), centered.
- Content: 小四号 (12pt), 1.25× line spacing.
- Secondary headings indent 2 Chinese characters; tertiary headings indent 4 characters.
- Page numbers right-aligned.
- Abstract pages: Roman numeral page numbers. Main body: Arabic page numbers.
- TOC lists to second-level headings by default; third-level only for substantial results.
- TOC first page should be odd-numbered (right-hand page after binding).

### Main Text

Source: `07.论文审查心得及注意事项.docx` §7

- Body: 宋体 小四 (12pt); English/Times New Roman 小四 (12pt).
- Line spacing: fixed 20 pt throughout.
- First-line indent: two Chinese characters.
- Minimum length: 10,000 Chinese characters (recommended 12,000+).
- Results and analysis section should be ≥ 65% of total word count.
- Each chapter starts on a new page (preferably right-hand).
- If a chapter end leaves > 1/3 blank page, insert two blank lines before next chapter instead of page break.
- No automatic numbering — use manual heading numbers.

### Heading Hierarchy

Source: `07.论文审查心得及注意事项.docx` §2.5

```text
第一章 标题
1.1 标题
1.1.1 标题
1.1.1.1 标题
```

| Level | Example | Font | Size | Alignment | Spacing |
|-------|---------|------|------|-----------|---------|
| 1 | `第一章 绪论` | 黑体 | 小二号 (18pt) | Centered | One blank line before/after |
| 2 | `1.1 研究背景` | 黑体 | 小三号 (15pt) | Left-aligned | No extra space |
| 3 | `1.1.1 国内研究现状` | 黑体 | 四号 (14pt) | Left-aligned | No extra space |
| 4 | `1.1.1.1 ...` | 黑体 | 小四号 (12pt) | Left-aligned | No extra space |
| Body | Body paragraph | 宋体 小四 | 12pt | Justified | Fixed 20 pt, first-line indent 2 chars |

- No trailing punctuation after heading numbers (e.g., "1.1 标题" not "1.1. 标题").
- A heading level must have ≥ 2 peer subheadings or merge into parent.
- Prefer three-level heading structure; fourth level only for exceptional papers.

### Figures, Tables, And Equations

Source: `07.论文审查心得及注意事项.docx` §8, §9, §10

Figures:
- Figure caption below figure, centered, 五号 (10.5pt) bold, fixed 20 pt line spacing.
- English caption: "Fig." + Times New Roman bold (if bilingual).
- One blank line before figure and after figure caption.
- At least 1.5 lines of body text before any figure/table on a new page.
- No text box captions; use inline embedded images.
- Multiple images should be composited or placed in a borderless table.
- Cite figure before placement; mark source at top-right of caption if applicable.
- No watermarks, commercial marks, or trial version marks on figures.

Tables:
- Table caption above table, centered, 五号 (10.5pt) bold, fixed 20 pt line spacing.
- English caption: "Tab." + Times New Roman bold (if bilingual).
- One blank line before table caption and after table.
- Three-line table: 1.5 pt top/bottom rules, 0.5 pt header separator rule.
- Table content: 五号 (10.5pt) 宋体.
- No first-line indent in table cells.
- On page break: repeat caption with "续表" suffix.

Equations:
- Created with equation editor; do not copy-paste from references.
- Equation number at right margin on same line.
- Parameter annotations below equation, either hanging-indent or single-paragraph format.
- Cite equation before placement.
- Use Greek letters or Times New Roman for equation text; no Chinese characters inside equations.

### References

Source: `07.论文审查心得及注意事项.docx` §11

- Minimum 40 references; ≥ 2/3 from the last 5 years.
- Chinese-majority: English ≥ 1/3. English-majority: Chinese ≥ 1/5.
- Prefer journal articles over patents, books, conference papers, web articles.
- Format: 著者. 题名[J]. 期刊名称, 出版年, 卷号(期号): 起止页码.
- Dissertation format: 作者. 篇名[D]. 学校所在城市: 学校名称, 出版年份.
- Authors ≤ 3: list all. Authors > 3: list first 3 + "，等" (Chinese) or ", et al" (English).
- Chinese and foreign authors: surname first, given name abbreviated.
- Volume number required; issue number optional if absent.
- Page numbers required; use "-" for ranges, "," for separate ranges.
- Each reference ends with ".".
- In-text citation numbers before punctuation (e.g., "[9]。" not "。[9]").
- Warn: AI-generated hallucinated references must be verified by the author.

### Review And Inspection Problem Checklist

Common problems found in Guangxi materials:

- Table of contents page numbers are missing or use the wrong format.
- Abstract page numbers or fonts are wrong or missing.
- Header content and format are inconsistent.
- Chinese abstract lacks the title, or English abstract lacks the title.
- Abstract background is too long while methods, data, results, or significance are weak.
- Reference list style is inconsistent.
- References are too old, not cited, or citation order does not match the list.
- Chinese and English reference balance does not satisfy college expectations.
- Figure names and numbers do not match.
- Figure titles split across pages.
- Figures/tables do not provide enough evidence for the argument.
- Design drawings lack process flow, layout, elevation, scale, dimensions, units, legend, wind rose, or title block.
- Wording is colloquial rather than academic.

---

## Sichuan University Master/Doctoral Dissertation

Use this profile when the user asks for Sichuan University master or doctoral dissertation formatting and no newer official file supersedes these rules.

### Required Document Parts

Known profile components:

- Chinese abstract.
- English abstract.
- Table of contents.
- Review or literature review section when required.
- Main text.
- Conclusion.
- References.
- Research achievements during enrollment.
- Originality declaration.
- School thesis use authorization statement.
- Acknowledgements.

The originality declaration and authorization statement require signatures according to the official template. Do not generate final signature content without user confirmation.

### Page Setup And Core Layout

Source: `学位论文格式 (2).doc` §1

- Prepared with Microsoft Word.
- Paper size: 16 kai (184 mm × 260 mm). Note: A4 may substitute if 16 kai unavailable, but the official requirement is 16 kai.
- Main body: 小四宋体 (12pt).
- Line spacing: fixed 20 pt.
- Body layout: about 34 Chinese characters per line.
- Margins: left 2.8 cm, right 2.2 cm, top 2.5 cm, bottom 2.5 cm (estimated from 版心 requirements; adjust if official template provides exact values).
- References: 五号宋体 (10.5pt).

### Abstracts

Source: `学位论文格式 (2).doc` §2

- Chinese abstract title: 小二号宋体 (18pt).
- Major line: 小四号宋体 (12pt).
- "研究生" and "指导教师" labels: 小四号黑体 (12pt).
- Graduate name and advisor name: 小四号楷体 (12pt).
- Abstract body: 小四号宋体 (12pt).
- "关键词" label: 小四号黑体 (12pt).
- Master's abstract: about 1000 Chinese characters.
- Doctoral abstract: about 3000 Chinese characters.
- Vertical spacing: two blank lines above title, one line between title and major, one line between major and author info, two lines between author info and body.
- Foreign-language abstract should correspond to the Chinese abstract.

### Heading Hierarchy

Source: `学位论文格式 (2).doc` §1

| Level | Font | Size | Alignment | Notes |
|-------|------|------|-----------|-------|
| Level 1 | 黑体 | 小三号 (15pt) | Left-aligned | — |
| Level 2 | 黑体 | 四号 (14pt) | Left-aligned | — |
| Level 3 | 黑体 | 小四号 (12pt) | Left-aligned | — |
| Level 4 | 楷体 | 小四号 (12pt) | Left-aligned | Distinct from headings 1–3 |

No blank line between adjacent headings. One blank line between a heading and the previous paragraph. All headings left-aligned ("靠左边顶排").

### Figures And Tables

Known profile requirements:

- Leave a blank line between figures/tables and surrounding body text.
- Figure and table names: 五号黑体.
- Figure and table content: 五号宋体.
- Keep numbering, captions, and references in the body consistent.

### References And Declarations

Known profile requirements:

- References use 五号宋体 unless the official template says otherwise.
- Include research achievements during enrollment when required.
- Include originality declaration and school thesis use authorization statement.
- Advisor and student signatures must follow official school process.

---

## Implementation Entry Points

Future implementation should connect this reference to:

- `academic-paper` `format-convert` mode for mainland Chinese university thesis profile selection.
- `academic-paper` `citation-check` mode for GB/T 7714-oriented citation checks.
- `academic-pipeline` Stage 5 FINALIZE for final package verification.

For output generation, keep using the existing ARS output mechanisms:

- LaTeX and Pandoc template guidance remains in `latex_template_reference.md`.
- Built-in fallback templates are available at `templates/chinese_thesis_guangxi_undergrad_template.tex` and `templates/chinese_thesis_sichuan_grad_template.tex`.
- Built-in DOCX reference templates are available under `templates/docx/` and can be used through `scripts/export_chinese_thesis.py`.
- Citation conversion remains in `citation_format_switcher.md`.
- DOCX/PDF conversion guidance remains in `formatter_agent` and the existing reference files.

Word template parsing, OCR of scanned PDFs, and automated layout comparison are intentionally out of scope for this issue.
