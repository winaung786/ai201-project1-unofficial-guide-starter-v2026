"""Week 2 answer scorer used automatically by ``run_eval.py``.

This intentionally implements the simple substring check taught in class.
It is only a quick check for a required fact; the criterion-level source and
grounding reviews in README.md remain manual because a substring scorer cannot
detect unsupported extra claims.
"""


def judge(question: str, expects: str, answer: str, results: list) -> bool:
    """Return whether the generated answer contains its expected phrase.

    ``question`` and ``results`` are part of the required Week 2 interface and
    are available for future retrieval-based criteria.  This scorer evaluates
    the current answer-based ``expects`` phrases from ``questions.py``.
    """
    del question, results
    expected = expects.strip().casefold()
    return bool(expected) and expected in answer.casefold()
