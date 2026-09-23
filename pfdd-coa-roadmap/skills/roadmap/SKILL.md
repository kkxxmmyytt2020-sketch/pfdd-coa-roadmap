---
name: roadmap
description: >-
  Start, resume, or check status of a PFDD COA Roadmap project — the human-gated workflow through
  FDA Patient-Focused Drug Development Guidances 1-4 that decides the meaningful aspect of health
  (MAH), concept of interest (COI), fit-for-purpose clinical outcome assessment (COA), and
  COA-based endpoint for a disease/indication. Use when the user wants to choose or justify what
  to measure in a clinical trial, select or develop a PRO/ObsRO/ClinRO/PerfO, build a conceptual
  framework or COA-based endpoint approach, plan concept-elicitation research, or says "PFDD",
  "MAH", "concept of interest", "fit-for-purpose COA", "COA roadmap". This is the entry point;
  it routes to the g1–g4 stage skills.
---

# PFDD COA Roadmap — orchestrator

This skill runs the whole workflow. It owns three things: the **state file**, the **gates**
(where the workflow stops and asks the user), and **routing** to the four stage skills.

```
G1 patient input  →  G2 what matters  →  G3 fit-for-purpose COA  →  G4 COA-based endpoint
(pfdd-coa-roadmap:    (…:g2-what-matters)  (…:g3-fit-for-purpose-coa)  (…:g4-coa-endpoint)
 g1-patient-input)
        ▲── under-represented group ──┘ ▲── COI never elicited ──┘ ▲── dilution/heterogeneity ──┘
```

The conceptual chain the whole thing serves: **MAH → COI → COA (fit-for-purpose in a context of
use) → endpoint.** Fit-for-purpose is a property of a COA *within a context of use* (G3 §II.C);
a fit-for-purpose COA is necessary but not sufficient for a good endpoint (G4 §I.B).

## 1. Open every run by showing what's behind the workflow

Before anything else, show the workflow figure so the user sees the stages, the sources behind
each step, and what AI does vs. what needs real people:

- Path: `${CLAUDE_PLUGIN_ROOT}/assets/workflow.png` — Read it (so it renders) and give a
  two-sentence orientation. If a state file exists, say which stage the project is at.
- Regenerate it only if the stage content changes: `python3 ${CLAUDE_PLUGIN_ROOT}/assets/src/make_workflow_figure.py`.

## 2. State file

Each project lives in the user's working folder as `pfdd-state.json` (create it at intake; never
store it inside the plugin). Schema → `references/state-schema.md`. Rules:

- Read it at the start of every turn that touches the project; write it after every decision.
- Every decision records **who decided** (`user` or `proposed`), the **sources** it rests on
  (guidance + section), and whether the evidence is **real patient data**, **literature**, or
  **synthetic/design-time** (see guardrail below).
- After each write, re-render the dossier:
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/render_dossier.py pfdd-state.json` → `pfdd-dossier.html`
  (HTML only). Tell the user the path; open it (`open pfdd-dossier.html`) at stage gates.

## 3. The gate protocol — how the workflow pauses and asks

The workflow **never runs end-to-end on its own.** It pulses: work a bounded chunk → show the
result → ask. Four kinds of pause, all via `AskUserQuestion` (1–4 questions per call, recommended
option first and labelled "(Recommended)", each option's description saying the consequence):

| Pause | When | Typical question |
|---|---|---|
| **Intake** | New project | Indication & population; product/mechanism of action; development phase; what materials already exist (PFDD meeting report, prior qualitative study, transcripts, candidate COAs) |
| **Decision point** | Inside a stage, whenever the guidance leaves a real choice | "Who should report for 2–5-year-olds?", "Keep which candidate MAHs?", "Use / modify / develop for this COI?" |
| **Data stop** | A step needs real data the plugin cannot create (transcripts, coded data, psychometric results, anchor data) | Offer: provide a file now · mark as *pending real data* and continue with the plan only · pause |
| **Stage gate** | End of every stage | Approve & continue · Revise something in this stage · Loop back to an earlier stage · Pause here |

Rules:
- **No stage starts until the previous gate is `approved` in the state file.** If the user asks to
  jump ahead (e.g., "just pick the COA"), explain which earlier decisions the jump assumes, record
  them as `proposed` (not `user`), and make the first question of the next gate confirm them.
- A gate question is preceded by a short summary (≤ 8 lines) of what the stage decided and the
  open evidence gaps — never by a wall of text. The dossier holds the detail.
- Subagents (the persona agents in `agents/`) **cannot ask the user anything.** Only this main
  conversation asks. Dispatch agents, collect their output, then pause.
- If the user answers "Other" with free text, treat it as the decision and record it verbatim.
- **Unattended draft** — only when the user explicitly asks for it ("draft all four stages without
  asking me", or a non-interactive run where `AskUserQuestion` is unavailable): work through the
  stages without pausing, record every decision as `decided_by: "proposed"`, leave every stage at
  `awaiting_gate` (never `approved`), and end with a numbered list of **all the gate and
  decision-point questions the user still has to answer**, each with the recommended option. The
  gates are deferred, not skipped.
  Because the user reads this in chat, the closing summary must stand on its own. For each stage,
  give 3–6 bullets, each ending with its source in brackets (e.g., "[G3 §III.C.3]"), and always state:
  - **G1:** the sampling method and its generalizability limits, and who reports for each subgroup.
  - **G2:** the evidence type behind the candidate MAHs (real / literature / pending).
  - **G3:** for each MAH, the COI, whether it is **direct or indirect**, the COA type, the branch
    (a/b/c), and the A–H gaps.
  - **G4:** the endpoint construction, the meaningfulness approach, and the top design risks. When
    any endpoint uses a PerfO, those risks always include practice effects and assistive devices.
- Loop-backs: record `{from, to, reason, date}` in `loopbacks`, set the reopened stage to
  `in_progress`, and mark later stages `stale` (their outputs stay, flagged for re-check).

## 4. Routing

| State | Do |
|---|---|
| No state file | Intake pause → create state → invoke `pfdd-coa-roadmap:g1-patient-input` |
| A stage `in_progress` / `awaiting_input` | Resume it by invoking that stage skill |
| A stage `awaiting_gate` | Re-show its summary and ask the stage-gate question |
| All four approved | Offer: final review by the `fda-coa-reviewer` agent; export dossier; loop back |
| User asks a narrow question ("which COA for itch in toddlers?") | Answer it, citing sections, then offer to record it as a decision in the relevant stage |

## 5. Guardrails (apply in every stage)

- **Synthetic ≠ evidence.** Persona agents, synthetic quotes, and simulated sorts are design-time
  checks. Anything they produce is tagged `evidence_type: "synthetic"` and is shown in the dossier
  with a "not patient evidence" badge. G1/G2 conclusions about what matters to patients require
  real, representative patient/caregiver input (G1 §II; G2 §II–III).
- **Cite or flag.** Every recommendation names its source (e.g., "G3 §IV.H", "Walton 2015 Fig. 2").
  If no source supports it, say it's a judgment call.
- **Don't invent instruments or evidence.** When naming an existing COA, state what is known about
  its context of use and say when it must be verified; never fabricate psychometric results.
- **Recommend, don't decide.** FDA dialogue is the real gate; the plugin prepares for it.

## References
- `references/state-schema.md` — `pfdd-state.json` fields and an example.
- `references/sources.md` — the seven source documents, what each contributes, and section map.
