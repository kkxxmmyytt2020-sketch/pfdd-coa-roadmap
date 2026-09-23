"""Render the PFDD COA Roadmap workflow figure (assets/workflow.png).

Each column is one FDA PFDD guidance stage. Every step carries the section it
comes from, so users can see what is behind the workflow.

    python3 make_workflow_figure.py   # writes ../workflow.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent.parent / "workflow.png"

INK = "#1f2328"
MUTED = "#57606a"
RULE = "#d0d7de"
PAPER = "#ffffff"

STAGES = [
    {
        "key": "G1",
        "name": "Patient input",
        "question": "Whose voice counts, and is it representative?",
        "hue": "#2f6f9f",
        "tint": "#e8f1f8",
        "steps": [
            ("Research objectives → questions", "G1 §II.A–B, Fig. 1"),
            ("Target population; who reports", "G1 §II.C (self-report criteria)"),
            ("Sampling method & representativeness", "G1 §II.D, Table 2, Fig. 2"),
            ("Sample size / concept saturation", "G1 §II.D.3"),
            ("Leverage existing data; data mgmt plan", "G1 §II.F.2, §III"),
        ],
        "output": "Evidence inventory\n+ representativeness gaps",
        "sources": "G1 · Walton 2015 (COU)",
        "ai": "Map existing evidence, flag\ncoverage gaps, lint study plan",
        "human": "Recruit a real, representative\nsample of patients/caregivers",
    },
    {
        "key": "G2",
        "name": "What matters",
        "question": "What do patients say matters to them?",
        "hue": "#8a5a00",
        "tint": "#fbf1e0",
        "steps": [
            ("Background research first", "G2 §II.A"),
            ("Interviews / focus groups", "G2 §III.A, Tables 1 & 4"),
            ("Non-leading, single-concept questions", "G2 §III.B, §IV.B"),
            ("Observe behaviours, never proxy-report", "G2 §VI"),
            ("Coding dictionary, saturation, QA", "G2 App. 3–4, Table 7"),
        ],
        "output": "Candidate MAH hierarchy\nwith patient evidence",
        "sources": "G2 · G1",
        "ai": "Lint interview guide; blind-coder\nagreement (κ); saturation grid",
        "human": "Conduct interviews; code\nreal transcripts",
    },
    {
        "key": "G3",
        "name": "Fit-for-purpose COA",
        "question": "What to measure, and with which COA?",
        "hue": "#1a7f5a",
        "tint": "#e6f4ee",
        "steps": [
            ("Select MAH: meaningful, core, can change", "G3 §II.B.1, §III.B"),
            ("COI per MAH: direct ↔ indirect", "G3 §II.B.2 · Walton Fig. 1–2 · Powers"),
            ("Context of use", "G3 §II.B.3 · Walton (8 elements)"),
            ("COA type: PRO · ObsRO · ClinRO · PerfO", "G3 App. A–D · Powers (no CGA primary)"),
            ("Existing → use / modify / develop new", "G3 §III.C.2 · Cano & Hobart"),
            ("Evidence rationale A–H", "G3 §IV, App. E"),
        ],
        "output": "Table 1: MAH · COI · COA · score\n+ evidence gaps by component",
        "sources": "G3 · Walton · Powers · Cano & Hobart",
        "ai": "COA search, label check,\nreviewer agents, draft A–H",
        "human": "FDA dialogue; qualitative and\npsychometric studies",
    },
    {
        "key": "G4",
        "name": "COA-based endpoint",
        "question": "How is a meaningful benefit read?",
        "hue": "#6e40aa",
        "tint": "#f1ebf8",
        "steps": [
            ("Endpoint rationale & construction", "G4 §II.A.1–2"),
            ("Multi-aspect: separate / multi-comp. / personalized", "G4 §II.A.2.e"),
            ("Timing, estimand, missing data", "G4 §II.A.3, §II.B"),
            ("Meaningful change: MSD (anchors) / MSR", "G4 §III.B–C"),
            ("Design risks: masking, practice, devices, CAT", "G4 §IV.A · Powers"),
        ],
        "output": "Endpoint definition\n+ meaningfulness plan",
        "sources": "G4 · Powers · Cano & Hobart",
        "ai": "Option trade-offs, anchor\nplan, risk checklist",
        "human": "FDA dialogue; anchor\nstudies; trial data",
    },
]

LOOPS = [  # (from stage index, to stage index, label)
    (1, 0, "under-represented subgroup"),
    (2, 1, "COI never elicited"),
    (3, 2, "effect dilution / heterogeneity"),
]

W, H = 20.0, 11.9
COL_W, GAP, LEFT = 4.45, 0.55, 0.35

HEAD_TOP, HEAD_H = 10.55, 1.05
STEP_TOP, STEP_H = 9.35, 3.95
OUT_TOP, OUT_H = 5.25, 0.95
SRC_TOP, SRC_H = 4.15, 0.45
ROLE_TOP, ROLE_H = 3.55, 1.2


def box(ax, x, y_top, w, h, face, edge=None, lw=1.0, r=0.12, hatch=None):
    ax.add_patch(FancyBboxPatch(
        (x, y_top - h), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=face, edgecolor=edge or face, linewidth=lw, hatch=hatch,
    ))


def main():
    plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
    fig = plt.figure(figsize=(W, H - 0.8), dpi=160)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0.8, H)
    ax.axis("off")
    fig.patch.set_facecolor(PAPER)

    ax.text(LEFT, 11.4, "PFDD COA Roadmap: from patient voice to a meaningful endpoint",
            fontsize=20, weight="bold", color=INK, va="center")
    ax.text(LEFT, 10.98,
            "One stage per FDA PFDD guidance. Each step shows the section it comes from; "
            "the bottom rows show what AI assists with and what still needs real people.",
            fontsize=11.5, color=MUTED, va="center")

    xs = [LEFT + i * (COL_W + GAP) for i in range(len(STAGES))]

    for i, (s, x) in enumerate(zip(STAGES, xs)):
        # header
        box(ax, x, HEAD_TOP, COL_W, HEAD_H, s["hue"])
        ax.text(x + 0.2, HEAD_TOP - 0.36, f'{s["key"]}  {s["name"]}',
                fontsize=15, weight="bold", color="white", va="center")
        ax.text(x + 0.2, HEAD_TOP - 0.78, s["question"],
                fontsize=10.5, color="white", va="center", style="italic")

        # steps
        box(ax, x, STEP_TOP, COL_W, STEP_H, s["tint"])
        n = len(s["steps"])
        pitch = (STEP_H - 0.25) / n
        for j, (step, cite) in enumerate(s["steps"]):
            y = STEP_TOP - 0.22 - j * pitch
            ax.add_patch(plt.Circle((x + 0.3, y - 0.17), 0.13, color=s["hue"]))
            ax.text(x + 0.3, y - 0.17, str(j + 1), fontsize=8.5, color="white",
                    ha="center", va="center", weight="bold")
            ax.text(x + 0.55, y - 0.1, step, fontsize=10.2, color=INK, va="center")
            ax.text(x + 0.55, y - 0.4, cite, fontsize=8.6, color=MUTED, va="center")

        # output
        box(ax, x, OUT_TOP, COL_W, OUT_H, PAPER, edge=s["hue"], lw=1.8)
        ax.text(x + 0.2, OUT_TOP - 0.2, "DECISION OUTPUT", fontsize=7.8,
                color=s["hue"], weight="bold", va="center")
        ax.text(x + 0.2, OUT_TOP - 0.6, s["output"], fontsize=10.2, color=INK,
                va="center", weight="bold", linespacing=1.25)

        # sources
        ax.text(x + 0.2, SRC_TOP - SRC_H / 2, "Sources:  " + s["sources"],
                fontsize=9.2, color=MUTED, va="center")

        # AI vs human
        half = (COL_W - 0.12) / 2
        box(ax, x, ROLE_TOP, half, ROLE_H, "#f6f8fa", edge=RULE)
        box(ax, x + half + 0.12, ROLE_TOP, half, ROLE_H, PAPER, edge=RULE, hatch="////")
        ax.text(x + 0.15, ROLE_TOP - 0.22, "AI ASSISTS", fontsize=7.8, color=INK,
                weight="bold", va="center")
        ax.text(x + 0.15, ROLE_TOP - 0.68, s["ai"], fontsize=8.8, color=INK,
                va="center", linespacing=1.3)
        hx = x + half + 0.12
        ax.text(hx + 0.15, ROLE_TOP - 0.22, "NEEDS REAL PEOPLE / DATA",
                fontsize=7.8, color=INK, weight="bold", va="center",
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.2))
        ax.text(hx + 0.15, ROLE_TOP - 0.68, s["human"], fontsize=8.8, color=INK,
                va="center", linespacing=1.3,
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5))

        # forward arrow to next stage
        if i < len(STAGES) - 1:
            ax.add_patch(FancyArrowPatch(
                (x + COL_W + 0.04, HEAD_TOP - HEAD_H / 2),
                (x + COL_W + GAP - 0.04, HEAD_TOP - HEAD_H / 2),
                arrowstyle="-|>", mutation_scale=18, color=INK, lw=1.6))

    # loop-backs, drawn under the columns
    base = ROLE_TOP - ROLE_H - 0.15
    for k, (a, b, label) in enumerate(LOOPS):
        xa = xs[a] + COL_W * 0.3
        xb = xs[b] + COL_W * 0.7
        ax.add_patch(FancyArrowPatch(
            (xa, base), (xb, base),
            connectionstyle="arc3,rad=-0.3", arrowstyle="-|>",
            mutation_scale=15, color=MUTED, lw=1.3, linestyle=(0, (4, 3))))
        ax.text((xa + xb) / 2, base - 0.55, label, fontsize=9.2, color=MUTED,
                ha="center", va="center", style="italic",
                bbox=dict(facecolor=PAPER, edgecolor="none", pad=1.5))
    ax.text(LEFT, 1.2, "↺  Dashed arrows: loop-backs. A later stage can reopen an earlier "
            "one; every loop-back is logged in the dossier.",
            fontsize=9.5, color=MUTED, va="center")
    ax.text(W - LEFT, 1.2,
            "Synthetic quotes and persona agents are design-time checks, never patient evidence.",
            fontsize=9.5, color=INK, va="center", ha="right", weight="bold")

    fig.savefig(OUT, dpi=160, facecolor=PAPER)
    print(OUT)


if __name__ == "__main__":
    main()
