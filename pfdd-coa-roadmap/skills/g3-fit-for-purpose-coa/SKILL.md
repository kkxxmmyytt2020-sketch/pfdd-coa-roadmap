---
name: g3-fit-for-purpose-coa
description: >-
  Stage G3 of the PFDD COA Roadmap (FDA PFDD Guidance 3 + Walton 2015, Powers 2017, Cano & Hobart
  2011): select the meaningful aspect(s) of health (MAH), derive the concept of interest (COI) for
  each, define the context of use (COU), choose the COA type (PRO/ObsRO/ClinRO/PerfO), search for
  existing COAs and decide use / modify / develop new, and build the evidence-based rationale
  (components A–H) and conceptual-framework Table 1 showing the COA is fit-for-purpose. Use via
  the pfdd-coa-roadmap:roadmap orchestrator, or directly when the user asks which COA to use for a
  concept, whether a COA is fit-for-purpose, how to justify a COI that differs from the MAH, how to
  modify an existing COA, or how to fill in the A–H rationale table.
---

# G3 — Fit-for-purpose COA: what to measure, and with which COA?

**Decisions this stage produces, in order:** MAH(s) targeted → COI for each MAH → COU → COA type →
specific COA (existing / modified / new) → evidence rationale A–H → **Table 1** (MAH · COI · COA
type · COA name · score · COA-based endpoint sketch).
**The rule of order:** choose the benefit (MAH) first, then the COI that informs it — never pick a
COI because it is known to show treatment effects (Powers 2017, ABSSSI example). The steps can
iterate (G3 §III: decisions are interrelated; Walton Fig. 1 "interplay"), but each iteration
re-states the MAH first.
**Fit-for-purpose** describes a COA *in a COU*: the level of validation is sufficient for that
context (G3 §II.C). It is judged by the A–H rationale, with more evidence required where there is
more uncertainty.

Needs from G2: candidate MAH hierarchy with evidence type. Follow the gate protocol throughout.

## Steps

