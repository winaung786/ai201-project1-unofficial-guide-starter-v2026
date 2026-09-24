# Run log — before_scored_live

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`
- Corpus: `campus_life` (index variant `default`)
- top-k: 5 · relevance cutoff: 0.6
- Runs per question: 3, caching off
- When: 2026-09-23 17:11

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| How are juniors and seniors ordered in the housing lottery? | pass | pass | pass |
| How long is the lunch wait at Kestrel Commons between 12:15 and 1:00? | pass | pass | pass |
| How much does one wash cost in Aldridge Hall, and how do you pay? | pass | pass | pass |
| How far ahead can I book a group study room, and how many blocks can I book per week? | pass | pass | pass |
| How much printing credit does each student get per semester, and does it roll over? | pass | pass | pass |

---

## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 15 of 15.

Each fixed question was tested in every run. Gate refusals cost
zero model calls; questions let through use the application answer.

| Run | Out-of-scope question | Best distance | Gate |
|---|---|---|---|
| 1 | What is the capital of Mongolia? | 0.825 | refused |
| 1 | How do I change the oil in a diesel engine? | 0.934 | refused |
| 1 | Who won the 1994 World Cup? | 0.886 | refused |
| 1 | What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| 1 | How do I write a for loop in Rust? | 0.896 | refused |
| 2 | What is the capital of Mongolia? | 0.825 | refused |
| 2 | How do I change the oil in a diesel engine? | 0.934 | refused |
| 2 | Who won the 1994 World Cup? | 0.886 | refused |
| 2 | What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| 2 | How do I write a for loop in Rust? | 0.896 | refused |
| 3 | What is the capital of Mongolia? | 0.825 | refused |
| 3 | How do I change the oil in a diesel engine? | 0.934 | refused |
| 3 | Who won the 1994 World Cup? | 0.886 | refused |
| 3 | What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| 3 | How do I write a for loop in Rust? | 0.896 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### How are juniors and seniors ordered in the housing lottery? — run 1

- Best distance: 0.2250 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, dining_the_atrium_followup.txt, housing_tamsin_court.txt
- Sources cited: admin_housing_lottery.txt

```
Juniors and seniors are ordered by accumulated credit hours first, with ties broken randomly (admin_housing_lottery.txt).
```

### How are juniors and seniors ordered in the housing lottery? — run 2

- Best distance: 0.2250 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, dining_the_atrium_followup.txt, housing_tamsin_court.txt
- Sources cited: admin_housing_lottery.txt

```
Juniors and seniors are ordered by accumulated credit hours first, with a random tie-break used only when necessary (admin_housing_lottery.txt).
```

### How are juniors and seniors ordered in the housing lottery? — run 3

- Best distance: 0.2250 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, advising_registration.txt, dining_the_atrium_followup.txt, housing_tamsin_court.txt
- Sources cited: admin_housing_lottery.txt

```
Juniors and seniors are ordered by accumulated credit hours first, with a random tie-break (admin_housing_lottery.txt).
```

### How long is the lunch wait at Kestrel Commons between 12:15 and 1:00? — run 1

- Best distance: 0.1797 (passed the gate)
- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_north_kitchen_followup.txt, dining_the_ridgeway_cafe_followup.txt
- Sources cited: dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt

```
The wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00 (dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt).
```

### How long is the lunch wait at Kestrel Commons between 12:15 and 1:00? — run 2

- Best distance: 0.1797 (passed the gate)
- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_north_kitchen_followup.txt, dining_the_ridgeway_cafe_followup.txt
- Sources cited: dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt

```
The wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00 (dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt).
```

### How long is the lunch wait at Kestrel Commons between 12:15 and 1:00? — run 3

- Best distance: 0.1797 (passed the gate)
- Sources retrieved: dining_halden_hall_followup.txt, dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt, dining_north_kitchen_followup.txt, dining_the_ridgeway_cafe_followup.txt
- Sources cited: dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt

```
The wait time at Kestrel Commons is 20 to 25 minutes between 12:15 and 1:00 (dining_kestrel_commons.txt, dining_kestrel_commons_followup.txt).
```

### How much does one wash cost in Aldridge Hall, and how do you pay? — run 1

- Best distance: 0.2623 (passed the gate)
- Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_old_brewhouse.txt
- Sources cited: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt

```
One wash in Aldridge Hall costs $1.75, and it is card only (housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt).
```

### How much does one wash cost in Aldridge Hall, and how do you pay? — run 2

- Best distance: 0.2623 (passed the gate)
- Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_old_brewhouse.txt
- Sources cited: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt

```
In Aldridge Hall, one wash costs $1.75 and is card only. This information comes from `housing_aldridge_hall_laundry.txt` and `housing_aldridge_hall.txt`.
```

### How much does one wash cost in Aldridge Hall, and how do you pay? — run 3

- Best distance: 0.2623 (passed the gate)
- Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt, housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_old_brewhouse.txt
- Sources cited: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt

```
In Aldridge Hall, a wash costs $1.75 and is card only. (housing_aldridge_hall_laundry.txt, housing_aldridge_hall.txt)
```

### How far ahead can I book a group study room, and how many blocks can I book per week? — run 1

- Best distance: 0.1958 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_340.txt, dining_north_kitchen_followup.txt, money_jobs.txt, study_group_rooms.txt
- Sources cited: study_group_rooms.txt

```
You can book a group study room two weeks ahead, for a maximum of two blocks per person per week (study_group_rooms.txt).
```

### How far ahead can I book a group study room, and how many blocks can I book per week? — run 2

- Best distance: 0.1958 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_340.txt, dining_north_kitchen_followup.txt, money_jobs.txt, study_group_rooms.txt
- Sources cited: study_group_rooms.txt

```
You can book a group study room two weeks ahead, and the maximum is two blocks per person per week (study_group_rooms.txt).
```

### How far ahead can I book a group study room, and how many blocks can I book per week? — run 3

- Best distance: 0.1958 (passed the gate)
- Sources retrieved: course_cs_210.txt, course_cs_340.txt, dining_north_kitchen_followup.txt, money_jobs.txt, study_group_rooms.txt
- Sources cited: study_group_rooms.txt

```
You can book a group study room two weeks ahead, for a maximum of two blocks per person per week (study_group_rooms.txt).
```

### How much printing credit does each student get per semester, and does it roll over? — run 1

- Best distance: 0.3726 (passed the gate)
- Sources retrieved: admin_graduation_requirements.txt, admin_pass_fail_option.txt, admin_printing_quota.txt, admin_wifi_and_accounts.txt, money_jobs.txt
- Sources cited: admin_printing_quota.txt

```
Every student gets $30 of printing per semester, and it does not roll over (admin_printing_quota.txt).
```

### How much printing credit does each student get per semester, and does it roll over? — run 2

- Best distance: 0.3726 (passed the gate)
- Sources retrieved: admin_graduation_requirements.txt, admin_pass_fail_option.txt, admin_printing_quota.txt, admin_wifi_and_accounts.txt, money_jobs.txt
- Sources cited: admin_printing_quota.txt

```
Each student gets $30 of printing per semester, and it does not roll over (admin_printing_quota.txt).
```

### How much printing credit does each student get per semester, and does it roll over? — run 3

- Best distance: 0.3726 (passed the gate)
- Sources retrieved: admin_graduation_requirements.txt, admin_pass_fail_option.txt, admin_printing_quota.txt, admin_wifi_and_accounts.txt, money_jobs.txt
- Sources cited: admin_printing_quota.txt

```
Each student gets $30 of printing per semester, and it does not roll over (admin_printing_quota.txt).
```
