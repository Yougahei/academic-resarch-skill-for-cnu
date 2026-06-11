# Chinese Undergraduate Thesis Formatting Reference

This reference is a fallback guide for mainland Chinese undergraduate thesis formatting. It is not a university-specific template and must not override official school or department rules.

## Rule Priority

Apply formatting rules in this order:

1. User-provided university or school official thesis template.
2. User-provided department or advisor-specific requirements.
3. User-provided sample documents from the same program.
4. This fallback reference.

If this reference conflicts with any user-provided rule, pause and ask the user to confirm the official requirement. Do not silently merge conflicting requirements.

## Boundary From Upstream APA Chinese Support

Upstream ARS includes an APA 7 Chinese citation guide based mainly on Taiwan academic conventions. That is useful for Chinese-language academic writing, but it is not the default norm for mainland undergraduate theses.

For mainland Chinese university theses, GB/T 7714 is usually the safer default citation family unless the school explicitly requires APA, MLA, IEEE, Chicago, or another style.

## Front Matter

Common front matter may include:

- Cover page.
- Title page.
- Academic integrity statement or originality statement.
- Authorization statement for thesis use.
- Chinese abstract.
- English abstract.
- Keywords.
- Table of contents.
- Lists of figures or tables when required.

School templates often define exact cover layout, logo placement, school name, major, student ID, advisor, college, date, and signature blocks. These details are template-specific and should be copied from the official document, not inferred.

## Abstracts And Keywords

Chinese abstract:

- Usually written in Chinese academic prose.
- Should state research background, objective, method, findings, and conclusion.
- Avoid unsupported claims and exaggerated contribution language.
- Keywords normally appear after the abstract.

English abstract:

- Should match the Chinese abstract in meaning, not necessarily sentence by sentence.
- Use discipline-appropriate terminology consistently.
- Keywords should correspond to the Chinese keywords.

Fallback label conventions:

- `摘要`
- `关键词：`
- `Abstract`
- `Keywords:`

## Table Of Contents And Pagination

Common requirements:

- Front matter may use Roman numerals or separate pagination, depending on school rules.
- Main text usually starts from page 1.
- Page numbers are often centered in the footer, but this is school-specific.
- The table of contents should reflect the final heading hierarchy and page numbers.

Do not invent pagination rules when a Word template is provided. Treat the template as authoritative.

## Heading Hierarchy

A common fallback hierarchy is:

```text
一级标题：1 标题
二级标题：1.1 标题
三级标题：1.1.1 标题
```

Some schools require Chinese numerals:

```text
一、标题
（一）标题
1. 标题
```

Choose the hierarchy from the official template when available. Do not mix numbering systems in one thesis.

## Body Formatting

Common fallback checks:

- Font family for Chinese body text is often Songti or SimSun.
- English and numbers often use Times New Roman.
- Body text size is commonly 小四 or equivalent.
- Line spacing is commonly fixed value or 1.5 lines, but varies by school.
- First-line indent is commonly two Chinese characters.
- Paragraph spacing is usually controlled by the template.

These values are intentionally non-authoritative. The school template wins.

## Figures, Tables, And Equations

Figures:

- Number figures by chapter or sequentially according to school rules.
- Place figure captions consistently above or below figures as required.
- Cite every figure in the text before or near its placement.

Tables:

- Number tables consistently.
- Use clear table titles.
- Avoid splitting small tables across pages unless the template permits it.
- Explain notes, abbreviations, and data sources.

Equations:

- Number important displayed equations when referenced later.
- Keep symbol definitions close to first use.
- Follow the discipline's notation conventions.

## Notes, Appendices, And Acknowledgements

Notes:

- Use footnotes or endnotes only if the school permits them.
- Keep explanatory notes separate from bibliographic references when GB/T 7714 is used.

Appendices:

- Use appendices for questionnaires, interview outlines, extended tables, code snippets, or supplementary derivations.
- Reference each appendix from the main text.

Acknowledgements:

- Keep acknowledgements concise and professional.
- Do not place methods, evidence, or unverified claims in acknowledgements.

## References And GB/T 7714 Basics

Use GB/T 7714 as the fallback mainland Chinese undergraduate thesis reference family unless the school specifies another style.

Minimum checks:

- Every in-text citation must have a corresponding reference-list entry.
- Every reference-list entry should be cited in the text unless the school permits uncited bibliography items.
- Reference numbering or author-year style must match the selected GB/T 7714 variant.
- Chinese and English references should follow the same selected standard, not a mixture of APA and GB/T rules.
- DOI, URL, and access dates should be included when required by source type and school rules.

Common GB/T 7714 source categories include journal articles, books, book chapters, dissertations, conference papers, standards, patents, reports, electronic resources, and datasets.

## Implementation Entry Points

Future implementation should connect this reference to:

- `academic-paper` `format-convert` mode for formatting guidance.
- `academic-paper` `citation-check` mode for GB/T 7714-oriented citation checks.
- `academic-pipeline` Stage 5 FINALIZE for final package verification.

Word template parsing is intentionally out of scope for this reference. A later issue can define template ingestion, field extraction, and automated layout comparison.
