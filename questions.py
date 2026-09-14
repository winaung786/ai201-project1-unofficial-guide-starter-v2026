"""Fixed questions recorded before retrieval calibration.

The expects phrases are a simple week-2 scoring aid, not a substitute for
checking that every part of a question was answered correctly.
"""

QUESTIONS = [
    {"question": "How are juniors and seniors ordered in the housing lottery?", "expects": "credit hours"},
    {"question": "How long is the lunch wait at Kestrel Commons between 12:15 and 1:00?", "expects": "20 to 25"},
    {"question": "How much does one wash cost in Aldridge Hall, and how do you pay?", "expects": "$1.75"},
    {"question": "How far ahead can I book a group study room, and how many blocks can I book per week?", "expects": "two"},
    {"question": "How much printing credit does each student get per semester, and does it roll over?", "expects": "$30"},
]

OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions that have been filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
