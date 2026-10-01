"""The summary must not present incomplete evidence as a completed evaluation."""

import json
from pathlib import Path
import tempfile
import unittest

import questions
from tools.summarize_evaluations import summarize


class SummaryTests(unittest.TestCase):
    def test_duplicate_or_missing_trials_are_incomplete(self):
        data = {
            "label": "SYNTHETIC TEST FIXTURE", "when_utc": "test fixture", "runs": 3,
            "answer_cache": False, "top_k": 1, "model_calls": 15,
            "token_counts": {"prompt": 100, "output": 20, "total": 120},
            "covered_trials": [{"question": q["question"], "run": run, "scorer_passed": True}
                               for q in questions.answered() for run in range(1, 4)],
            "out_of_scope_trials": [{"question": q, "run": run, "gate_refused": True}
                                    for q in questions.OUT_OF_SCOPE for run in range(1, 4)],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(data))
            self.assertEqual(summarize(path)["status"], "COMPLETE")
            data["covered_trials"][-1] = dict(data["covered_trials"][0])
            path.write_text(json.dumps(data))
            self.assertEqual(summarize(path)["status"], "INCOMPLETE")
            data["token_counts"]["total"] = 999
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "token arithmetic"):
                summarize(path)


if __name__ == "__main__":
    unittest.main()
