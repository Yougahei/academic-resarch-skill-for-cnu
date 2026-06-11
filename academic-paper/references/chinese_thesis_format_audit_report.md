# Chinese Thesis Format Audit Report

Use this report template when the user asks to check mainland Chinese university thesis or dissertation formatting. This is an audit/reporting workflow, not an automatic DOCX rewriting workflow.

Controlling reference: `chinese_higher_education_thesis_format.md`.

## Activation Signals

Activate this audit when the user asks for any of:

- Chinese university thesis format check.
- Mainland Chinese undergraduate thesis formatting review.
- Guangxi University undergraduate thesis/design format check.
- Sichuan University master/doctoral dissertation format check.
- GB/T 7714-oriented thesis reference check.
- Thesis table of contents, pagination, heading, figure/table/equation, or archive-material review.

If the user only asks to convert citations between APA, IEEE, Chicago, MLA, or Vancouver, keep using the normal citation conversion path.

## Profile Selection

Select the controlling profile in this order:

1. User-uploaded official school, graduate school, college, or department template.
2. User-uploaded advisor, defense, inspection, or archive requirement.
3. User-uploaded sample from the same school and year.
4. School profile in `chinese_higher_education_thesis_format.md`.
5. Mainland China University Thesis Fallback.

When the target profile is unclear, ask the user for the school, degree level, paper type, and available official template. If the user cannot provide them, continue with the fallback profile and mark the profile choice as an assumption.

## Evidence Rules

Mark every finding with one of these evidence statuses:

| Status | Meaning |
|--------|---------|
| `verified` | The supplied manuscript or template contains enough evidence to check the rule |
| `missing-input` | The rule needs DOCX/PDF/template evidence that the user has not supplied |
| `conflict` | Two supplied rules disagree and require user confirmation |
| `profile-fallback` | The rule comes from a built-in profile, not a user-supplied official file |
| `not-applicable` | The rule does not apply to the user's paper type or supplied materials |

Do not guess DOCX-only facts such as actual margins, page breaks, header/footer content, or table-of-contents field behavior from plain Markdown alone.

## Required Output Shape

```markdown
## Chinese Thesis Format Audit Report

### 1. Profile And Rule Priority
| Item | Value |
|------|-------|
| Selected profile | ... |
| Degree / paper type | ... |
| Highest-priority source used | ... |
| Fallback rules used | yes/no + reason |
| Conflicts requiring confirmation | ... |

### 2. Inputs Inspected
| Input | Present? | What can be verified | Limits |
|-------|----------|----------------------|--------|
| Manuscript text / Markdown | yes/no | ... | ... |
| DOCX draft | yes/no | ... | ... |
| Official template | yes/no | ... | ... |
| PDF / rendered output | yes/no | ... | ... |
| Reference list / bibliography | yes/no | ... | ... |

### 3. Findings Summary
| Severity | Count | Meaning |
|----------|-------|---------|
| Blocker | ... | Must be resolved before submission/archive |
| Major | ... | Likely to fail school or college inspection |
| Minor | ... | Formatting inconsistency or cleanup item |
| Needs confirmation | ... | Rule conflict or missing official input |

### 4. Detailed Audit
| Area | Rule | Evidence status | Finding | Severity | Recommended action |
|------|------|-----------------|---------|----------|--------------------|
| Page setup | ... | verified/missing-input/... | ... | ... | ... |
| Front matter | ... | ... | ... | ... | ... |
| Abstracts and keywords | ... | ... | ... | ... | ... |
| Table of contents and pagination | ... | ... | ... | ... | ... |
| Heading hierarchy | ... | ... | ... | ... | ... |
| Body formatting | ... | ... | ... | ... | ... |
| Figures, tables, and equations | ... | ... | ... | ... | ... |
| References and GB/T 7714 | ... | ... | ... | ... | ... |
| Declarations / appendices / acknowledgements | ... | ... | ... | ... | ... |
| Process and archive materials | ... | ... | ... | ... | ... |

### 5. Items Requiring User Confirmation
| Question | Why it matters | Current assumption |
|----------|----------------|--------------------|
| ... | ... | ... |

### 6. Action Checklist
- [ ] ...
- [ ] ...
- [ ] ...
```

