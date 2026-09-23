#!/usr/bin/env python3
"""Render pfdd-state.json into a single self-contained HTML dossier.

    python3 render_dossier.py pfdd-state.json [-o pfdd-dossier.html]

One panel per guidance stage (G1–G4), plus the loop-back log and synthetic-artefact register.
The workflow figure (assets/workflow.png) is embedded so readers see what is behind the workflow.
Schema: skills/roadmap/references/state-schema.md.
"""
import argparse
import base64
import datetime as dt
import html
import json
import os
import sys

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURE = os.path.join(PLUGIN, "assets", "workflow.png")

STAGES = [
    ("g1", "G1 · Patient input", "Whose voice counts, and is it representative?", "--g1"),
    ("g2", "G2 · What matters", "What do patients say matters to them?", "--g2"),
    ("g3", "G3 · Fit-for-purpose COA", "What to measure, and with which COA?", "--g3"),
    ("g4", "G4 · COA-based endpoint", "How is a meaningful benefit read?", "--g4"),
]
STATUS_LABEL = {
    "not_started": "Not started", "in_progress": "In progress", "awaiting_input": "Waiting for data",
    "awaiting_gate": "Waiting for your approval", "approved": "Approved", "stale": "Needs re-check",
}
EVIDENCE_LABEL = {
    "real_patient_data": "Patient data", "literature": "Literature", "regulatory_precedent": "Regulatory precedent",
    "expert_input": "Expert input", "synthetic": "Synthetic · not patient evidence",
}

CSS = """
:root{--bg:#f6f7f9;--surface:#fff;--ink:#1f2328;--muted:#59636e;--rule:#d8dee4;
--g1:#2f6f9f;--g2:#8a5a00;--g3:#1a7f5a;--g4:#6e40aa;
--ok:#1a7f37;--ok-bg:#dafbe1;--warn:#9a6700;--warn-bg:#fff8c5;--bad:#cf222e;--bad-bg:#ffebe9;
--syn:#8250df;--syn-bg:#fbefff;--chip:#eaeef2}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0d1117;--surface:#161b22;
--ink:#e6edf3;--muted:#9198a1;--rule:#30363d;--g1:#58a6ff;--g2:#d29922;--g3:#3fb950;--g4:#bc8cff;
--ok:#3fb950;--ok-bg:#12261e;--warn:#d29922;--warn-bg:#272115;--bad:#f85149;--bad-bg:#25171c;
--syn:#bc8cff;--syn-bg:#231a33;--chip:#21262d}}
:root[data-theme="dark"]{--bg:#0d1117;--surface:#161b22;--ink:#e6edf3;--muted:#9198a1;--rule:#30363d;
--g1:#58a6ff;--g2:#d29922;--g3:#3fb950;--g4:#bc8cff;--ok:#3fb950;--ok-bg:#12261e;--warn:#d29922;
--warn-bg:#272115;--bad:#f85149;--bad-bg:#25171c;--syn:#bc8cff;--syn-bg:#231a33;--chip:#21262d}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
main{max-width:1180px;margin:0 auto;padding:28px 16px 64px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:0}h3{font-size:15px;margin:22px 0 8px}
.sub{color:var(--muted);margin:0 0 18px}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;color:var(--muted);font-size:13px;margin-bottom:18px}
.meta b{color:var(--ink);font-weight:600}
.track{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:16px 0 22px}
.track a{display:block;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--rule);
border-top:4px solid var(--c);border-radius:8px;padding:8px 10px;font-size:13px}
.track a span{display:block;color:var(--muted);font-size:12px}
details.fig{background:var(--surface);border:1px solid var(--rule);border-radius:10px;padding:10px 14px;margin-bottom:22px}
details.fig summary{cursor:pointer;font-weight:600}
details.fig img{width:100%;height:auto;margin-top:10px;border-radius:6px;background:#fff}
section.stage{background:var(--surface);border:1px solid var(--rule);border-radius:12px;margin:0 0 22px;overflow:hidden}
.stage>header{border-left:6px solid var(--c);padding:14px 18px;display:flex;justify-content:space-between;
align-items:flex-start;gap:12px;flex-wrap:wrap;border-bottom:1px solid var(--rule)}
.stage>header p{margin:2px 0 0;color:var(--muted);font-style:italic;font-size:14px}
.body{padding:4px 18px 18px}
.chip{display:inline-block;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:600;background:var(--chip);white-space:nowrap}
.chip.ok{background:var(--ok-bg);color:var(--ok)}.chip.warn{background:var(--warn-bg);color:var(--warn)}
.chip.bad{background:var(--bad-bg);color:var(--bad)}.chip.syn{background:var(--syn-bg);color:var(--syn)}
.tw{overflow-x:auto;margin:6px 0 4px}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{text-align:left;vertical-align:top;padding:7px 9px;border-bottom:1px solid var(--rule)}
th{font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);font-weight:600}
ul{margin:4px 0;padding-left:20px}
.empty{color:var(--muted);font-style:italic}
.dec{border:1px solid var(--rule);border-radius:8px;padding:8px 12px;margin:6px 0}
.dec summary{cursor:pointer}
.src{color:var(--muted);font-size:12.5px}
pre{white-space:pre-wrap;font-size:12.5px;background:var(--bg);padding:10px;border-radius:6px}
.mah{margin:4px 0 4px 0}.mah .mah{margin-left:18px}
footer{color:var(--muted);font-size:12.5px;margin-top:28px}
@media (max-width:720px){.track{grid-template-columns:repeat(2,1fr)}}
"""