1. **Select MAH(s)** (G3 §II.B.1, §III.B; Walton "Identification of the Intended Treatment
   Benefit"). For each candidate MAH, score against: important to patients (G2 evidence); part of
   typical daily life; **core/proximal** manifestation vs distal impact; plausibly affected by the
   mechanism of action; able to change within the trial's time frame; relevant to most vs some
   patients (heterogeneity → G4 multi-aspect strategy). If a secondary manifestation is targeted
   instead of the core, justify its value to patients (G3 §III.B fn). Represent complex MAHs as a
   hierarchy figure (G3 Fig. 2). Record `outputs.mah_selection`. **⏸** User chooses MAH(s).

2. **COI for each MAH** (G3 §II.B.2; Walton Fig. 1–2; Powers GMP 2–3, Fig. 1;
   `references/mah-coi-cou.md`). Decide **direct** (COI = MAH, typical for PROs of feelings) vs
   **indirect** (a narrower, more measurable bodily ability or sign thought to drive the MAH, e.g.
   leg strength or walking speed for ambulation). Name the characteristic measured (intensity,
   frequency, duration, worst vs average). Place the COI on the **indirectness continuum**; the
   more indirect, the more component-H evidence G3/G4 will demand (Walton attribute 3). One MAH may
   need several COIs (G3 Fig. 3); say how they combine to support an inference about the MAH.
   **⏸** Confirm COI(s) — offer direct vs indirect options with their evidence burden.

3. **Context of use** (G3 §II.B.3; Walton's 8 COU components; Powers Table 3). Target population
   (definition, inclusion criteria, baseline severity, subgroups, expected events such as assistive
   device use); use of the COA in the endpoint; implementation (setting, mode, who completes);
   trial design (comparator, masking); schedule; culture/language; concomitant care. Record
   `outputs.cou`.

4. **COA type** (G3 §III.C.1, App. A–D; Walton attributes 1–2; Powers; `references/coa-types.md`).
   Who can validly report the COI in this COU? PRO for anything known only to the patient if they
   can self-report; ObsRO for observable behaviours when they can't (**never proxy**); ClinRO when
   professional judgment is required (readings / ratings; **clinician global assessments are not
   acceptable as a primary basis** — Powers); PerfO for standardized task performance (usually an
   indirect COI). Pediatric: one version across ages if the COI can be measured reliably across the
   range; otherwise justified multiple versions or types (G3 §III.C.3 — e.g., caregiver ObsRO of
   scratching for all ages + itch-intensity PRO for those who can self-report). Accessibility and
   universal design (G3 §III.C.4). This is component A of the rationale. **⏸** Confirm type.

5. **Search existing COAs → three branches** (G3 §III.C.2; `references/existing-coa-search.md`).
   Search literature, item banks (e.g., PROMIS), FDA COA Qualification Program and MDDT, clinical
   trial registries, FDA review summaries and disease-specific guidances. Run the **label check**:
   a COA's name does not show it measures the MAH (Walton, "Identifying the COA") — compare its
   actual items/tasks, COI, and development COU with yours. For each candidate record COU match:
   - **(a) same/similar COU → use** it; assess fitness, summarize existing evidence, find gaps.
   - **(b) different COU → collect additional evidence and modify as necessary**; classify each
     modification by whether it likely changes scores/interpretation (e.g., recall period change
     ≈ new measure; paper → single-item-per-screen ePRO usually not). Check copyright.
   - **(c) none → develop a new COA** (step 6).
   Record `outputs.coa_landscape`. **⏸** Branch per COI.

6. **New-COA path (branch c)** (G3 §III.C.2.c; Cano & Hobart; `references/new-coa-development.md`).
   Construct theory before items; concept elicitation (G2) → item/task generation in patients'
   words, each item tagged to its place on the COI's predicted severity ordering → item tracking
   matrix → cognitive interviews → measurement model (reflective vs composite; CTT/IRT/Rasch) and
   psychometric analysis plan → missing-item scoring rule → user manual and training → evaluate in
   an early-phase trial or standalone observational study **before** the registration trial.
   Submit qualitative protocols and analysis plans to FDA for comment first.

7. **Evidence rationale A–H** (G3 §IV, Table 2, App. E; `references/evidence-rationale.md`).
   For each COA: state COU, MAH justification, and (if COI ≠ MAH) how the COI informs the MAH; then
   fill components A–H with claim, support, and status **supported / partial / gap**, and for each
   gap the study that would close it. Weigh evidence against uncertainty (G3 §II.C). Dispatch
   `fda-coa-reviewer` and `psychometrician` agents to challenge the rationale — they return
   critiques; you present them. Record `outputs.rationale`.

8. **Table 1** (G3 §III.D). MAH · COI · COA type · COA name · score · COA-based endpoint (initial
   thoughts only — G4 refines). Record `outputs.table1`.

## Stage gate
Summarize Table 1 and the rationale's gaps. Ask: Approve & continue to G4 · Revise G3 ·
Loop back to G2 (a COI/MAH was never elicited from patients, or a subgroup's experience is missing) ·
Pause.

## References
- `references/mah-coi-cou.md` — MAH, COI, COU definitions and selection criteria, direct/indirect
  continuum, worked structures (Walton Fig. 2; G3 Fig. 2–3).
- `references/coa-types.md` — PRO, ObsRO, ClinRO (readings/ratings/CGA), PerfO: when to use,
  implementation cautions, pediatrics.
- `references/existing-coa-search.md` — where to search, COU matching, label check, modification
  impact table, copyright.
- `references/new-coa-development.md` — construct theory, item generation, cognitive interviews,
  measurement models, scoring and missing items, pre-registration evaluation.
- `references/evidence-rationale.md` — components A–H, evidence sources, App. E template.
