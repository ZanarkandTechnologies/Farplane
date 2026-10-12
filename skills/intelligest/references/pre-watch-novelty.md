# Pre-watch novelty

Answer before watching: what in this video is new from this creator?

## Creator memory

- One Wiki page per creator: `.farplane/entities/<creator-id>.md`, `kind: person` with `roles: [creator]`,
  at the company Wiki root (nearest ancestor whose `.farplane/entities/` holds pages).
- The page follows the creator page template
  (`docs/farplane-framework/entity-templates/creator.md`): a 3–5 sentence lede, then
  `## Claims` and `## Stories` under its fixed `### ` themes (plus at most two
  niche claim themes), each with a one-line summary.
  Every line is one idea ending in its `[video@m:ss](https://youtu.be/<id>?t=<seconds>)`
  citations; more citations means he repeats it.
- The page is a cache of the creator's top ideas, not a log: at most 100 claims
  and 50 stories. The bridge evicts the least-cited lines (ties keep the newest),
  and full per-video detail stays in each video's dossier. Novelty is judged
  against these top ideas: one-offs rarely recur, and a returning one is only
  re-added, the cheap error.
- The page is a Wikipedia article, never an append-only log. After analysis,
  each point worth remembering goes exactly one way: the page already has it
  (said the same or better) → that line gains this video's citation; it adds a
  specific (number, step, case) → the line is rewritten and keeps every
  citation; it is genuinely new → a new line under its theme. A line is the creator's own
  durable claim or a real story from their life or business. Skits, jokes,
  other speakers' lines, scene descriptions, viewer comments and event
  logistics never become lines; a sketch video usually changes nothing.
  Add the video to `## Videos covered`.
- When the caller owns writes (the YouTube bridge), do not edit the page: return
  `creatorMemory` {creatorId, creatorName, newShare, links[line, timestamp],
  extends[line, rewritten, timestamp], additions[type, text, timestamp]}, copying
  page lines exactly; the caller merges and syncs.

## Classification

| Verdict | Rule |
| --- | --- |
| `NEW` | No memory line states the same specific idea |
| `RESTATED` | A memory line states the same idea, even in other words; cite it exactly |
| `EXTENDS` | Same idea plus a genuinely new specific (number, step, case); name it |

Topic overlap ("both about content") is never `RESTATED`.

## Transport mapping (strict schema, no new fields)

- `recommendation.decision = SKIP`, `reasonCode = ALREADY_KNOWN` when fewer than a
  third of points are `NEW` or `EXTENDS`; otherwise judge WATCH/READ as usual.
- `recommendation.rationale` states "N of M points are new".
- `recommendation.matchedProfile` lists up to three restated memory lines.
- `keyPoints` lead with `NEW`/`EXTENDS` points and their timestamps, and each `finding` starts
  with its class in brackets (`[NEW] …`, `[EXTENDS] …`, `[RESTATED] …`). The stored analysis keeps
  only these tags, so the overlay and the Content panel read each point's verdict and the video's
  originality from them. With no creator page nothing is on file yet, so every point is `[NEW]`;
  leave findings untagged only when the source has no identifiable creator.

## Calibration (Alex Hormozi, 2026-09-28)

- Memory built from 4 videos; two newer videos judged blind: 35 points, one
  false `NEW`.
- The miss: the memory line "Education is the door to commerce" had compressed
  "entertainment makes you a media business that sells eyeballs to advertisers".
  Once that claim had its own line, the new video's "media companies chase views,
  businesses chase buyers" correctly became `EXTENDS`. Keep memory lines atomic.

## Skill level-up (the second check)

- Pick the closest Farplane skill to what the video teaches (the same targets as
  Intel's skill level-ups). Read its SKILL.md and references before judging.
- Return only what the skill lacks, each as one diff line (a step, rule or
  example), with the story or example behind it and its timestamp. Return
  `none` when the skill already covers the video, so it adds nothing to watch.
- The call: neither check finds anything new → skip; a level-up → read the diff,
  or watch when it is a demo or craft you have to see; only creator novelty →
  read his new ideas.
- Proposals are shown, never applied: accepted lines go through
  `harness` maintain mode. When the target skill has an eval, the applied change
  reruns the same frozen eval; never change the rubric to make it pass.
- A tutorial the operator wants learned end to end ("learn this from the
  video") is still one level-up: the method's steps become diff lines against
  the closest skill, or a `harness` create mode handoff when no skill is close.