def e(x):
    return html.escape("" if x is None else str(x))


def chip(text, kind=""):
    return f'<span class="chip {kind}">{e(text)}</span>'


def status_chip(status):
    kind = {"approved": "ok", "awaiting_gate": "warn", "awaiting_input": "warn", "stale": "bad"}.get(status, "")
    return chip(STATUS_LABEL.get(status, status or "Not started"), kind)


def evidence_chip(ev):
    if not ev:
        return ""
    return chip(EVIDENCE_LABEL.get(ev, ev), "syn" if ev == "synthetic" else "")


def rationale_chip(s):
    return chip({"supported": "Supported", "partial": "Partial", "gap": "Gap"}.get(s, s or "—"),
                {"supported": "ok", "partial": "warn", "gap": "bad"}.get(s, ""))


def fmt(v):
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, list):
        return ", ".join(e(i) for i in v)
    if isinstance(v, dict):
        return "<br>".join(f"<b>{e(k)}:</b> {fmt(val)}" for k, val in v.items())
    return e(v)


def table(rows, cols, render=None):
    """rows: list of dicts; cols: list of (key, header)."""
    if not rows:
        return '<p class="empty">Nothing recorded yet.</p>'
    render = render or {}
    head = "".join(f"<th>{e(h)}</th>" for _, h in cols)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(
            f"<td>{render[k](r.get(k)) if k in render else fmt(r.get(k))}</td>" for k, _ in cols) + "</tr>"
    return f'<div class="tw"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def kv(d):
    if not d:
        return '<p class="empty">Nothing recorded yet.</p>'
    return table([{"k": k, "v": v} for k, v in d.items()], [("k", "Item"), ("v", "Detail")])


def mah_tree(items):
    if not items:
        return '<p class="empty">Nothing recorded yet.</p>'
    by_parent = {}
    for m in items:
        by_parent.setdefault(m.get("parent") or None, []).append(m)

    def node(m):
        kids = by_parent.get(m.get("mah"), [])
        extra = []
        if m.get("concepts"):
            extra.append(f"<div class='src'>Concepts: {fmt(m['concepts'])}</div>")
        if m.get("patient_evidence"):
            extra.append(f"<div>Evidence: {fmt(m['patient_evidence'])}</div>")
        if m.get("importance"):
            extra.append(f"<div>Importance: {fmt(m['importance'])}</div>")
        badge = chip(m.get("level", ""), "") if m.get("level") else ""
        inner = "".join(extra) + "".join(node(k) for k in kids)
        return (f"<details class='dec mah' open><summary><b>{e(m.get('mah'))}</b> {badge} "
                f"{evidence_chip(m.get('evidence_type'))}</summary>{inner}</details>")

    roots = [m for m in items if not m.get("parent") or m.get("parent") not in {x.get("mah") for x in items}]
    return "".join(node(m) for m in roots)


