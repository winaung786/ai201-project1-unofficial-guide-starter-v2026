"""Check that evaluation measures the real, uncached application outcome."""

import unittest
from unittest.mock import patch

import gate
import run_eval
import scorer
from store import Result


class EvaluationTests(unittest.TestCase):
    def test_week_two_scorer_uses_required_expected_phrase(self):
        self.assertTrue(
            scorer.judge(
                "How much printing credit?", "$30",
                "Each student gets $30 per semester.", [],
            )
        )
        self.assertFalse(
            scorer.judge(
                "How much printing credit?", "$30",
                "The answer does not state the amount.", [],
            )
        )

    def test_week_two_scorer_rejects_an_empty_expectation(self):
        self.assertFalse(scorer.judge("Question", "", "Any answer", []))

    def test_uncited_raw_answer_is_logged_but_user_sees_refusal(self):
        hit = Result(
            "Printing credit is $30.", "printing.txt", "printing.txt#0",
            0.25, "chunker.py::split_documents",
        )
        with patch("store.search", return_value=[hit]), patch(
            "generate.answer_from_chunks", return_value="Printing credit is $30."
        ) as model:
            outcome, results, decision, raw = run_eval.run_once(
                "How much printing credit?", 5, 0.6, "campus_life", "default"
            )

        model.assert_called_once_with("How much printing credit?", [hit], cache=False)
        self.assertEqual(raw, "Printing credit is $30.")
        self.assertEqual(outcome["answer"], gate.REFUSAL)
        self.assertEqual(outcome["refusal_reason"], "missing_source_citation")
        entry = run_eval.evidence(outcome, results, decision, raw, 2)
        self.assertEqual(entry["run"], 2)
        self.assertEqual(entry["retrieved_chunks"][0]["text"], hit.text)
        self.assertEqual(entry["retrieved_chunks"][0]["distance"], 0.25)
        self.assertEqual(entry["raw_model_answer"], raw)
        self.assertEqual(entry["answer"], gate.REFUSAL)


if __name__ == "__main__":
    unittest.main()
