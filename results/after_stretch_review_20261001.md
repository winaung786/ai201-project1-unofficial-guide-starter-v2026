# Manual evidence review — post-stretch live evaluation

Reviewed by Codex against the original corpus, after the live execution.
This is a derived human review, not another model run and not an automatic
substring score. Criterion-level verdicts are canonical in the README.

- Live inputs/outputs: [after_stretch JSON](run_20261001T031757487133Z_after_stretch.json)
- Readable live log: [after_stretch Markdown](run_20261001T031757487133Z_after_stretch.md)
- Fresh chunk inspections: [chunk JSON](chunks_20261001T031759129002Z_after_stretch.json)
- Original targets: [criteria.md](../criteria.md)

All three answers for each question were read, together with the actual
retrieved chunk and the original explicitly cited file. The quick scorer was
not used as a substitute for this claim review.

| Fixed question/topic | Required source facts | Cited source in all three trials | Review of all three actual answers |
|---|---|---|---|
| Housing lottery | Juniors/seniors ordered by accumulated credit hours; random tie-breaking only | `admin_housing_lottery.txt` | Each answer states both rules; no unsupported extra rule |
| Kestrel lunch wait | 20 to 25 minutes between 12:15 and 1:00 | `dining_kestrel_commons_followup.txt` | Each answer preserves the named location, time window, and wait range |
| Aldridge wash/payment | $1.75 per wash; card only | `housing_aldridge_hall_laundry.txt` | Each answer states both price and payment restriction, supported by the Aldridge source |
| Group study rooms | Two weeks ahead; maximum two blocks per person per week | `study_group_rooms.txt` | Each answer states both booking limits without inventing a different unit or limit |
| Printing quota | $30 per student per semester; does not roll over | `admin_printing_quota.txt` | Each answer states the amount, period, and no-rollover restriction |

An identity-wording limitation is visible in Aldridge run 2: the answer says
"One wash costs $1.75" and names the correct Aldridge laundry filename, but
does not repeat "Aldridge Hall" in ordinary prose. The cited filename explicitly
identifies the location, and the claim is supported there. This is consistent
with the prior source/entity review; a future requirement to repeat the place
in ordinary prose would need to be specified in advance, as discussed in
What I'd Do Differently. It is not grounds for inventing a missed criterion.

For retrieval, each saved top-1 chunk independently contains every requested
fact above. For source presence, every substantive answer cites that retrieved
filename. Every recorded unrelated trial has the exact application refusal,
a failed relevance gate, null raw model answer, and zero recorded model calls.

For criterion 4, all six pieces from Innisfree Hall, Morrow House, and Old
Brewhouse were compared with their own original text in the fresh chunk log.
The later piece in each post begins with the full laundry sentence and retains
the full noise sentence; the earlier piece ends with the full laundry sentence.
Titles and building-specific prices remain with their named source. No sentence
is cut, and no text from a different post is introduced. The same six pieces
were produced and structurally checked in each of the three fresh trials.

The live run's final process exit was successful. Its checkpoint status is
`complete`, it records no errors, and response caching is disabled. This
establishes recorded completion of these trials, not universal reliability.
