# Working on IMOBX copy

This repository is a public static website. Keep private briefs, reviews and reader
feedback outside it. Work on branches; commit, push and publish only when requested.

Before writing, use the `copywriting` skill when available and read the existing brief.
Identify the reader, the question this page answers, what they already know and their
next action. Preserve the author's meaning and distinguish facts from proposals.

Judge language in context. Navigation names destinations; buttons name actions;
explanations connect new ideas to situations the reader understands. Avoid importing
private instructions or naming discussions into visitor-facing explanations.
Marketing formulas are optional. Plain navigation labels need no unique selling claim.

Review both Portuguese and English in the browser at mobile and desktop widths. Record
editorial reasoning and browser evidence privately. Label actual audience testing
separately; an AI review or a readability score cannot establish comprehension.

Render local HTML for inspection with `python build_publication.py --preview`; this
does not rebuild PDF, PowerPoint or ZIP exports and is not a publication command.
After observing that preview, build reviewed exports with
`python build_publication.py --copy-review /absolute/private/review.json`.
The review must match the current source fingerprints and include the reader questions,
editorial answers, source sections and observed browser checks. `copy_review.py` defines
the record format. Changes invalidate the record and require another review. The build
checks record completeness and freshness, not the quality of its editorial judgment.

Follow explanations through their destination pages. A summary must answer something
useful by itself; a detail link must provide the next level of detail. Avoid repeated
cards that merely promise an agreement will explain things. Give the proposed operation,
name exact unresolved terms and link to the relevant section. Record page-by-page
coverage privately; a homepage-only pass does not complete a site-wide copy task.
