---
name: g2-what-matters
description: >-
  Stage G2 of the PFDD COA Roadmap (FDA PFDD Guidance 2): identify what matters to patients and
  turn it into a candidate hierarchy of meaningful aspects of health (MAHs) — background research,
  interviews vs focus groups, non-leading interview guides, barriers to self-report, coding
  dictionary, saturation, and coder agreement. Use via the pfdd-coa-roadmap:roadmap orchestrator,
  or directly when the user wants to draft or check a concept-elicitation interview guide, lint
  survey/interview questions for leading or double-barreled wording, build a coding dictionary,
  assess saturation, or check inter-coder agreement on patient transcripts.
---

# G2 — What matters: what do patients say matters to them?

**Decision this stage produces:** a *candidate MAH hierarchy* (activities/experiences → lower-order
MAHs → higher-order MAHs, per G3 Fig. 2) with the patient evidence for each: how many patients
raised it, how important/bothersome, in which subgroups.
**Hands to G3:** the candidate MAHs with evidence; the concepts patients use in their own words.

Needs from G1: research questions, target population, reporter plan. If G1 isn't approved, follow
the orchestrator's jump-ahead rule. Follow the gate protocol throughout.

## Steps

1. **Background research first** (G2 §II.A). Characterize the disease and current therapies from
   literature, PFDD meeting reports, and experts; draft a **disease model** (G3 §III.A: bodily
   process → signs/symptoms → impacts on feeling/functioning). This seeds the preliminary coding
   dictionary. Record sources.

2. **Choose the method** (G2 §III.A, Tables 1 & 4, App. 1). One-on-one interviews for depth,
   sensitive topics, heterogeneous presentations; focus groups (5–10 people) for range and
   efficiency; both sequentially is common. Administration mode (in person / phone / video) fits
   the population. Other methods: Delphi (expert consensus), observation (for people who cannot
   communicate verbally), facilitated patient meetings, open-ended surveys, mixed methods (G2 §V).
   **⏸** Decision point: method(s) and mode.

3. **Draft the interview/discussion guide** (G2 App. 3 Table 5; `references/question-rules.md`).
   Structure: interviewer instructions → warm-up → core open-ended questions → targeted
   approaches (typical-day diary, critical incident, free listing, **ranking** of importance and
   bothersomeness) → wrap-up. Plain language (shortness of breath, not dyspnea). For caregivers of
   patients who can't self-report, ask what they **observe**, never proxy questions.
   Then **lint** every question:
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_questions.py guide.txt` (one question per line) →
   flags leading, judging, double-barreled, double-negative, jargon, incomplete and proxy-phrased
   questions. The linter is a heuristic screen: review each flag and fix or justify it. Record
   `outputs.interview_guide_lint`. **⏸** Show the revised guide; confirm.

4. **Pilot and conduct** (real data — **data stop**). The plugin cannot interview patients. Ask:
   provide transcripts/coded data now · mark *pending real data* and continue designing · pause.
   If only literature exists, build the hierarchy from it and label every MAH
   `evidence_type: literature` so G3 knows the patient voice is indirect.

5. **Coding dictionary** (G2 App. 3–4). Hierarchical: main codes (candidate MAHs) → detailed codes
   (concepts in patients' words), each with a definition, inclusion/exclusion notes, and an example
   quote. Derive initial codes from the disease model and guide; let new codes emerge from data;
   keep a memo trail of how codes were derived.

6. **Coder agreement — blind coder** (G2 App. 4 quality control). Dispatch the `blind-coder`
   agent with **only the code definitions and the unlabeled segments** (never the true codes, never
   the hierarchy's parent labels if those would leak the answer). Compare with the human/primary
   coding: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/agreement.py primary.csv blind.csv` → Cohen's κ,
   per-code agreement, confusion pairs. Low agreement on a pair of codes means the definitions
   don't separate them → sharpen, merge, or split, then re-run once. Record `outputs.coder_agreement`.
   If no real transcripts exist yet, this can run on **synthetic quotes** to stress-test the
   dictionary before fieldwork — tag the result `synthetic` (it tests the definitions, not what
   patients think).

7. **Saturation** (G2 App. 4, Table 7). From coded data (`interview_id, order, concept` CSV):
   `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/saturation.py coded.csv --planned N` → grid of concepts
   by 25% chunk of planned interviews, first-mention chunk, new concepts per chunk. Saturation =
   no new important concepts in the last chunk **and** the sample looks representative (check
   G1's heterogeneity dimensions). If not reached or a subgroup is thin → **loop back to G1**
   (record reason). Record `outputs.saturation`.

8. **Build the candidate MAH hierarchy** (G3 §III.A–B, Fig. 2). Group concepts into lower-order
   MAHs, and those into higher-order MAHs where patients' experience supports it. For each:
   patients mentioning it (n, %), spontaneous vs probed, importance/bothersome rank, subgroup
   differences, representative quotes. Flag **core/proximal** manifestations vs **distal impacts**
   (G3 §III.B) — G3 uses this. Record `outputs.mah_hierarchy`. Optionally dispatch
   `patient-voice` / `caregiver-observer` / `clinical-expert` agents to critique the hierarchy for
   missing or conflated concepts (their critique = questions for real research).

## Stage gate
Summarize: method, guide status, evidence type behind the hierarchy (real / literature /
pending), saturation status, κ, top candidate MAHs with evidence. Ask: Approve & continue to G3 ·
Revise G2 · Loop back to G1 (name the under-represented group) · Pause.

## References
- `references/question-rules.md` — what makes a good elicitation/survey question (G2 §III.B, §IV.B,
  App. 3), with G2's own bad-question examples.
- `references/coding-and-saturation.md` — coding dictionary structure, QA, saturation method,
  reporting, screening/exit interviews.
