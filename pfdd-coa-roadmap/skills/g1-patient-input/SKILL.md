---
name: g1-patient-input
description: >-
  Stage G1 of the PFDD COA Roadmap (FDA PFDD Guidance 1): decide whose input counts and whether the
  patient-experience evidence base is representative — research objectives and questions, target
  population, who reports (self-report vs caregiver/observer), sampling method, representativeness,
  saturation-based sample size, and leveraging existing data. Use via the pfdd-coa-roadmap:roadmap
  orchestrator, or directly when the user asks how to sample patients/caregivers for concept
  elicitation, who should report for a pediatric or cognitively impaired population, or whether an
  existing PFDD meeting report / literature / registry is representative enough.
---

# G1 — Patient input: whose voice counts, and is it representative?

**Decision this stage produces:** an *evidence inventory* (what patient-experience data already
exist and whom they represent), a *reporter plan* (who reports for each subgroup), and a
*sampling plan* for any new qualitative/quantitative work — with representativeness gaps named.
**Hands to G2:** the research questions, the target population definition, the reporter plan.

Read the state file first (`pfdd-state.json`); if this stage is `approved`, say so and offer the
gate options instead of redoing work. Follow the orchestrator's gate protocol throughout.

## Steps

Each step ends with what gets recorded. Pause with `AskUserQuestion` where marked **⏸**.

1. **Research objectives → research questions** (G1 §II.A–B, Fig. 1 steps 1–8).
   Draft 2–4 specific objectives (e.g., "identify the most bothersome symptoms", "characterize
   impacts on daily function", "understand how burden changes with severity"), each refined into
   answerable research questions. Consult literature and subject-matter experts first (G1 §II.B).
   Record `outputs.research_questions`. **⏸** Confirm objectives with the user.

2. **Define the target population** (G1 §II.C.1). Diagnostic criteria; spectrum of severity,
   duration, subtype; whether "newly diagnosed" or the full spectrum is meant. Warn when a
   restricted population may not generalize (G1's Parkinson's example).

3. **Decide who reports** (G1 §II.C.2; G2 §VI; G3 App. B). Default is direct patient report.
   Assess self-report feasibility per subgroup against: cognitive development/function, language,
   numeracy (if a numeric scale), health literacy, health state, comorbidities. Where self-report is
   not feasible, plan to elicit **observable behaviours from caregivers — never proxy report of
   the patient's inner experience**. Set criteria for who the reporter is, whether it may change
   during a study, and record the reporter for every data point. Record `outputs.reporter_plan`.
   **⏸** Decision point: reporter per age/ability band.

4. **Inventory existing evidence** (G1 §II.F.2, Table 3; G3 §III.A). Search/collect: FDA or
   externally-led PFDD meeting reports, published qualitative studies, natural-history studies,
   registries, prior sponsor research, verified patient communities. For each, record source,
   type, population covered, reporter, sampling method, and **representativeness gaps** (which
   subgroups, severities, ages, regions, languages are missing). Social-media / unverified sources
   are hypothesis-generating only (self-selection, unverifiable diagnosis — G1 Table 3).
   Record `outputs.evidence_inventory`. Use `references/representativeness.md` for the checklist.

5. **Sampling plan for new work** (G1 §II.D, Table 2). Choose probability vs non-probability
   sampling per objective and constraint (rare disease → purposive/quota/snowball with stated
   limits; generalizing a prevalence → probability sampling from a frame such as a registry).
   Specify sampling frame and undercoverage risk, subgroups to represent (prespecify), target
   sample size — for qualitative work, **concept saturation** with a documented rule (see G2 App. 4)
   — and anticipated non-response/dropout (G1 §II.E.1). **⏸** Decision point: method + target n.

6. **Data management & operational plan** (G1 §III). Note that a written data management plan,
   discussion guide/observation form, trained interviewers, and FDA-supported data standards are
   expected; flag human-subjects/IRB needs. One short list in the dossier — do not draft an IRB
   package.

7. **AI-assisted checks** (label outputs as design-time):
   - *Coverage gap check*: compare the evidence inventory against the target population's
     heterogeneity dimensions (`references/representativeness.md`) and list uncovered cells.
   - *Plan lint*: flag convenience-only samples used to make population statements, missing
     reporter criteria, saturation claimed without a rule, subgroups not prespecified.
   - Optionally dispatch `patient-voice` and `caregiver-observer` agents to point out groups or
     settings the plan would miss (their output = prompts for real research, not evidence).

## Stage gate
Summarize (≤ 8 lines): research questions, reporter plan, strongest existing evidence, top
representativeness gaps, sampling plan. Set status `awaiting_gate`, render the dossier, then ask:
Approve & continue to G2 (Recommended when no blocking gap) · Revise G1 · Pause.
**Data stop:** if the user has no evidence at all yet, the recommended option is to proceed to G2
*to design* the concept-elicitation study, with G2's conclusions marked pending real data.

## References
- `references/sampling-and-reporters.md` — G1 Table 2 sampling types with limitations; self-report
  feasibility criteria; observer vs proxy.
- `references/representativeness.md` — heterogeneity dimensions checklist; saturation and sample size.
