"""Regression checks for chunk boundaries and the pre-generation gate.

Run with: python -m unittest discover -s tests -v
Model calls and retrieval are mocked only in pipeline control-flow tests.
"""
import unittest
from unittest.mock import patch

import app
import config
import gate
from chunker import split_documents
from ingest import Document, clean_text, load_documents
from serve import app as web_app
from store import Result


class ChunkTests(unittest.TestCase):
    def test_short_post_keeps_title_and_paragraphs(self):
        doc = Document("laundry.txt", "Laundry\n\nWash costs $1.75.\n\nPay by card.")
        chunks = split_documents([doc])
        self.assertEqual([c.text for c in chunks], [doc.text])
        self.assertEqual(chunks[0].label, "laundry.txt#0")
        self.assertEqual(chunks[0].produced_by, "chunker.py::split_documents")

    def test_long_post_keeps_every_sentence_and_repeats_title(self):
        sentences = ["Wash costs $1.75.", "Pay with a card.", "Dryers cost $1.50.", "Avoid Sunday nights."]
        doc = Document("laundry.txt", "Laundry\n\n" + " ".join(sentences))
        with patch.object(config, "CHUNK_SIZE", 55), patch.object(config, "CHUNK_OVERLAP", 20):
            chunks = split_documents([doc])
        self.assertGreater(len(chunks), 1)
        for sentence in sentences:
            self.assertTrue(any(sentence in c.text for c in chunks), sentence)
        for c in chunks:
            self.assertTrue(c.text.startswith("Laundry\n\n"))
            self.assertTrue(c.text.endswith("."))
            self.assertLessEqual(len(c.text), 55)
        self.assertEqual([c.index for c in chunks], list(range(len(chunks))))
        self.assertIn("Pay with a card.", chunks[0].text)
        self.assertIn("Pay with a card.", chunks[1].text)

    def test_oversized_sentence_is_preserved_and_no_overlap_only_tail(self):
        sentence = "This " + "very " * 30 + "long sentence stays complete."
        with patch.object(config, "CHUNK_SIZE", 60), patch.object(config, "CHUNK_OVERLAP", 20):
            chunks = split_documents([Document("long.txt", "Title\n\n" + sentence)])
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].text, "Title\n\n" + sentence)

    def test_zero_overlap_and_empty_documents(self):
        with patch.object(config, "CHUNK_SIZE", 40), patch.object(config, "CHUNK_OVERLAP", 0):
            chunks = split_documents([Document("a.txt", "Topic\n\nFirst complete sentence. Second complete sentence."), Document("b.txt", " ")])
        self.assertEqual(len(chunks), 2)
        self.assertNotIn("First complete sentence.", chunks[1].text)

    def test_invalid_settings_fail_instead_of_looping(self):
        for size, overlap in [(0, 0), (40, -1), (40, 40)]:
            with self.subTest(size=size, overlap=overlap):
                with patch.object(config, "CHUNK_SIZE", size), patch.object(config, "CHUNK_OVERLAP", overlap):
                    with self.assertRaises(ValueError):
                        split_documents([])

    def test_cleaning_preserves_content_and_paragraphs(self):
        self.assertEqual(clean_text("  Title\r\n\r\n\r\nPay\t\t$1.75.  "), "Title\n\nPay $1.75.")

    def test_campus_corpus_has_no_lost_body_text(self):
        # Compare token sequences, allowing repeated titles/sentence overlap.
        for doc in load_documents("campus_life"):
            chunks = split_documents([doc])
            body = doc.text.partition("\n\n")[2]
            for paragraph in body.split("\n\n"):
                for sentence in paragraph.split(". "):
                    self.assertTrue(any(sentence.rstrip(".") in c.text for c in chunks), (doc.source, sentence))


class GateTests(unittest.TestCase):
    def result(self, distance):
        return Result("Printing credit is $30.", "printing.txt", "printing.txt#0", distance, "chunker.py::split_documents")

    def test_empty_and_boundary_are_refused(self):
        self.assertFalse(gate.check([], 0.6).passed)
        self.assertFalse(gate.check([self.result(0.6)], 0.6).passed)
        self.assertTrue(gate.check([self.result(0.599)], 0.6).passed)

    def test_refusal_never_calls_the_model(self):
        for hits in [[], [self.result(0.95)]]:
            with self.subTest(hits=hits):
                with patch("store.search", return_value=hits), patch("generate.answer_from_chunks") as model:
                    outcome = app.ask_pipeline("Unrelated question", threshold=0.6)
                model.assert_not_called()
                self.assertTrue(outcome["refused"])
                self.assertEqual(outcome["answer"], gate.REFUSAL)
                self.assertEqual(outcome["sources"], [])
                self.assertEqual(outcome["refusal_reason"], "relevance_gate")

    def test_relevant_question_uses_retrieved_evidence(self):
        hit = self.result(0.25)
        with patch("store.search", return_value=[hit]), patch("generate.answer_from_chunks", return_value="Credit is $30 (printing.txt).") as model:
            outcome = app.ask_pipeline("How much printing credit?", threshold=0.6)
        model.assert_called_once_with("How much printing credit?", [hit])
        self.assertFalse(outcome["refused"])
        self.assertIn("printing.txt", outcome["answer"])
        self.assertEqual(outcome["sources"], ["printing.txt"])
        self.assertEqual(outcome["retrieved_sources"], ["printing.txt"])
        self.assertIsNone(outcome["refusal_reason"])
        self.assertIn(hit.text, outcome["prompt"])

    def test_uncited_model_answer_is_refused(self):
        hit = self.result(0.25)
        with patch("store.search", return_value=[hit]), patch(
            "generate.answer_from_chunks", return_value="Each student gets thirty dollars."
        ) as model:
            outcome = app.ask_pipeline("How much printing credit?", threshold=0.6)

        model.assert_called_once_with("How much printing credit?", [hit])
        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["answer"], gate.REFUSAL)
        self.assertEqual(outcome["sources"], [])
        self.assertEqual(outcome["retrieved_sources"], ["printing.txt"])
        self.assertEqual(outcome["refusal_reason"], "missing_source_citation")

    def test_model_refusal_sets_refused_flag(self):
        hit = self.result(0.25)
        with patch("store.search", return_value=[hit]), patch(
            "generate.answer_from_chunks", return_value=gate.REFUSAL
        ):
            outcome = app.ask_pipeline("A near-topic unsupported question", threshold=0.6)

        self.assertTrue(outcome["refused"])
        self.assertEqual(outcome["answer"], gate.REFUSAL)
        self.assertEqual(outcome["sources"], [])
        self.assertEqual(outcome["retrieved_sources"], ["printing.txt"])
        self.assertEqual(outcome["refusal_reason"], "model_refusal")


class ServeTests(unittest.TestCase):
    def test_model_refusal_is_reported_consistently_over_http(self):
        hit = Result(
            "Printing credit is $30.",
            "printing.txt",
            "printing.txt#0",
            0.25,
            "chunker.py::split_documents",
        )
        with patch("store.search", return_value=[hit]), patch(
            "generate.answer_from_chunks", return_value=gate.REFUSAL
        ):
            response = web_app.test_client().post(
                "/ask", json={"question": "A near-topic unsupported question"}
            )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["refused"])
        self.assertEqual(payload["refusal_reason"], "model_refusal")
        self.assertEqual(payload["sources"], [])
        self.assertEqual(payload["retrieved_sources"], ["printing.txt"])


if __name__ == "__main__":
    unittest.main()

