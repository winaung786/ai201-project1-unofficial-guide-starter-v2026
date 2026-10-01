"""Failure injection with synthetic fixtures; these are NOT live RAG results."""

from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import config
import eval_checkpoint
import generate
import questions
import run_eval


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.calls = 0
        self.tokens = {"prompt": 0, "output": 0, "total": 0}
        for context in (
            patch.object(config, "RESULTS_DIR", self.directory),
            patch.object(config, "REQUESTS_PER_MINUTE", 30),
            patch.object(generate, "call_count", side_effect=lambda: self.calls),
            patch.object(generate, "token_counts", side_effect=lambda: dict(self.tokens)),
            redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()),
        ):
            context.__enter__()
            self.addCleanup(context.__exit__, None, None, None)

    def fake_trial(self, question, *args):
        covered = question in {item["question"] for item in questions.answered()}
        if covered:
            self.calls += 1
            self.tokens["prompt"] += 10
            self.tokens["output"] += 2
            self.tokens["total"] += 12
        outcome = {
            "question": question, "answer": "SYNTHETIC TEST FIXTURE",
            "sources": [], "retrieved_sources": [], "refused": not covered,
            "refusal_reason": None if covered else "relevance_gate",
        }
        return outcome, [], SimpleNamespace(passed=covered, best_distance=0.2 if covered else 0.9), (
            outcome["answer"] if covered else None
        )

    def saved(self):
        path, = self.directory.glob("*.json")
        return path, json.loads(path.read_text())

    def test_fourteen_answers_survive_and_resume_skips_completed_trials(self):
        attempted = 0

        def fail_fifteenth(*args):
            nonlocal attempted
            attempted += 1
            if attempted == 15:
                self.calls += 1  # attempted request, but no returned token metadata
                raise RuntimeError("synthetic exhausted 429 retries")
            return self.fake_trial(*args)

        with patch.object(run_eval, "run_once", side_effect=fail_fifteenth), patch.object(
            run_eval, "load_scorer", return_value=lambda *args: True,
        ):
            self.assertEqual(run_eval.main(["--label", "recovery-fixture", "--requests-per-minute", "8"]), 1)
            path, state = self.saved()
            self.assertEqual(state["status"], "interrupted")
            self.assertEqual(len(state["covered_trials"]), 14)
            self.assertEqual(state["model_calls"], 15)
            self.assertEqual(state["token_counts"]["total"], 168)
            self.assertEqual(state["requests_per_minute"], 8)
            original_entries = state["covered_trials"]
            self.assertIn("pending", path.with_suffix(".md").read_text())

            # A fresh process has fresh session counters. The log retains prior usage.
            self.calls = 0
            self.tokens = {"prompt": 0, "output": 0, "total": 0}
            with patch.object(run_eval, "run_once", side_effect=self.fake_trial) as remaining:
                self.assertEqual(run_eval.main(["--resume", str(path), "--requests-per-minute", "4"]), 0)
                self.assertEqual(remaining.call_count, 16)  # one covered + fifteen gate trials
            _, state = self.saved()
            self.assertEqual(state["status"], "complete")
            self.assertEqual(state["covered_trials"][:14], original_entries)
            self.assertEqual(len(state["covered_trials"]), 15)
            self.assertEqual(len(state["out_of_scope_trials"]), 15)
            self.assertEqual(state["model_calls"], 16)  # fifteen successes + one failed attempt
            self.assertEqual(state["token_counts"]["total"], 180)
            self.assertEqual([s["requests_per_minute"] for s in state["sessions"]], [8, 4])

    def test_scorer_failure_keeps_raw_answer_and_resumes_without_regeneration(self):
        with patch.object(run_eval, "run_once", side_effect=self.fake_trial), patch.object(
            run_eval, "load_scorer", return_value=lambda *args: (_ for _ in ()).throw(ValueError("fixture")),
        ):
            self.assertEqual(run_eval.main(["--label", "scorer-fixture"]), 1)
        path, state = self.saved()
        raw = state["covered_trials"][0]
        self.assertEqual(raw["raw_model_answer"], "SYNTHETIC TEST FIXTURE")
        self.assertFalse(raw["scoring_complete"])
        with patch.object(run_eval, "run_once", side_effect=self.fake_trial) as remaining, patch.object(
            run_eval, "load_scorer", return_value=lambda *args: True,
        ):
            self.assertEqual(run_eval.main(["--resume", str(path)]), 0)
            self.assertEqual(remaining.call_count, 29)

    def test_resume_rejects_changed_settings_or_corpus_before_any_trial(self):
        with patch.object(run_eval, "run_once", side_effect=RuntimeError("fixture")):
            self.assertEqual(run_eval.main([]), 1)
        path, _ = self.saved()
        with patch.object(run_eval, "run_once") as trial:
            with self.assertRaisesRegex(ValueError, "top_k differs"):
                run_eval.main(["--resume", str(path), "--top-k", "7"])
            with patch.object(eval_checkpoint, "fingerprints", return_value={"changed": "hash"}):
                with self.assertRaisesRegex(ValueError, "pipeline code or corpus changed"):
                    run_eval.main(["--resume", str(path)])
            trial.assert_not_called()

    def test_atomic_write_failure_preserves_previous_checkpoint(self):
        path = self.directory / "checkpoint.json"
        eval_checkpoint.atomic_write(path, "previous evidence")
        with patch("eval_checkpoint.os.replace", side_effect=OSError("fixture")):
            with self.assertRaises(OSError):
                eval_checkpoint.atomic_write(path, "new evidence")
        self.assertEqual(path.read_text(), "previous evidence")
        self.assertEqual(list(self.directory.iterdir()), [path])


class RetryTests(unittest.TestCase):
    def test_429_retries_are_bounded_and_counted_as_attempts(self):
        response = SimpleNamespace(text="fixture", usage_metadata=SimpleNamespace(
            prompt_token_count=10, candidates_token_count=2,
        ))
        client = SimpleNamespace(models=SimpleNamespace())
        from unittest.mock import Mock
        client.models.generate_content = Mock(side_effect=[RuntimeError("429"), response])
        with patch.object(generate, "_get_client", return_value=client), patch.object(
            generate, "_wait_for_slot"
        ), patch.object(generate.time, "sleep") as sleep, patch.object(
            generate, "_session_calls", 0
        ), patch.object(generate, "_session_prompt_tokens", 0), patch.object(
            generate, "_session_output_tokens", 0
        ), patch.object(generate, "_call_times", []), redirect_stderr(io.StringIO()):
            self.assertEqual(generate.generate("fixture", cache=False), "fixture")
            self.assertEqual(generate.call_count(), 2)
            self.assertEqual(generate.token_counts()["total"], 12)
            sleep.assert_called_once_with(1)
            client.models.generate_content.side_effect = RuntimeError("429")
            with self.assertRaisesRegex(RuntimeError, "Still rate limited"):
                generate.generate("fixture", cache=False)
            self.assertEqual(client.models.generate_content.call_count, 2 + config.MAX_RETRIES)
            # No pointless backoff after the final exhausted attempt.
            self.assertEqual(sleep.call_count, config.MAX_RETRIES)

    def test_pacing_rejects_nonpositive_values(self):
        self.assertEqual(config.positive_int("8"), 8)
        for value in ("0", "-1", "word"):
            with self.assertRaises(ValueError):
                config.positive_int(value)


if __name__ == "__main__":
    unittest.main()
