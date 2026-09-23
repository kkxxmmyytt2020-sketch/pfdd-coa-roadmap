# Representativeness, sample size, saturation (G1 §II.D.2–3, §II.E–F)

## Two meanings of "representative" (G1 §II.D.2)
1. **Generalizable** — statements from the sample extend to the target population (usually needs
   probability sampling; can be limited if subgroups are under-represented).
2. **Covers the heterogeneity** — the sample includes people spanning the population's range of
   characteristics. Often sufficient when the objective is to generate hypotheses or develop
   tools (e.g., concept elicitation for a new COA).

Regardless of selection method, the sample should represent the population on attributes
**associated with the endpoints of interest** (G1 §II.D.2).

## Heterogeneity checklist (use for the coverage-gap check)
For each dimension, mark covered / partly / missing in the evidence inventory:
- Disease: subtype/phenotype/genotype; severity; duration; stage; involvement of body regions
- Treatment history; current standard of care; concomitant care (Walton COU #4)
- Age bands (esp. pediatric bands by self-report ability); sex; race/ethnicity
- Language, culture, geography (region; urban/rural); health literacy; education
- Comorbidities; cognitive/sensory/motor impairments (accessibility, G3 §III.C.4)
- Reporter type (patient / caregiver / clinician) — keep separable
- Care setting (specialist centre vs community) and site diversity (G1 §III.A)

## Sample size (G1 §II.D.3)
Driven by objectives, outcome types, design (qualitative vs quantitative), planned analysis.
Adjust for drop-out/non-response; ensure enough information in prespecified subgroups (subgroups
by reporter type, demographics, clinical factors). If limited (rare disease), adjust objectives
and state limitations in the report.
- **Qualitative:** concept saturation — the point where no new important concepts emerge and the
  recruited group appears representative. Specify how saturation will be assessed and documented
  (G2 App. 4 gives a 25%-increment comparison; `scripts/saturation.py` computes it).
- **Quantitative:** standard sample-size formulae for the design; simulation for complex designs.

## Missing data / non-response (G1 §II.E.1)
Anticipate unit non-response, dropout, item non-response. Report a missing-data table
(frequencies, %, by subgroup, reasons; by visit for longitudinal data).

## Existing data (G1 §II.F.2)
FDA encourages leveraging registries, archival databases, literature — but you must show their
representativeness, methodological rigor, and data integrity. Unverified social-media data:
self-selection, unverifiable identity/diagnosis, representativeness "highly questionable without
strong assumptions" (G1 Table 3) → hypothesis-generating only.
