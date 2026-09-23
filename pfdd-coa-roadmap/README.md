# pfdd-coa-roadmap — plugin reference

A human-gated, AI-assisted workflow through the four FDA Patient-Focused Drug Development (PFDD)
guidances. It helps a team decide, and justify, **what to measure in a clinical trial and how**:

> **MAH** (meaningful aspect of health) → **COI** (concept of interest) → **COA** that is
> *fit-for-purpose* in its context of use → **COA-based endpoint**

"Fit-for-purpose" describes a COA **within a context of use**: its level of validation is
sufficient for that context (G3 §II.C). A fit-for-purpose COA is necessary but not sufficient for
a good endpoint (G4 §I.B).

![workflow](assets/workflow.png)

---

## Stages

| Stage | Skill | Question | Decides | Built from |
|---|---|---|---|---|
| **G1** | `g1-patient-input` | Whose voice counts, and is it representative? | Research questions, who reports (self vs observed-by-caregiver), sampling plan, evidence inventory and representativeness gaps | PFDD G1 · Walton 2015 |
| **G2** | `g2-what-matters` | What do patients say matters to them? | Interview guide (linted), coding dictionary, saturation, coder agreement, **candidate MAH hierarchy** | PFDD G2 · G1 |
| **G3** | `g3-fit-for-purpose-coa` | What to measure, and with which COA? | MAH selection → COI (direct/indirect) → context of use → COA type → use / modify / develop → **A–H rationale** → **Table 1** | PFDD G3 · Walton 2015 · Powers 2017 · Cano & Hobart 2011 |
| **G4** | `g4-coa-endpoint` | How is a meaningful benefit read? | Endpoint construction, multi-aspect strategy, timing and estimand, **meaningful-change plan** (MSD/MSR), design-risk register | PFDD G4 (draft) · Powers 2017 |

`roadmap` is the entry point. It shows the workflow figure, keeps the project state, enforces the
gates and routes to the stage skills. Later stages can **loop back**. For example, a COI that
patients never raised reopens G2, and each loop-back is logged.

## How it pauses and asks you

The workflow pulses: it does a bounded piece of work, shows the result, then asks.

| Pause | When |
|---|---|
| **Intake** | New project: indication, population, product and mechanism, phase, existing materials |
| **Decision point** | Inside a stage, wherever the guidance leaves a real choice |
| **Data stop** | A step needs real data (transcripts, coded data, psychometric or anchor results) |
| **Stage gate** | End of each stage: approve · revise · loop back · pause |

- A stage cannot start until the previous gate is `approved` in `pfdd-state.json`.
- Subagents never ask you anything; only the main conversation does.
- **Unattended draft** (only if you ask for it): all stages are drafted, every decision is marked
  `proposed`, nothing is approved, and the closing summary lists every question you still need to
  answer, with a recommended option and a section citation for each.

## Usage

```text
/pfdd-coa-roadmap:roadmap
```
Or describe the task in plain language, for example:
- "Help me choose the COA for itch in atopic dermatitis, including toddlers."
- "Lint my concept-elicitation interview guide." → G2 directly
- "Is the 6-minute walk test fit-for-purpose for our DMD trial?" → G3 directly
- "Draft all four stages for our program without asking me; list what I need to decide."

### Files it writes (in your working folder)
| File | What |
|---|---|
| `pfdd-state.json` | Project state: decisions (who decided, sources, evidence type), stage outputs, loop-backs, synthetic artefacts. Schema: `skills/roadmap/references/state-schema.md` |
| `pfdd-dossier.html` | Single-file dossier with one panel per stage, Table 1, the A–H rationale with supported/partial/gap badges, the endpoint plan, the loop-back log and the embedded workflow figure |

A worked example state is `skills/roadmap/references/example-state.json`.

## Agents (design-time reviewers)

