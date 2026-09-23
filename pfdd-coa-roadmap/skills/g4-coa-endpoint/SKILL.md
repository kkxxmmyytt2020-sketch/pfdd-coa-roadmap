---
name: g4-coa-endpoint
description: >-
  Stage G4 of the PFDD COA Roadmap (FDA PFDD Guidance 4, draft; Powers 2017): turn fit-for-purpose
  COA scores into a COA-based endpoint and a plan to show the treatment effect is meaningful to
  patients — endpoint rationale and construction (fixed time point, summary, dichotomized, change),
  strategies when a disease affects several aspects of health (separate, multi-component,
  personalized), timing, estimand and missing data, meaningful score differences (MSD, anchor-based)
  and meaningful score regions (MSR), and design risks (masking, practice effects, assistive
  devices, external controls, CAT, burden). Use via the pfdd-coa-roadmap:roadmap orchestrator, or
  directly when the user asks how to build or justify a COA-based endpoint, define a responder
  threshold, choose anchors, or interpret whether a COA treatment effect is clinically meaningful.
---

# G4 — COA-based endpoint: how is a meaningful benefit read?

**Decisions this stage produces:** for each Table-1 row, the endpoint definition and rationale; a
multi-aspect strategy if several MAHs are in play; the assessment schedule; the **meaningfulness
plan** (MSD and/or MSR, anchors, when the evidence is generated); and a design-risk register.
**Reminder:** a fit-for-purpose COA is necessary but not sufficient — the endpoint must itself
preserve the meaningfulness (G4 §I.B: average intensity is a weak endpoint if patients care about
worst intensity).

Needs from G3: Table 1, COU, rationale gaps. Follow the gate protocol throughout.

## Steps

1. **Endpoint rationale checklist** (G4 §II.A.1; `references/endpoint-construction.md`). For each
   endpoint: COA type, COA, specific score, algorithm if multi-component, missing-item rule, timing
   and aggregation window, definition of baseline; plus the rationale — COI, a *specific* objective/
   hypothesis, role (primary/secondary/other), indication, why the COA is fit-for-purpose (link to
   G3 rationale), support for importance to patients, strengths/limitations. Check disease-specific
   FDA guidances.

2. **Construction choice** (G4 §II.A.2.a–d). Default: score at a prespecified time point or a summary
   over a period, compared between arms adjusting for baseline. Baseline ≠ screening value (regression
   to the mean). Dichotomizing loses power — only for well-established, meaningful health states,
   with a single prespecified, patient-justified threshold derived from data other than the
   registration trial, plus a range-of-thresholds sensitivity analysis. Change-from-baseline:
   caution for ordinal scores; percent change: asymmetric, undefined at zero, non-normal.
   **⏸** Decision point: construction per endpoint (offer 2–3 options with trade-offs).

3. **Multi-aspect strategy** (G4 §II.A.2.e). If the disease affects several MAHs, especially
   heterogeneously: separate endpoints (primary + secondary / multiple primary / co-primary — see
   *Multiple Endpoints* guidance), a **multi-component** endpoint (explicit weights; dilution risk;
   examine components; composite-indicator COAs only for item-level components), or a
   **personalized** endpoint (most bothersome symptom; Goal Attainment Scaling — standardize
   elicitation, still measure all symptoms for everyone). If dilution/heterogeneity makes the
   chosen MAH a poor fit → **loop back to G3**. **⏸** Decision point.

4. **Timing and schedule** (G4 §II.A.3). Natural course (acute/chronic/episodic), expected onset of
   effect, rate of change of the COI, recall period, event-triggered collection with end-of-day
   prompts, same schedule in all arms, collect after treatment discontinuation (estimand), patient
   input on feasibility and burden.

5. **Estimand and missing data** (G4 §II.B). Baseline-adjusted analysis at the fixed time point
   (longitudinal models may use intermediate visits); ordinal endpoints (cumulative logit vs
   dichotomy; caution with ordinal multi-component endpoints mixing symptoms, hospitalization,
   death); intercurrent events vs missing data (ICH E9(R1)); minimize missingness, collect reasons,
   sensitivity analyses aligned with the estimand. Dispatch the `biostatistician` agent for a check.

6. **Meaningfulness plan** (G4 §III; `references/meaningful-change.md`). Judge how interpretable
   the scores already are (directness of COI; simple/familiar metric). Then choose:
   **MSD** — anchor-based, multiple anchors (PGIS/PGIC and others), anchors tested in cognitive
   interviews, distribution displays per anchor level, range of thresholds, baseline-dependency and
   improvement/deterioration symmetry checked; distribution-based methods only as supporting
   information. **MSR** — PGIS-based regions, bookmarking, illustrative items, or **IRT item maps**
   (the ordered item map from G3's construct theory). Evidence generated **before** the registration
   trial; rare disease → exit interviews/surveys with neutral interviewers (masked trials).
   Record `outputs.meaningfulness_plan`. **⏸** Confirm approach and when the evidence will be built.

7. **Design-risk register** (G4 §IV.A; Powers GMP 8). Masking of patients/raters/caregivers;
   PerfO practice effects (spacing, run-in, alternate forms); assistive devices (build into the
   endpoint if changing need is a goal; supportive endpoint otherwise; record on CRF);
   nonrandomized/external/nonconcurrent controls (expectation bias, non-comparable assessment
   methods/schedules — prefer less judgment-dependent COIs, masked or automated PerfO ratings);
   subgroups defined post-baseline; CAT vs short form; participant burden; rater training for
   ClinROs. Walk every item above and mark it applicable or not. **Whenever any endpoint uses a
   PerfO, practice effects and assistive-device handling are always in the register and in the
   stage summary** (G3 App. D; G4 §IV.A.2–3). Record `outputs.design_risks`.

8. **Endpoint table** — COA · score · construction · timing · role · rationale; update Table 1's
   endpoint column. Dispatch `fda-coa-reviewer` for a final read of G3+G4 together.

## Stage gate
Summarize endpoints, meaningfulness plan, top risks, and what evidence must exist before the
registration trial. Ask: Approve (workflow complete) · Revise G4 · Loop back to G3 (e.g.,
heterogeneity → reconsider MAH or add a personalized endpoint) · Pause. On approval, render the
final dossier and open it.

## References
- `references/endpoint-construction.md` — rationale checklist; construction options with pitfalls;
  multi-aspect strategies; timing; estimation and missing data.
- `references/meaningful-change.md` — interpretability factors; MSD (anchors, analyses, threshold
  ranges); MSR (PGIS, bookmarking, illustrative items, IRT); applying them to trial results; design
  considerations.
