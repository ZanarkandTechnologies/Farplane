# Closeout Demo

Load for `qa(..., closeout: demo)`: a material implementation Goal, or an
explicit `$demo`, whose QA has already passed and now needs the 45-90 second
Before/After/Example MP4 that leads the GitHub issue's closing proof comment.
Direct non-Goal fixes, heartbeats, and planning-only work skip it. The video
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
- Send the MP4, evidence map, and sources to an independent `reviewer` with the
  demo, video, and evidence rubrics; require TAS-A.
- Then post the closing proof comment with the MP4 first: `gh issue comment
  <n> --body-file closeout.md` (attach or link the MP4; a local path alone is
  not shared), followed by commits, checks, and the QA receipt.

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
