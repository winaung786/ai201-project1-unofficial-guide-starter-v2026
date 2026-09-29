"""Guard the optional lexical rerank against losing semantic relevance."""

import unittest
from unittest.mock import MagicMock, patch

from store import Result, _rerank, search


def hit(text, source, distance):
    return Result(text, source, f"{source}#0", distance, "chunker.py::split_documents")


class StretchRerankTests(unittest.TestCase):
    def test_search_can_reproduce_vector_only_baseline_without_reranking(self):
        collection = MagicMock()
        collection.count.return_value = 10
        collection.query.return_value = {
            "documents": [["A source fact."]],
            "metadatas": [[{"source": "fact.txt", "index": 0}]],
            "distances": [[0.25]],
        }
        for enabled, expected_candidates in ((False, 1), (True, 5)):
            with self.subTest(lexical_rerank=enabled):
                with patch("store._client") as client, patch("store.embed", return_value=[[0.0]]), patch("store._rerank", side_effect=lambda question, hits: hits) as rerank:
                    client.return_value.get_collection.return_value = collection
                    results = search("A fact?", top_k=1, lexical_rerank=enabled)
                self.assertEqual(collection.query.call_args.kwargs["n_results"], expected_candidates)
                self.assertEqual(rerank.call_count, int(enabled))
                self.assertEqual(results[0].distance, 0.25)

    def test_weekend_hours_chunk_beats_named_followup_without_hours(self):
        followup = hit("Re: Kestrel Commons. Kestrel Commons has a lunch wait.", "followup.txt", 0.428)
        hours = hit("Kestrel Commons. Open until 8:00pm weekends.", "main.txt", 0.505)
        ranked = _rerank("When does Kestrel Commons close on weekends?", [followup, hours])
        self.assertEqual(ranked[0].source, "main.txt")
        self.assertEqual(ranked[0].distance, 0.505)

    def test_far_lexical_hit_cannot_override_near_semantic_hit(self):
        near = hit("Kestrel Commons has meals.", "near.txt", 0.31)
        far = hit("Kestrel Commons cash meal cost", "far.txt", 0.8)
        ranked = _rerank("What is the cost of a cash meal at Kestrel Commons?", [near, far])
        self.assertEqual(ranked[0].source, "near.txt")


if __name__ == "__main__":
    unittest.main()
