# Meaningful change and design considerations (G4 §III–IV; Powers GMP 7–8)

Statistical significance does not show that an effect is meaningful to patients (G4 §I.B).

## How interpretable are the scores already? (G4 §III.A)
1. **Directness of the COI** — current pain intensity (direct) is easy to read; pain behaviour
   (ObsRO) or leg strength (PerfO) needs empirical translation to daily experience.
2. **Metric** — natural units (night-time voids, metres) or a small ordinal scale shown in
   cognitive interviews to map to distinct experiences may need no more evidence; transformed
   scores (0–100 from 0–4) need evidence linking scores to experiences.

## Meaningful score differences — MSD (G4 §III.B.1)
- The size of difference patients would regard as meaningful (often within-patient change; can
  also come from vignette comparisons). Choose a **range** that reflects most patients.
- Uses: interpret the average treatment effect; threshold for descriptive individual-change analyses.
- Check assumptions: MSD constant across baseline scores? same for improvement and deterioration?
  (don't test baseline dependency by simple stratification on baseline — Terluin 2021).
- **Anchor-based methods**; **distribution-based methods (effect sizes, SD/SEM fractions) are
  insufficient alone** (no patient voice) — use as information on measurement variability. Other
  justified methods (e.g., Idio Scale Judgment) can be discussed with FDA.
- **Anchors:** use several; concept matches or includes the COI; plainly understood (cognitive
  interviews, including response options representing meaningfully different experiences);
  well-justified meaningful change on the anchor; demonstrated association with COA differences;
  comparable time points and recall periods. PGIC: evidence it reflects perceived change; beware
  recall error and present-state bias; not given at baseline. PGIS: given at baseline and follow-up;
  supports MSD (change in PGIS) or MSR.
- **Analyses:** check anchor variability; describe the COA–anchor relationship; show the
  distribution of COA changes at each anchor level (percentile table by baseline PGIS for patients
  with a 1-category improvement — G4 Table 1); decide which anchor change is meaningful first.
  Widen the threshold range when anchor–COA association is weak or distributions overlap, anchors or
  studies disagree, or subgroups differ.

## Meaningful score regions — MSR (G4 §III.B.2)
Divide the score range into regions corresponding to distinct experiences:
- COA score distributions by **PGIS** category → region boundaries (widths may differ);
- **Bookmarking** — patients/caregivers/clinicians sort experiences into a few ordinal categories;
- **Illustrative items** — a strongly associated, easy-to-read item from the COA as an internal
  anchor (e.g., "much difficulty" vs "little difficulty" climbing stairs at scores 40 vs 60);
- **IRT item parameters** — locate items on the metric to show what patients at each score can do
  (e.g., activities done "with no assistance"). This is where G3's construct theory and ordered
  item map pay off.

## Additional points (G4 §III.B.3)
Seek FDA input early; estimate before the registration trial. Report thresholds on raw and
transformed scales; for multi-item transformed scales, the MSD must be ≥ a one-category change on
at least one item. Rare disease / infeasible beforehand: exit interviews or surveys (masked trials,
after the main study, neutral interviewer; protocol to FDA early) — more bias-prone. Literature MSDs
need a comparability argument (disease, population, standard of care, region, calendar time, COA
version, endpoint, follow-up).

## Applying to trial results (G4 §III.C)
Prespecify methods and uncertainty (ranges, CIs). Continuous endpoints: MSD/MSR **aid
interpretation** (compare the effect and its CI with the MSD range; eCDF/ePDF of change by arm
annotated with MSD values and proportions exceeding them; examine across baseline if MSD varies).
Categorical/responder endpoints: MSD/MSR **define** the endpoint → a single prespecified threshold
(or set). Ordinal scales with few well-understood categories may need no extra work; many-level
ordinal scales → MSR work.

## Design considerations (G4 §IV.A)
- **Masking** of patients, clinicians, caregivers, raters; specify its extent in the protocol.
- **Practice effects** (esp. PerfO): check instrument evidence; space assessments; longer run-in with
  repeated practice; alternate forms. Unmasked or external-control designs can turn practice into bias.
- **Assistive devices:** follow COA instructions; otherwise incorporate device use into the
  endpoint if changing need is a treatment goal, or a supportive endpoint if not; record on CRF.
- **Nonrandomized / external / nonconcurrent controls:** expectation bias; different COAs, modes or
  schedules; baseline differences → prefer less subjective COIs, masked or automated PerfO scoring,
  standardized training and timing (ICH E10).
- **Post-baseline subgroups** break randomization.
- **CAT:** IRT parameters from the population of interest; model and algorithm checks; content
  coverage (hybrid CAT); may not beat a targeted short form when severity range is narrow.
- **Burden:** patient-community input on relevance, length, frequency; pilot procedures.
- **ClinRO operations** (Powers GMP 8): user manual, rater training and requalification, QA during
  data collection, local-language training materials.
