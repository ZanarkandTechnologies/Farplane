# Research taste

How to pick a bet worth holding, and how to reach a verdict that survives a
second look. Kenji, 14 Nov 2026: threads hill-climbed today's method, set an
outside method up quickly, scored it on our data and dropped it at the first
bad number. Five such "the method is bad" verdicts were later traced to our
own setup: LingBot-Map (stream order), Solv3R (black bars), IDOL (wrong mode),
SURE-Map (63.9 to 75.4 with a square crop and anchors) and the RoomPlan truth
(shifted 12 cm).

The verdict rules (3 to 7) are also in the global `AGENTS.md`, because any
thread can test a paper. This file adds the planning method and the records.

## 1. Bet from the ideal backwards (before N2 and N3)

Draw the ideal end-to-end solution as parts, not today's pipeline:

| Part | What it unlocks | Status | Evidence |
| --- | --- | --- | --- |
| one row per part | the parts and product measures that depend on it | `works`, `works with perfect input` or `unproved` | receipt or "not measured" |

- Give each unproved part perfect input (N2's truth swap, applied to the ideal
  solution) to read its ceiling before building it.
- Bet on the part whose success unlocks the most, even when it is the hard
  one. Hill-climb today's method only when the map says its part is the limit.
- Redraw the map when a part changes status.

## 2. Two idea sources, both used (N3)

- **Promises:** what papers and released models report they can do. Combine
  promises that cover different parts of the map or miss different cases.
  State how the paper's data differs from ours (sensor, scene type, scale).
- **Practice:** what our own misses and perfect-input swaps say is the limit.
- Each card says in its `mechanism` which source it comes from (`promise`,
  `practice` or `both`) and which map part it unlocks. A tree fed by one
  source only is incomplete: say so.

## 3. Reproduce before you judge (N1, for any outside method)

Before an outside method is scored on our data, record:

```text
reproduction: claim | their number | our number | data | settings | status
status = reproduced (within their reported spread) | off by <x> | not run
```

- Use their code, checkpoint and preprocessing unchanged, at the smallest
  published setting.
- `off by` or `not run`: a bad score on our data reads "setup unverified".
  It is never a kill and never a "lost" row.

## 4. Suspect the setup first (N5, on any miss)

Ask why the authors got X and we got Y, before any "failed because":

- List what differs: input size, crop or padding, orientation, units,
  coordinate frame, frame order, mode or preset, checkpoint, preprocessing,
  the scorer, and the truth itself.
- Test the three most likely differences, one at a time.
- Run one known-answer case: an input where the method must work (the
  authors' demo input, or a synthetic case with exact truth).
- Look at exactly what enters the model and what leaves it, as images or
  overlays, not only the score.

## 5. Give up for a reason (N6)

Before the first run, size the tries the bet deserves from its upside. Drop an
idea, for one stated purpose, only when one of these holds:

- its physical claim is measured false;
- with perfect input it still does not move the product measure beyond that
  measure's noise;
- three faithful designs, each fixing the last one's named failure, stay flat.

Anything else is `alive`, or `parked` with a "revisit when" line. A tool that
broke is not a result (`unblock`).

## 6. Say what was tested

A verdict names the setup, the reproduction status, and the cause class of a
loss: `idea`, `design`, `setup` or `measure`.

## 7. Test lean

Each step is the smallest run that could change the decision: one room before
three, one GPU, a cached image, a free local run before a paid one.
Persistence means more small tries, each with a named cause, never a bigger
budget.

## Sources

- Karpathy, [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/):
  training fails silently, so overfit one batch, check the first loss, and
  look at what enters the network.
- Hamming, [You and Your Research](https://www.cs.virginia.edu/~robins/YouAndYourResearch.html):
  a problem is important when you have a reasonable attack on it.
