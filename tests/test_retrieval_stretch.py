"""Guard the optional lexical rerank against losing semantic relevance."""

import unittest

from store import Result, _rerank


def hit(text, source, distance):
    return Result(text, source, f"{source}#0", distance, "chunker.py::split_documents")


class StretchRerankTests(unittest.TestCase):
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