## Audit Areas

### Page Setup

Check what the available input can support:

- Paper size.
- Margins.
- Line spacing.
- Header and footer.
- Page number format and location.
- Single-sided or double-sided printing assumptions.

If only Markdown/plain text is supplied, mark page setup as `missing-input` and explain that DOCX/PDF/template evidence is required.

### Front Matter

Check whether expected front matter exists:

- Cover or title page.
- Chinese abstract and keywords.
- English abstract and keywords.
- Table of contents.
- Originality, integrity, or authorization statement when required.

Do not invent cover content or signature blocks.

### Abstracts And Keywords

Check:

- Chinese and English abstract presence.
- Approximate length requirements in the selected profile.
- Whether objective, methods, results, and conclusion are represented.
- Keyword count, separators, and final punctuation.
- Chinese-English semantic correspondence when both versions are supplied.

### Table Of Contents And Pagination

Check:

- Whether a table of contents exists.
- Whether the heading levels in the table of contents match the selected profile.
- Whether abstract/front-matter pagination and body pagination follow the profile.
- Whether page numbers are present and consistent.

If page numbers cannot be verified from input, mark as `missing-input`.

### Heading Hierarchy

Check:

- Numbering system consistency.
- Level depth allowed by the selected profile.
- Whether a heading level contains only one subsection.
- Whether common thesis chapters are present when expected, such as introduction, main analysis, conclusion, references, appendices, and acknowledgements.

### Body Formatting

Check:

- Body font family, size, indentation, and line spacing when DOCX/PDF evidence is supplied.
- Minimum or recommended body length when text is supplied.
- Whether the structure matches the paper type.

### Figures, Tables, And Equations

Check:

- Figure/table/equation numbering.
- Caption placement.
- Whether every figure/table/equation is referenced in text.
- Whether units, notes, symbols, and equation parameter explanations are supplied.
- Whether obvious screenshots or split captions may violate the profile.

### References And GB/T 7714

When the selected profile uses mainland Chinese university fallback rules:

- Treat GB/T 7714 as the default citation family unless a school rule says otherwise.
- Confirm all in-text citations and reference-list entries cross-reference.
- Check whether citation order and numbering are consistent.
- Flag APA 7 Chinese/Taiwan conventions if they are being used as the default for a mainland university thesis without an explicit school requirement.

### Declarations, Appendices, Acknowledgements, And Archive Materials

Check the selected profile's required declaration and archive materials. For Guangxi University undergraduate work, check whether task book, opening report, midterm assessment, review forms, defense records, integrity pledge, duplicate-check result, and foreign literature translation/reading notes are accounted for when the user asks for archive/package readiness.

For Sichuan University graduate work, check originality declaration, thesis use authorization statement, research achievements during enrollment, and acknowledgements when required.

## Severity Guidance

| Severity | Use when |
|----------|----------|
| Blocker | Required official element is absent, wrong profile is used, or citation/reference integrity is broken |
| Major | Likely school inspection problem: wrong page setup, missing abstract, wrong TOC/pagination, inconsistent headings, missing declaration, severe reference style mismatch |
| Minor | Cosmetic or consistency issue that should be fixed but is unlikely to invalidate the thesis alone |
| Needs confirmation | Official sources conflict, or the evidence needed to judge the rule is missing |

## Non-Goals

Do not:

- Rewrite the manuscript content.
- Modify a DOCX file.
- Generate final signatures, seals, school cover layouts, or authorization text without user confirmation.
- Claim page setup, header/footer, or page break compliance without DOCX/PDF/template evidence.
