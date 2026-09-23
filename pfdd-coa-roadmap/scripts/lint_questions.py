#!/usr/bin/env python3
"""Screen interview/survey questions against FDA PFDD Guidance 2 question rules.

Heuristic screen, not a verdict: every FLAG needs a human look (G2 §III.B, §IV.B; G3 App. B).

    python3 lint_questions.py guide.txt            # one question per line; '#' lines ignored
    python3 lint_questions.py guide.txt --json

Levels: FLAG = very likely violates a rule; CHECK = review whether it does.
"""
import argparse
import json
import re
import sys

NEGATIONS = re.compile(
    r"\b(not|no|never|none|nobody|nothing|neither|nor|without)\b|n't\b", re.I)

LEADING = [
    re.compile(r"\b(wouldn't|won't|don't|doesn't|isn't|aren't|didn't|shouldn't|can't|couldn't)\s+(you|it|that|this)\b", re.I),
    re.compile(r"\bwould(n't)?\s+you\s+agree\b", re.I),
    re.compile(r"\bisn't\s+it\s+true\b", re.I),
    re.compile(r"\b(surely|obviously|of course)\b", re.I),
]
SUGGESTED_EXAMPLE = re.compile(r"\b(for example|e\.g\.|such as|like when)\b", re.I)
JUDGING = [
    re.compile(r"\bwhy\b[^?.]*\b(not|n't)\b", re.I),
    re.compile(r"\bwhy\s+(did|do|would|are)\s+you\s+(choose|decide|refuse|stop|skip|fail)", re.I),
]
PAIR = re.compile(r"\b([a-z]+(?:ed|ing|ful|ous|ive|al|ic|y|less|ble|ant|ent)?)\s+(and|or|and/or)\s+([a-z]+)\b", re.I)
PAIR_STOP = {"the", "a", "an", "your", "my", "his", "her", "their", "our", "other", "others",
             "so", "then", "how", "what", "when", "why", "you", "i", "we", "they", "it"}
JARGON = {
    "dyspnea": "shortness of breath", "dyspnoea": "shortness of breath",
    "pruritus": "itch / itching", "pruritic": "itchy", "nocturia": "waking up at night to urinate",
    "dysuria": "pain or burning when urinating", "dysphagia": "trouble swallowing",
    "emesis": "vomiting", "pyrexia": "fever", "cephalalgia": "headache", "arthralgia": "joint pain",
    "myalgia": "muscle pain", "paresthesia": "tingling / pins and needles",
    "paraesthesia": "tingling / pins and needles", "erythema": "redness", "edema": "swelling",
    "oedema": "swelling", "syncope": "fainting", "ambulation": "walking", "ambulate": "walk",
    "somnolence": "sleepiness", "xerosis": "dry skin", "lesion": "sore / patch / spot",
    "exacerbation": "flare / worsening", "adls": "everyday activities (name them)",
    "activities of daily living": "everyday activities (name them)",
    "comorbidity": "other health conditions", "comorbidities": "other health conditions",
}
ABSTRACT = re.compile(r"\b(quality of life|well-being|wellbeing|functioning|functional status|health status)\b", re.I)
PROXY_SUBJECT = re.compile(
    r"\b(your|my|the)\s+(child|son|daughter|baby|infant|kid|husband|wife|partner|spouse|mother|father|"
    r"parent|loved one|patient|relative)('s)?\b", re.I)
INNER_STATE = re.compile(
    r"\b(pain\w*|itch\w*|tired\w*|fatigue\w*|sad\w*|feel\w*|felt|mood|anxi\w*|nause\w*|worr\w*|"
    r"depress\w*|lonely|embarrass\w*|frustrat\w*|scared|afraid|breathless\w*|dizz\w*|severity|severe)\b", re.I)
OBSERVED = re.compile(r"\b(see|saw|seen|notice\w*|observ\w*|hear|heard|say|said|tell|told|watch\w*|do|did)\b", re.I)
VAS = re.compile(r"\b(visual analog(ue)? scale|VAS|mark on the line|place a mark)\b", re.I)


def lint(question):
    q = question.strip()
    flags = []
    words = re.findall(r"[A-Za-z']+", q)

    if len(words) < 3:
        flags.append(("FLAG", "incomplete", "Incomplete question — write a full sentence (G2 §IV.B)."))

    if any(p.search(q) for p in LEADING):
        flags.append(("FLAG", "leading", "Leading — implies the expected answer (G2 §III.B). Ask openly, e.g. 'Tell me how … affects you.'"))
    elif SUGGESTED_EXAMPLE.search(q) and re.search(r"\b(important|most|improve|worse|better)\b", q, re.I):
        flags.append(("CHECK", "leading", "Example inside an evaluative probe may steer the answer (G2 §III.B)."))

    if any(p.search(q) for p in JUDGING):
        flags.append(("FLAG", "judging", "May cast judgment on a choice (G2 §III.B). Try 'What did you consider when …?'"))

    negs = len(NEGATIONS.findall(q))
    if negs >= 2:
        flags.append(("FLAG", "double-negative", f"{negs} negations — rephrase positively (G2 §IV.B)."))

    for m in PAIR.finditer(q):
        left, right = m.group(1).lower(), m.group(3).lower()
        if left in PAIR_STOP or right in PAIR_STOP:
            continue
        flags.append(("CHECK", "double-barreled",
                      f"'{m.group(0)}' — does this ask about two concepts? Split if so (G2 §IV.B)."))
        break

    low = q.lower()
    for term, plain in JARGON.items():
        if re.search(r"\b" + re.escape(term) + r"\b", low):
            flags.append(("FLAG", "jargon", f"'{term}' → '{plain}' (G2 App. 3 Table 5)."))

    if ABSTRACT.search(q):
        flags.append(("CHECK", "abstract", "Abstract concept — frame within the person's concrete experience (G2 App. 3)."))

    if PROXY_SUBJECT.search(q) and INNER_STATE.search(q) and not OBSERVED.search(q):
        flags.append(("FLAG", "proxy",
                      "Asks someone else to report the patient's inner experience (proxy). Ask what they observe instead (G3 App. B; G2 §VI)."))

    if VAS.search(q):
        flags.append(("FLAG", "vas", "Visual analog scale — FDA generally does not recommend; use a verbal or 0–10 numeric scale (G3 §IV.E.1)."))

    return [{"level": lv, "rule": rule, "message": msg} for lv, rule, msg in flags]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text file, one question per line ('-' for stdin)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    args = ap.parse_args(argv)

    fh = sys.stdin if args.file == "-" else open(args.file, encoding="utf-8")
    questions = [ln.strip() for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
    results = [{"question": q, "flags": lint(q)} for q in questions]

    if args.json:
        json.dump(results, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 0

    n_flag = sum(1 for r in results for f in r["flags"] if f["level"] == "FLAG")
    n_check = sum(1 for r in results for f in r["flags"] if f["level"] == "CHECK")
    for i, r in enumerate(results, 1):
        mark = "ok " if not r["flags"] else "!! "
        print(f"{mark}{i:>3}. {r['question']}")
        for f in r["flags"]:
            print(f"        [{f['level']}] {f['rule']}: {f['message']}")
    print(f"\n{len(results)} questions · {n_flag} FLAG · {n_check} CHECK "
          "(heuristic screen — review every flag)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
