# `pfdd-state.json` schema

One file per project, in the user's working folder. `scripts/render_dossier.py` reads it.

```json
{
  "project": {
    "title": "Pruritus in moderate-to-severe atopic dermatitis",
    "indication": "Atopic dermatitis, moderate-to-severe",
    "population": "Adults and children ≥2 years",
    "product": "Oral JAK1 inhibitor (hypothetical)",
    "mechanism": "Anti-inflammatory; rapid anti-pruritic effect expected",
    "phase": "Planning phase 2b/3",
    "created": "2026-09-22",
    "materials": ["FDA PFDD meeting report (AD, 2019)"]
  },
  "stages": {
    "g1": {
      "status": "approved",
      "gate": {"decided_by": "user", "date": "2026-09-22", "note": "OK, add adolescents"},
      "decisions": [
        {
          "id": "g1-reporter",
          "question": "Who reports for each age band?",
          "answer": "Self-report ≥12 y; caregiver-observed behaviours 2–11 y",
          "decided_by": "user",
          "sources": ["G1 §II.C", "G2 §VI"],
          "evidence_type": "literature",
          "date": "2026-09-22"
        }
      ],
      "outputs": {},
      "open_questions": ["Is a sampling frame available (registry)?"]
    },
    "g2": {"status": "not_started", "decisions": [], "outputs": {}, "open_questions": []},
    "g3": {"status": "not_started", "decisions": [], "outputs": {}, "open_questions": []},
    "g4": {"status": "not_started", "decisions": [], "outputs": {}, "open_questions": []}
  },
  "loopbacks": [
    {"from": "g3", "to": "g2", "reason": "Sleep-disturbance COI was never elicited from children", "date": "2026-09-23"}
  ],
  "synthetic_artifacts": [
    {"id": "syn-quotes-1", "stage": "g2", "what": "24 synthetic quotes for blind-coder QA", "file": "synthetic/g2-quotes.csv"}
  ]
}
```

## Field rules

- `status`: `not_started` | `in_progress` | `awaiting_input` (data stop) | `awaiting_gate` |
  `approved` | `stale` (an earlier stage was reopened after this one was approved).
- `decided_by`: `user` (the user chose/confirmed) or `proposed` (the plugin's recommendation,
  not yet confirmed). A stage cannot be `approved` while any decision is `proposed`.
- `evidence_type`: `real_patient_data` | `literature` | `regulatory_precedent` | `expert_input` |
  `synthetic`. `synthetic` can never be the sole support for a G1/G2 conclusion.
- `outputs` (by stage — the renderer knows these keys; extra keys are shown as JSON):
  - **g1**: `evidence_inventory` [{source, type, population_covered, reporter, representativeness_gaps}],
    `reporter_plan` [{subgroup, reporter, rationale}], `sampling_plan` {method, frame, target_n,
    saturation_rule, subgroups}, `research_questions` [str]
  - **g2**: `interview_guide_lint` [{question, flags}], `mah_hierarchy` [{mah, level (higher|lower),
    parent, concepts:[str], patient_evidence, importance}], `saturation` {file, new_by_chunk},
    `coder_agreement` {kappa, n_segments, disagreements}
  - **g3**: `mah_selection` [{mah, selected, reasons}], `table1` [{mah, coi, direct (bool),
    coa_type, coa_name, score, endpoint}], `cou` {population, use, implementation, design, schedule},
    `coa_landscape` [{coa, coi, cou_match (same|different|none), branch (a|b|c), notes}],
    `rationale` [{component (A–H), claim, support, status (supported|partial|gap), evidence_needed}]
  - **g4**: `endpoints` [{coa, score, construction, timing, role, rationale}],
    `meaningfulness_plan` {approach (MSD|MSR|both), anchors:[str], notes}, `design_risks` [{risk, mitigation, source}]
