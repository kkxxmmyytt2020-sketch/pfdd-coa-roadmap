"""Unit checks for the plugin scripts.  Run: python3 -m unittest discover -s scripts/tests"""
import csv
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import agreement  # noqa: E402
import lint_questions  # noqa: E402
import saturation  # noqa: E402


def rules(q):
    return {f["rule"] for f in lint_questions.lint(q) if f["level"] == "FLAG"}


def run_json(mod, argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        mod.main(argv + ["--json"])
    return json.loads(buf.getvalue())


def write_csv(rows, header):
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
    w = csv.writer(fh)
    w.writerow(header)
    w.writerows(rows)
    fh.close()
    return fh.name


class LintG2Examples(unittest.TestCase):
    """The four bad-question examples printed in FDA PFDD Guidance 2."""

    def test_leading_pad(self):
        q = ("Wouldn't you consider it most important to improve your walking distance, for example, "
             "how far you walk around the track when you exercise?")
        self.assertIn("leading", rules(q))

    def test_judging(self):
        self.assertIn("judging", rules("Could you tell me why you are not treating your condition with medication?"))

    def test_double_barreled(self):
        flags = lint_questions.lint("How embarrassed and self-conscious have you been because of your condition?")
        self.assertIn("double-barreled", {f["rule"] for f in flags})

    def test_double_negative(self):
        self.assertIn("double-negative", rules("I do not have symptoms that are not of concern."))

    def test_incomplete(self):
        self.assertIn("incomplete", rules("Age?"))

    def test_proxy_vs_observed(self):
        self.assertIn("proxy", rules("How severe was your child's pain from the time your child woke up until right now?"))
        self.assertNotIn("proxy", rules("In the last hour, how often did you see your child holding their stomach or abdomen?"))

    def test_good_questions_clean(self):
        for q in ["Tell me how peripheral artery disease impacts you. What would you like to see improve with treatment?",
                  "What did you consider when deciding whether to treat your condition with medication?",
                  "How embarrassed have you been because of your condition?"]:
            self.assertEqual(rules(q), set(), q)

    def test_jargon(self):
        self.assertIn("jargon", rules("How often do you experience dyspnea when climbing stairs?"))


class Agreement(unittest.TestCase):
    def test_textbook_kappa(self):
        # 2x2: both yes 20, A yes/B no 5, A no/B yes 10, both no 15 -> po=.70, pe=.50, kappa=.40
        a, b = [], []
        i = 0
        for x, y, n in [("yes", "yes", 20), ("yes", "no", 5), ("no", "yes", 10), ("no", "no", 15)]:
            for _ in range(n):
                a.append((f"s{i}", x)); b.append((f"s{i}", y)); i += 1
        pa, pb = write_csv(a, ["segment_id", "code"]), write_csv(b, ["segment_id", "code"])
        res = run_json(agreement, [pa, pb])
        self.assertEqual(res["n_segments"], 50)
        self.assertAlmostEqual(res["percent_agreement"], 0.70)
        self.assertAlmostEqual(res["kappa"], 0.40)
        self.assertEqual(res["top_disagreements"][0], {"codes": ["no", "yes"], "count": 15})


class Saturation(unittest.TestCase):
    def test_table7_layout_groups(self):
        """G2 Table 7 rows with unambiguous cells: Symptom A 5,4,3,3; B 4,3,5,3; C 3,4,4,3;
        F 4,3,5,4 (6 patients per group); Symptom G appears once in group 4 (fixture choice —
        the printed table's column placement for D/E/G is ambiguous)."""
        spec = {"Symptom A": [5, 4, 3, 3], "Symptom B": [4, 3, 5, 3], "Symptom C": [3, 4, 4, 3],
                "Symptom F": [4, 3, 5, 4], "Symptom G": [0, 0, 0, 1]}
        rows = []
        for g in range(4):
            for concept, counts in spec.items():
                for p in range(counts[g]):
                    rows.append([f"G{g+1}", g + 1, concept, f"G{g+1}-P{p+1}"])
        path = write_csv(rows, ["interview_id", "order", "concept", "participant_id"])
        res = run_json(saturation, [path, "--groups"])
        self.assertEqual(res["chunks"], ["Group 1", "Group 2", "Group 3", "Group 4"])
        for concept, counts in spec.items():
            self.assertEqual([res["grid"][concept][c] for c in res["chunks"]], counts, concept)
        self.assertEqual(res["new_by_chunk"]["Group 4"], ["Symptom G"])
        self.assertFalse(res["no_new_in_last_chunk"])

    def test_quartiles_and_beyond_plan(self):
        rows = [[f"I{i}", i, "itch"] for i in range(1, 9)] + [["I7", 7, "sleep loss"], ["I9", 9, "stigma"]]
        path = write_csv(rows, ["interview_id", "order", "concept"])
        res = run_json(saturation, [path, "--planned", "8"])
        self.assertEqual(res["chunks"], ["Q1", "Q2", "Q3", "Q4", "beyond plan"])
        self.assertEqual(res["first_seen"]["sleep loss"], "Q4")
        self.assertEqual(res["new_by_chunk"]["beyond plan"], ["stigma"])


if __name__ == "__main__":
    unittest.main()
