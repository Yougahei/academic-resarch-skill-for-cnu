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

Known profile requirements:

- Paper: A4.
- Margins: top 2.54 cm, bottom 2.54 cm, left 2.2 cm, right 2.2 cm.
- Overall line spacing: fixed 20 pt unless a specific element requires otherwise.
- Cover, abstracts, and table of contents: single-sided printing.
- Main text, references, appendices, and acknowledgements: double-sided printing.
- Page number: centered in the footer.

### Cover

Common cover rules:

- Thesis/design title: 黑体 一号, centered.
- Other cover information: 宋体 四号, centered.
- Use the official Guangxi University cover when available; do not recreate seal, logo, or field layout from memory.

### Chinese Abstract

Known profile requirements:

- Chinese title appears above the abstract when required by the template.
- `摘要`: 黑体 三号, centered; the two Chinese characters may use spaced layout.
- Abstract body: 宋体 小四, fixed 20 pt line spacing, first-line indent two Chinese characters.
- Length: commonly at least 400 Chinese characters; review notes suggest roughly 400-600 Chinese characters.
- Content: purpose, significance, methods, process, results, conclusion, and innovation where appropriate.
- Avoid self-evaluation and unsupported claims.
- `关键词`: label in 黑体 小四; keyword terms in 宋体 小四.
- Keywords: usually 3-8 terms; 5 is a practical target when no stricter rule is given.
- Separator: Chinese semicolon `；`; no final punctuation after the last keyword.

### English Abstract

Known profile requirements:

- English abstract uses Times New Roman, corresponding in size to the Chinese abstract.
- `ABSTRACT` and title formatting should follow the official template.
- Body line spacing commonly follows fixed 20 pt.
- `Keywords` use semicolon-separated terms.
- No final punctuation after the last keyword when the template follows the Chinese keyword convention.

### Table Of Contents

Known profile requirements:

- `目录`: 黑体 三号, centered; review notes show spaced-character layout may be expected.
- Contents: 宋体 小四.
- The table of contents generally reaches second-level headings, unless the template requires deeper levels.
- Chinese and English abstracts should appear in the table of contents when required.
- Abstract pages use Roman numerals; main text uses Arabic numerals.
- Second-level entries may indent two Chinese spaces; third-level entries may indent four Chinese spaces.
- Common line spacing: 1.25 lines in some review notes.

### Main Text

Known profile requirements:

- Main text length: at least 10,000 Chinese characters/words; some review notes recommend about 12,000.
- Common structure: introduction or preface, method or design argumentation, process, result analysis, conclusion or summary.
- First chapter is often expected to be `绪论`.
- Results and analysis should be substantial; review notes expect them to be the majority of the body for some thesis/design types.
- Each chapter may start on a new page or right-side page depending on template/printing setup.

### Heading Hierarchy

Known Guangxi profile styles:

```text
第一章 标题
1.1 标题
1.1.1 标题
1.1.1.1 标题
```

Common formatting from review notes:

| Level | Example | Format |
|-------|---------|--------|
| 1 | `第一章 绪论` | 小二号黑体, centered; blank line before/after |
| 2 | `1.1 研究背景` | 小三号黑体, left aligned |
| 3 | `1.1.1 国内研究现状` | 四号黑体, left aligned |
| 4 | `1.1.1.1 ...` | 小四号黑体, left aligned |
| Body | Body paragraph | 宋体 小四; English Times New Roman 12 pt; fixed 20 pt; first-line indent two Chinese characters |

Avoid using only one subsection under a heading level. Review notes prefer multiple peer subsections when a level is introduced.

### Figures, Tables, And Equations

Figures:

- Use computer-drawn or exported figures; avoid freehand drawings and casual screenshots.
- Number by chapter, for example `图3-2`.
- Figure title goes below the figure.
- Figure title commonly uses 五号 bold; English titles may use Times New Roman bold and `Fig.`.
- Do not split figure title and figure across pages.
- Cite figures before placement.

Tables:

- Number by chapter, for example `表5-4`.
- Table title goes above the table.
- Use units, notes, and consistent decimal precision.
- Three-line tables are commonly expected.
- Keep table titles and tables together across page breaks when possible.

Equations:

- Display equations on separate centered lines.
- Number by chapter, for example `(2-3)`, placed at the right end.
- Explain parameters and units after the equation when needed.

### References

Known profile checks:

- Use in-text upper-right numeric references such as `[序号]` when required by the template.
- Include foreign-language literature when required by the college.
- Design work may require at least two English papers.
- Some thesis review notes expect 13 or more English papers for research theses.
- Prefer recent references from the last 3-5 years unless a source is foundational.
- Ensure all listed references are cited in the text and citation order matches the list when using numbered style.
- Avoid casual, low-value, or uncited references.
- Include complete author, title, journal/book, year, volume, issue, pages, DOI/URL, and other required metadata.

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

Known profile requirements:

- Prepared with Microsoft Word.
- Paper size: 16 kai.
- Main body: 小四宋体.
- Line spacing: fixed 20 pt.
- Body layout: about 34 Chinese characters per line.
- References: 五号宋体.

### Abstracts

Known profile requirements:

- Chinese abstract title: 小二宋体.
- Major line: 小四宋体.
- Graduate and advisor labels: 小四黑体.
- Names: 小四楷体.
- Abstract body: 小四宋体.
- Keyword label: 小四黑体.
- Master's abstract: about 1000 Chinese characters.
- Doctoral abstract: about 3000 Chinese characters.
- Foreign-language abstract should correspond to the Chinese abstract.

### Heading Hierarchy

Known profile requirements:

| Level | Format |
|-------|--------|
| Level 1 | 小三黑体, left aligned |
| Level 2 | 四号黑体, left aligned |
| Level 3 | 小四黑体, left aligned |
| Level 4 | 小四楷体, left aligned |

There should be no blank line between adjacent headings. There should be a blank line between a heading and the previous paragraph.

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

- LaTeX guidance remains in `latex_template_reference.md`.
- Citation conversion remains in `citation_format_switcher.md`.
- DOCX/PDF conversion guidance remains in `formatter_agent` and the existing reference files.

Word template parsing, OCR of scanned PDFs, and automated layout comparison are intentionally out of scope for this issue.
