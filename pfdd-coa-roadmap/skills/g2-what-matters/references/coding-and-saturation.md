# Coding, quality control, saturation, reporting (G2 App. 3–5)

## Study materials to have before fieldwork (G2 App. 3 Table 5)
Research protocol (objectives, target population with clinical characteristics, sites, number
and length of sessions) · interview/discussion guide · training materials (mock sessions,
consent/assent) · glossary · **coding dictionary** · **data analysis plan** (coders and
credentials, discrepancy resolution, coding stages, saturation method, table shells) — the analysis
plan is set *before* data collection. G3 §III.C.2.c: submit qualitative protocols and guides to
FDA for comment before starting.

## Coding dictionary
- Codes = category/concept descriptions; hierarchical main codes → detailed codes.
- Initial codes from prior knowledge (natural history, disease model, guide structure); refine as
  concepts emerge. Memos record how each code was derived.
- Choose the unit (line-by-line vs segments), what is relevant enough to code, and the grammatical
  form of code labels (actions vs processes vs nouns).
- FDA generally recommends coding qualitative data for regulatory submissions (G2 App. 4).

For this plugin, each code carries: `code`, `parent`, `definition`, `include`, `exclude`,
`example_quote`. The `blind-coder` agent receives only `code`, `definition`, `include`, `exclude`.

## Quality control (G2 App. 4)
Read and re-read transcripts; apply codes consistently; **multiple coders** with agreement checks
on a subset; audit trail; analyze in the order collected and display in a grid.
`scripts/agreement.py` reports Cohen's κ overall and per code plus the most-confused code pairs.
Interpretation is a judgment — use κ to find definitions that don't separate concepts, not as a
pass/fail number.

## Saturation (G2 App. 4, Table 7)
No new relevant information emerges; more data would not add to understanding of the concept.
One approach: compare concepts in the first 25% of planned interviews with the next 25%, then the
first 50% with the next 25%, and so on. If saturation isn't reached at the planned n, or a subgroup
needs more data, add interviews. Before concluding saturation, check participant demographics for
representativeness.

`scripts/saturation.py coded.csv --planned N` expects columns `interview_id,order,concept` (order =
interview sequence number, 1..N) and prints: grid (concept × chunk: number of participants endorsing),
first-mention chunk, and new concepts per chunk. `--groups` treats `interview_id` as focus-group id
and chunks = groups (reproduces the G2 Table 7 layout).

## Reporting (G2 App. 4)
Present clearly with participants' own words; follow COREQ-type reporting.

## Screening/exit interviews (G2 App. 5)
Within trials: capture changes experienced, expectations, side effects, burden, and — importantly
for G4 — **patients' own definitions of meaningful improvement/worsening**. Use a trained neutral
third-party interviewer; conduct outside the main study period to protect integrity. Especially
useful in rare diseases where stand-alone qualitative studies are hard.
