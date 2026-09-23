# Week 2 scorer verification

The required `scorer.py::judge(question, expects, answer, results)` function
was applied to the saved, real, uncached model answers from both Unit 2
evaluations. This does not regenerate or alter either evaluation run.

| Evaluation | Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|
| Before | Housing-lottery ordering | pass | pass | pass |
| Before | Kestrel Commons lunch wait | pass | pass | pass |
| Before | Aldridge Hall laundry | pass | pass | pass |
| Before | Group study-room booking | pass | pass | pass |
| Before | Printing credit | pass | pass | pass |
| After | Housing-lottery ordering | pass | pass | pass |
| After | Kestrel Commons lunch wait | pass | pass | pass |
| After | Aldridge Hall laundry | pass | pass | pass |
| After | Group study-room booking | pass | pass | pass |
| After | Printing credit | pass | pass | pass |

- Before: 15/15 saved live answers passed the substring scorer.
- After: 15/15 saved live answers passed the substring scorer.
- Verification date: September 23, 2026.

The scorer checks only whether the expected phrase appears. It does not replace
the manual source-support review documented in `README.md`, because it cannot
detect an additional unsupported claim.
