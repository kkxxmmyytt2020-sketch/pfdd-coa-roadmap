---
type: llm
weight: 3
---

Judge the final response (the closing chat summary the user reads).
A successful run satisfies ALL of these:

1. G1: plans direct self-report for adults/adolescents and, for young children who cannot reliably
   self-report itch, a caregiver who reports **observed behaviour** (e.g., scratching) — not proxy
   report of the child's itch intensity.
2. G2: itch is a candidate MAH; sleep disturbance and/or skin pain also appear as candidate concepts.
   The evidence behind them is labelled literature/meeting report (not real interview data), and the
   need for real concept-elicitation interviews is stated.
3. G3: MAH itch → COI worst (or peak) itch intensity over ~24 hours, measured **directly** by a PRO
   (e.g., a 0–10 numeric rating scale daily diary); the existing-COA branch is "use existing" (a) or
   "use with additional evidence" (b) with a reason; for young children a separate ObsRO of
   scratching (or equivalent observable behaviour) is proposed and its component-H link to itch is
   flagged as needing evidence. An A–H rationale exists with at least one gap named.
4. G4: the meaningfulness plan is anchor-based (e.g., PGIS/PGIC) and states that distribution-based
   methods alone are insufficient; any responder threshold is to be prespecified and justified by
   patient input.
5. Every decision is marked proposed (not user-approved), no stage is marked approved, and the
   response ends with a list of questions for the user to decide.
6. Recommendations cite guidance sections (e.g., "G3 §III.C.3") and nothing claims fabricated
   psychometric results.

Score 1.0 if all six hold, deduct proportionally for each missed item, 0 if the workflow was not used.
