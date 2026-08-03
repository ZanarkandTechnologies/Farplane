---
template_id: skill-method-reference
template_version: "0.1.0"
feature_refs:
  - FEAT-0008
  - FEAT-0057
consumer_scope: skill-reference
applies_to:
  - skills/demo/SKILL.md
---

# Lead-Engineer Recap

Use this method after the demo skill has found a passing QA result and created
the ticket-scoped demo run directory.

```text
lead_engineer_recap(ticket, verified_evidence, brand_kit?)
  -> narrated_mp4 + evidence_map + media_probe + review_receipts
state: reads(ticket packet and artifacts); writes(one demo run directory)
gates: QA_pass; claim_source_complete; playable_media; TAS_A
fails: PPTX; unsupported claim; invented visual; unauthorized spend
```

## Use When

- A material implementation Goal has passed QA and needs its final recap.
- An operator explicitly invokes `$demo` for a ticket with passing QA.

## Inputs

```text
input_packet:
  required:
    - ticket.md
    - passing QA result.json and its evidence
    - relevant tests or command receipts
  optional:
    - program.md and progress.md
    - diagrams.md or architecture diagrams
    - QA screenshots or clips
    - completion-review inputs
    - approved Brand Kit
  source_refs:
    - every narrative claim resolves to one required or optional artifact
```

## Workflow

1. **Inventory evidence.** Build `evidence-map.json` before scripting. Mark
   gaps as blockers; do not write around them.
2. **Plan one story.** Use `content-impl-plan` in ticket-scoped artifact mode.
   Default audience is the lead engineer and default duration is 45–90
   seconds. Produce MP4 only.
3. **Use the fixed glanceable narrative spine.**
   - `Before`: old behavior and why it mattered.
   - `After`: the shipped behavior.
   - `Example`: one concrete end-to-end use case shown with verified evidence.
   - `Key decisions`: at most three decisions or tradeoffs needed to understand
     the result.
   - `Proof`: compact QA/review evidence and any honest residual risk.
4. **Script and storyboard.** Keep each beat tied to evidence IDs. Prefer
   readable crops, callouts, and deterministic motion over decorative scenes.
5. **Produce narration.** Use an authorized existing voice/audio route. If
   provider use or spend is not already authorized, stop with the exact
   approval needed; do not silently synthesize audio.
6. **Assemble deterministically.** Use Remotion for captions, source labels,
   diagrams, screenshots, code/log excerpts, and audio timing. Generated
   visuals are forbidden by default.
7. **Verify and review.** Probe the MP4, inspect representative frames and
   narration, then obtain independent TAS-A demo/video/evidence review.

## Output Shape

```text
demo_run/
  content-plan.md
  storyboard.md
  narration-script.txt
  evidence-map.json
  final.mp4
  media-probe.json
  reviews/
  result.json
```

Keep `result.json` compatible with Farplane validators:

```json
{
  "ticket_id": "TASK-0000",
  "phase": "demo",
  "verdict": "pass",
  "summary": "Narrated lead-engineer recap passed review.",
  "artifacts": [
    "tickets/TASK-0000/artifacts/demo/<run>/final.mp4",
    "tickets/TASK-0000/artifacts/demo/<run>/evidence-map.json"
  ]
}
```

## Quality Gates

- Every spoken and visible factual claim has an evidence-map entry.
- MP4 media checks pass and independent review reaches TAS-A.
- The recap can refresh context without requiring the viewer to open the
  ticket, while artifact links remain available for deeper inspection.
- For material feature work, the reviewed MP4 is ready to become the first
  selected `$close-ticket` media comment.

## Bad Output

- A deck, screenshot dump, feature trailer, unverified victory narrative, or
  polished video that omits proof and residual risk.
