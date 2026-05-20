# Manual Benchmark Scorecard

Task: Given one Instagram video, extract relevant frames, understand the visible
workflow, and propose a reusable Codexter skill that could replay the process at
scale.

Variants:

1. `current-codexter`: use existing `harness-scout` plus `harness-advisor`
   manually.
2. `source-proposed`: ask for a single prompt to recreate the visible artifact.
3. `best-of-worlds`: use frame extraction, storyboard inference, Codexter
   placement advice, skill-creator contract, and frontend/visual QA handoff.

Scores:

| Variant | Task completion | Evidence quality | Operator trust | Autonomy resume quality | Overhead cost | Maintainability | Average |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `current-codexter` | 7 | 7 | 8 | 7 | 6 | 8 | 7.2 |
| `source-proposed` | 5 | 3 | 4 | 3 | 9 | 4 | 4.7 |
| `best-of-worlds` | 9 | 9 | 9 | 9 | 7 | 9 | 8.7 |

Winner: `best-of-worlds`

Confidence: medium-high. The visual evidence is strong enough to reconstruct
the workflow, but exact audio and the creator's full master prompt were not
available.

Anti-metrics:

- Do not count "one prompt" as a win if acceptance criteria, assets, and
  debugging are hidden.
- Do not store raw social video as canonical repo knowledge.
- Do not treat selected frames as permission to copy the design verbatim.

Notes:

The best workflow is not a literal clone. It is a source-grounded reconstruction
brief that makes the design intent, event timeline, assets, states, and proof
checks explicit before implementation.