| Agent | Role |
|---|---|
| `patient-voice` | Lived-experience critique of plans, guides, hierarchies, items |
| `caregiver-observer` | Checks observable-behaviour framing vs proxy report |
| `clinical-expert` | Disease model, core vs distal, COI plausibility, site feasibility |
| `fda-coa-reviewer` | Regulatory-science read of G3/G4 against the guidances |
| `psychometrician` | Construct theory, measurement model, scoring, reliability, DIF, IRT maps |
| `biostatistician` | Endpoint construction, estimands, missing data, MSD analyses |
| `blind-coder` | Independent second coder; sees only code definitions, never the labels |

Persona output is labelled **synthetic — not patient evidence**. It can sharpen a plan, but it never
supports a conclusion about what matters to patients.

## Scripts (Python standard library only)

```bash
S=scripts   # inside the plugin folder

# G2: screen questions (one per line) for leading, judging, double-barreled,
#     double-negative, jargon, incomplete, proxy and VAS wording
python3 $S/lint_questions.py guide.txt [--json]

# G2: saturation grid in 25% chunks of planned interviews, or one chunk per focus group
python3 $S/saturation.py coded.csv --planned 30 [--json]    # columns: interview_id,order,concept[,participant_id]
python3 $S/saturation.py groups.csv --groups

# G2: inter-coder agreement (Cohen's kappa, per-code kappa, most-confused pairs)
python3 $S/agreement.py primary.csv blind.csv [--json]      # columns: segment_id,code

# Render the dossier from the state file
python3 $S/render_dossier.py pfdd-state.json [-o pfdd-dossier.html]

# Regenerate the workflow figure after changing stage content
python3 assets/src/make_workflow_figure.py
```

## Tests and evals

```bash
python3 -m unittest discover -s scripts/tests          # 11 unit tests
claude plugin validate .
claude plugin eval . --runs 1 --ablation none \
  --allow-tools Bash Write Edit --trust-plugin --no-publish
```
- **Unit tests:** the linter flags all four bad-question examples from G2. The kappa script
  reproduces a textbook value (0.40). The saturation grid reproduces the layout of G2 Table 7.
- **Eval cases:**
  - `evals/ad-itch`: direct PRO for itch, plus an ObsRO of scratching for young children.
  - `evals/dmd-ambulation`: indirect PerfO COIs, the component-H burden, practice effects,
    assistive devices, and the risks of an external control.

## Sources

| Key | Document |
|---|---|
| G1 | FDA PFDD Guidance 1, *Collecting Comprehensive and Representative Input* (2020) |
| G2 | FDA PFDD Guidance 2, *Methods to Identify What Is Important to Patients* (2022) |
| G3 | FDA PFDD Guidance 3, *Selecting, Developing, or Modifying Fit-for-Purpose COAs* (2025) |
| G4 | FDA PFDD Guidance 4 (draft), *Incorporating COAs Into Endpoints for Regulatory Decision-Making* |
| Walton 2015 | *Clinical Outcome Assessments: Conceptual Foundation*, Value Health 18:741–752 |
| Powers 2017 | *ClinRO Assessments of Treatment Benefit*, Value Health 20:2–14 |
| Cano & Hobart 2011 | *The problem with health measurement*, Patient Pref Adherence 5:279–290 |

The FDA guidances are public domain. The journal articles are paraphrased and cited, not bundled.
This plugin prepares for FDA dialogue; it does not replace it or give regulatory advice.

## Versioning

Bump `version` in `.claude-plugin/plugin.json` on every change. Installed copies only update when
the version changes:
```bash
claude plugin marketplace update pfdd-local
claude plugin update pfdd-coa-roadmap@pfdd-local
```

| Version | Changes |
|---|---|
| 0.1.2 | Plugin-level README |
| 0.1.1 | Unattended-draft summary must stand on its own with citations; PerfO endpoints always carry practice-effect and assistive-device risks |
| 0.1.0 | First release: 5 skills, 7 agents, 4 scripts, workflow figure, 2 eval cases |