def decisions(ds):
    if not ds:
        return '<p class="empty">No decisions recorded yet.</p>'
    out = []
    for d in ds:
        who = chip("You decided", "ok") if d.get("decided_by") == "user" else chip("Proposed — needs your confirmation", "warn")
        out.append(
            f"<details class='dec'><summary><b>{e(d.get('question'))}</b> — {e(d.get('answer'))} "
            f"{who} {evidence_chip(d.get('evidence_type'))}</summary>"
            f"<div class='src'>Sources: {fmt(d.get('sources', []))} · {e(d.get('date', ''))}</div></details>")
    return "".join(out)


def outputs_g1(o):
    s = "<h3>Research questions</h3>" + (
        "<ul>" + "".join(f"<li>{e(q)}</li>" for q in o.get("research_questions", [])) + "</ul>"
        if o.get("research_questions") else '<p class="empty">Nothing recorded yet.</p>')
    s += "<h3>Who reports</h3>" + table(o.get("reporter_plan"), [("subgroup", "Subgroup"), ("reporter", "Reporter"), ("rationale", "Rationale")])
    s += "<h3>Evidence inventory</h3>" + table(o.get("evidence_inventory"), [
        ("source", "Source"), ("type", "Type"), ("population_covered", "Population covered"),
        ("reporter", "Reporter"), ("representativeness_gaps", "Representativeness gaps")])
    s += "<h3>Sampling plan</h3>" + kv(o.get("sampling_plan"))
    return s


def outputs_g2(o):
    s = "<h3>Candidate MAH hierarchy</h3>" + mah_tree(o.get("mah_hierarchy"))
    lint = o.get("interview_guide_lint") or []
    s += "<h3>Interview-guide check</h3>" + table(lint, [("question", "Question"), ("flags", "Flags")],
                                                 {"flags": lambda f: fmt(f) if f else chip("OK", "ok")})
    s += "<h3>Saturation</h3>" + kv(o.get("saturation"))
    s += "<h3>Coder agreement</h3>" + kv(o.get("coder_agreement"))
    return s


def outputs_g3(o):
    s = "<h3>MAH selection</h3>" + table(o.get("mah_selection"), [("mah", "MAH"), ("selected", "Selected"), ("reasons", "Reasons")])
    s += "<h3>Table 1 · COA-based endpoint approach (G3 §III.D)</h3>" + table(o.get("table1"), [
        ("mah", "Meaningful aspect of health"), ("coi", "Concept of interest"), ("direct", "Direct?"),
        ("coa_type", "COA type"), ("coa_name", "COA"), ("score", "Score"), ("endpoint", "COA-based endpoint")])
    s += "<h3>Context of use</h3>" + kv(o.get("cou"))
    s += "<h3>Existing-COA landscape</h3>" + table(o.get("coa_landscape"), [
        ("coa", "COA"), ("coi", "COI measured"), ("cou_match", "COU match"), ("branch", "Branch"), ("notes", "Notes")],
        {"branch": lambda b: e({"a": "a · use", "b": "b · modify / add evidence", "c": "c · develop new"}.get(b, b))})
    s += "<h3>Evidence rationale A–H (G3 §IV, App. E)</h3>" + table(o.get("rationale"), [
        ("component", ""), ("claim", "Claim"), ("support", "Support"), ("status", "Status"), ("evidence_needed", "To close the gap")],
        {"status": rationale_chip})
    return s


def outputs_g4(o):
    s = "<h3>Endpoints</h3>" + table(o.get("endpoints"), [
        ("coa", "COA"), ("score", "Score"), ("construction", "Construction"), ("timing", "Timing"),
        ("role", "Role"), ("rationale", "Rationale")])
    s += "<h3>Meaningfulness plan (G4 §III)</h3>" + kv(o.get("meaningfulness_plan"))
    s += "<h3>Design risks (G4 §IV.A)</h3>" + table(o.get("design_risks"), [("risk", "Risk"), ("mitigation", "Mitigation"), ("source", "Source")])
    return s


RENDERERS = {"g1": outputs_g1, "g2": outputs_g2, "g3": outputs_g3, "g4": outputs_g4}
KNOWN = {
    "g1": {"research_questions", "reporter_plan", "evidence_inventory", "sampling_plan"},
    "g2": {"mah_hierarchy", "interview_guide_lint", "saturation", "coder_agreement"},
    "g3": {"mah_selection", "table1", "cou", "coa_landscape", "rationale"},
    "g4": {"endpoints", "meaningfulness_plan", "design_risks"},
}


