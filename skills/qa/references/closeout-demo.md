# Closeout Demo

Load for `qa(..., closeout: demo)`: an issue labelled `feature`, a material
implementation Goal, or an explicit `$demo`, whose QA has already passed and
now needs the 45-90 second Before/After/Example MP4 that leads the GitHub
issue's closing proof comment. Bug fixes, chores, heartbeats, and
planning-only work skip it. The videos are the release record: the bunker's
Issues board plays them on shipped cards, and the release reel is stitched
from them. The video
explains existing proof; it never replaces QA or adds product claims.

```text
closeout_demo(issue, passing_qa_result, brand_kit?)
  -> final.mp4 + evidence-map.json + media-probe.json + review receipt
```

## Gates

1. **QA passed first.** The latest validated `result.json` verdict is `pass`.
   On `revise`, missing screenshots, or unsourced claims, stop, route back to
   functional or visual mode, and name the recovery owner. Never recapture or
   reinterpret failed behavior to make the story cleaner.
2. **Every claim cites evidence.** Build `evidence-map.json` before scripting:
   each spoken or visible claim maps to an existing QA capture, test output,
   diagram, issue comment, or review receipt. A gap is a blocker, not a line to
   write around.
3. **No generated visuals.** Use real screenshots, captures, diagrams, logs,
   and code excerpts. AI imagery never stands in for product proof; decline
   decorative hero images even when asked, and keep the tone an engineering
   context refresh, not a trailer.
4. **Authorized narration only.** Use an already authorized voice route
   (`ai-video` audio mode). Without approval, keep the spend-free plan, script,
   and evidence map, and return the exact approval needed.

## Story Spine

Plan in `storyboard` plan mode as a child artifact of this issue, not a new
issue. Audience: the lead engineer who watches instead of reading.

- `Before`: old behavior and why it mattered.
- `After`: the shipped behavior.
- `Example`: one concrete end-to-end case shown with verified captures.
- `Key decisions`: at most three tradeoffs needed to understand the result.
- `Proof`: compact QA/review evidence and honest residual risk.

## Render

Render through `/pr-to-video` when the change is one PR (it builds from the
diff and commits), otherwise `/hyperframes` for a deterministic composition of
captions, source labels, screenshots, diagrams, and audio timing. One MP4; no
PPTX, slide deck, or screenshot montage.

## Verify and Review

- `ffprobe` duration, streams, and audible narration; inspect representative
  frames and listen to a sample. Write `media-probe.json`.
- Send the MP4, evidence map, and sources to an independent `reviewer` running
  `review` with families `demo-quality`, `video-quality`, and
  `evidence-quality`; require TAS-A.
- On a public repository the reviewer also confirms the video shows no private
  data (client names, balances, personal details); anything uploaded there is
  public.
- Put it on the shelf: `python3 skills/qa/scripts/demo_shelf.py upload <n>
  final.mp4`. It uploads `issue-<n>.mp4` to the repo's `demos` pre-release
  (created on first use; the fixed tag keeps links stable) and prints the
  `🎬 Demo: <url>` line.
- Post the closing proof comment with that line first: `gh issue comment <n>
  --body-file closeout.md`, followed by commits, checks, and the QA receipt.
  The office reads the first `🎬 Demo:` line from the repo's owner or members.

## Release Reel

At release time, `python3 skills/qa/scripts/demo_shelf.py reel [--since
<tag>]` joins the shelved demos of issues closed since that release (default:
the latest published one) in closing order, into
`.farplane/demo-shelf/reel-<date>.mp4`, and lists the issues it used.

## Package

```text
.farplane/qa/<issue>/<run>/demo/
  content-plan.md  storyboard.md  narration-script.txt
  evidence-map.json  final.mp4  media-probe.json  reviews/  result.json
```

`result.json` here is `{issue, phase: "demo", verdict, summary, artifacts}`. A
pass means the reviewed recap exists and plays; it does not weaken the Goal's
completion review. On a blocker, write a `blocked` or `revise` result beside
the spend-free artifacts and finish with
`EXECUTION_RESULT: status=<demo_complete|blocked> next=<owner> reason=<brief>`.
