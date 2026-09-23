# Endpoint construction (G4 §II; Powers GMP 6; Walton "Relationship between assessments and endpoints")

An assessment is not an endpoint. An endpoint = the COA + number and timing of assessments + how
scores are combined + the analysis comparing groups (Walton; Powers). The same COA can yield very
different endpoints (Powers' skin-lesion example: time to resolution; time to 20% reduction;
responder proportion at day 3; mean area at a time point).

## Describe (G4 §II.A.1)
COA type · COA · specific score(s) · algorithm for multi-component endpoints · missing item/task
rule · timing, aggregation window, how scores within the period are combined (e.g., mean of daily
scores in the 7 days before week 12) · baseline definition.

## Justify (G4 §II.A.1)
COI · specific objective/hypothesis ("compare patient-reported physical functioning between arms at
week 12", not "compare PROs") · role (primary/secondary/other) and place in the endpoint hierarchy
(Powers) · intended indication · why the COA is fit-for-purpose (G3) · importance to patients
(literature/primary data; e.g., patients ranking candidate endpoints — Stone 2021) · components and
algorithm for multi-component endpoints · strengths and limitations. Prior use in another trial is
not sufficient support (COU differs; science and policy evolve).

## Options and pitfalls (G4 §II.A.2)
| Construction | Use when | Pitfalls |
|---|---|---|
| Score at a fixed time point, baseline-adjusted | Default for ordinal/continuous scores; score not highly variable; time point reflects durability | Justify the time point; align with recall period |
| Summary over a period (mean, worst/max, min) or repeated-measures model | Daily diaries, fluctuating symptoms | Robustness of the summary, missing days, power, interpretability |
| Dichotomized ("responder") | Well-established, clearly meaningful health states (e.g., clear/almost clear) | Loses information/power; single prespecified threshold justified by patients; derived from data other than the registration trial; sensitivity over a range of thresholds |
| Change from baseline | Aids interpretation; single-arm studies | Ordinal differences not equal-interval; better as model-derived predicted change |
| Percent change | Multiplicative effects | Asymmetric (+100% vs −50%), undefined at 0, non-normal → consider log transform |
| Time to event from a COA threshold | Resolution/progression questions | Same threshold justification as dichotomies; assessment frequency must resolve time differences |

Baseline: multiple baseline measurements need a defined rule; don't use the screening score as
baseline; account for run-in changes.

## Several aspects of health (G4 §II.A.2.e)
| Strategy | Good for | Watch |
|---|---|---|
| Separate endpoints (1 primary + secondaries; multiple primary; co-primary) | One cardinal manifestation most patients have | Unknown which aspects will improve; multiplicity; dilution by patients without the symptom |
| Multi-component (within-patient algorithm) | Variable manifestations; concordant effects; no multiplicity adjustment | Explicit, justified weights; dilution when averaging unaffected components; thresholds and rater awareness of them; symmetric −1/0/+1 scoring assumption; examine components |
| Personalized (most bothersome symptom; Goal Attainment Scaling) | Heterogeneous diseases; very patient-focused; no dilution | Choosing one symptom is hard; choices drift; may pick untargeted/unrealistic goals; misses new symptoms → measure all symptoms in everyone; standardize elicitation |

Item-level components of a single COA are only valid components if the COA follows a composite-
indicator model (G3 §IV.E). Composite *measurement model* ≠ composite *endpoint* (G3 fn 38).

## Timing (G4 §II.A.3)
Natural course; research question; duration; burden; disease stage; when the product is expected
to act; interruptions/discontinuation; same rules across arms; event-triggered data with windows
and end-of-day completeness prompts; spacing matched to the expected rate of change; frequent
enough for time-to-event; continue collecting after treatment discontinuation.

## Estimation and missing data (G4 §II.B)
Baseline-adjusted comparisons (covariate-adjustment guidance); longitudinal models with a
prespecified contrast; ordinal endpoints — cumulative logistic models vs dichotomies, interpretable
results, explore assumption violations; ordinal multi-component endpoints can hide harm (symptom
benefit vs mortality) — consult FDA. Missing data: minimize (only necessary COAs, low burden,
reminders, site follow-up), collect reasons, distinguish intercurrent events (ICH E9(R1)); item-level
missingness per the scoring algorithm; form-level missingness per the estimand with sensitivity
analyses.