def figure_block():
    if not os.path.exists(FIGURE):
        return ""
    b64 = base64.b64encode(open(FIGURE, "rb").read()).decode()
    return ("<details class='fig'><summary>What's behind this workflow (stages, sources, AI vs people)</summary>"
            f"<img alt='PFDD COA Roadmap workflow: four stages G1 to G4 with steps, sources and roles' "
            f"src='data:image/png;base64,{b64}'></details>")


def render(state):
    p = state.get("project", {})
    stages = state.get("stages", {})
    title = p.get("title") or p.get("indication") or "PFDD COA Roadmap"
    meta = "".join(f"<span>{e(lbl)}: <b>{e(p[k])}</b></span>" for k, lbl in [
        ("indication", "Indication"), ("population", "Population"), ("product", "Product"),
        ("phase", "Phase"), ("created", "Started")] if p.get(k))
    track = "".join(
        f"<a href='#{k}' style='--c:var({c})'>{e(name)}<span>{e(STATUS_LABEL.get(stages.get(k, {}).get('status', 'not_started')))}</span></a>"
        for k, name, _, c in STAGES)

    sections = []
    for k, name, q, c in STAGES:
        st = stages.get(k, {})
        o = st.get("outputs", {}) or {}
        gate = st.get("gate") or {}
        gate_line = (f"<p class='src'>Gate: {e(gate.get('decided_by', ''))} · {e(gate.get('date', ''))} · {e(gate.get('note', ''))}</p>"
                     if gate else "")
        extra = {kk: vv for kk, vv in o.items() if kk not in KNOWN[k]}
        extra_html = "".join(f"<h3>{e(kk)}</h3><pre>{e(json.dumps(vv, indent=2, ensure_ascii=False))}</pre>" for kk, vv in extra.items())
        oq = st.get("open_questions") or []
        oq_html = ("<h3>Open questions</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in oq) + "</ul>") if oq else ""
        sections.append(
            f"<section class='stage' id='{k}' style='--c:var({c})'><header><div><h2>{e(name)}</h2><p>{e(q)}</p></div>"
            f"{status_chip(st.get('status', 'not_started'))}</header><div class='body'>{gate_line}"
            f"<h3>Decisions</h3>{decisions(st.get('decisions'))}{RENDERERS[k](o)}{extra_html}{oq_html}</div></section>")

    loops = state.get("loopbacks") or []
    loop_html = table(loops, [("from", "From"), ("to", "Back to"), ("reason", "Reason"), ("date", "Date")])
    syn = state.get("synthetic_artifacts") or []
    syn_html = table(syn, [("id", "ID"), ("stage", "Stage"), ("what", "What"), ("file", "File")])

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · PFDD dossier</title><style>{CSS}</style></head><body><main>
<h1>{e(title)}</h1>
<p class="sub">PFDD COA Roadmap dossier: MAH → COI → fit-for-purpose COA → COA-based endpoint, one stage per FDA PFDD guidance.</p>
<div class="meta">{meta}</div>
<nav class="track" aria-label="Stages">{track}</nav>
{figure_block()}
{''.join(sections)}
<section class="stage" style="--c:var(--muted)"><header><div><h2>Loop-backs</h2><p>When a later stage reopened an earlier one</p></div></header><div class="body">{loop_html}</div></section>
<section class="stage" style="--c:var(--syn)"><header><div><h2>Synthetic artefacts</h2><p>Design-time checks only — never patient evidence</p></div>{chip('Not patient evidence', 'syn')}</header><div class="body">{syn_html}</div></section>
<footer>Rendered {e(now)} from pfdd-state.json · Sources: FDA PFDD Guidances 1–4; Walton et al. 2015; Powers et al. 2017; Cano &amp; Hobart 2011. Recommendations prepare for, and do not replace, FDA dialogue.</footer>
</main></body></html>"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("state")
    ap.add_argument("-o", "--out")
    args = ap.parse_args(argv)
    with open(args.state, encoding="utf-8") as fh:
        state = json.load(fh)
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.state)), "pfdd-dossier.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(render(state))
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
