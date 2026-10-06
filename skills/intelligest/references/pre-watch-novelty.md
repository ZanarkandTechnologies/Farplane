# Pre-watch novelty

Answer before watching: what in this video is new from this creator?

## Creator memory

- One Wiki page per creator: `.farplane/entities/<creator-id>.md`, `kind: person` with `roles: [creator]`,
  at the company Wiki root (nearest ancestor whose `.farplane/entities/` holds pages).
- `## Claims` and `## Stories` hold one atomic line each, ending in a
  `[video@m:ss](https://youtu.be/<id>?t=<seconds>)` evidence link.
- After analysis, append every `NEW` or `EXTENDS` point as its own line through
  `manage-wiki` (standing apply intent) and add the video to `## Videos covered`.
- When the caller owns writes (the YouTube bridge), do not edit the page: return
  `creatorMemory` {creatorId, creatorName, newShare, restated, additions[type, text,
  timestamp]} and the caller appends and syncs.

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
