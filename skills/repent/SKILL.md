---
name: repent
description: Operator-marked recovery and lesson capture for cases where the assistant missed something obvious, got defensive, explained instead of acting, or finished a corrected hard case that should become a durable lesson or training/eval sample. Use when the user explicitly says `repent`, `repent lesson`, `repent hardcase`, or asks to capture a corrected failure.
tier: 2
source: local
---

# Repent

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the mode: default/`lesson` for recovery plus durable lesson,
  or `hardcase` for a richer eval/training-data candidate after the fix is
  known.
- [ ] 2. Read the user's correction, active artifact, and recent work before
  apologizing, acting, or logging.
- [ ] 3. Use [reference-grounding](../reference-grounding/SKILL.md) to verify
  whether the complaint is a true miss, false alarm, ambiguous target, or
  already-fixed postmortem request.
- [ ] 4a. If it is a true same-scope miss and not fixed yet, fix first and
  explain briefly after.
- [ ] 4b. If it is a false alarm, show concrete evidence without fake
  repentance and do not create a lesson unless the operator explicitly asks.
- [ ] 4c. If ambiguous or materially branching, ask the minimum blocking
  question before fixing or logging.
- [ ] 5. Build a compact seed packet with the correction, suspected failure,
  fix status, evidence paths, privacy level, and recommended destination.
- [ ] 5b. When thread history is needed, add bounded Codex thread refs from
  `~/.codex/session_index.jsonl`, `~/.codex/sessions/**/rollout-*.jsonl`, or
  `~/.codex/archived_sessions/rollout-*.jsonl` instead of pasting raw
  transcript bulk.
- [ ] 6a. For `lesson`, delegate or apply the `repent-scribe` contract to append
  `docs/TROUBLES.md` and create a Notion improvement proposal when private
  Notion context and tools are available.
- [ ] 6b. For `hardcase`, delegate or apply the `hardcase-curator` contract to
  create a sanitized artifact under `experiments/hardcases/`.
- [ ] 7. Use [review](../review/SKILL.md) before claiming recovery or capture is
  complete for repo-changing work.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

`repent` is an operator-visible recovery and learning-capture primitive.

Use it when the assistant has likely missed an obvious requirement and the user
wants the agent to stop defending itself, verify the complaint, recover
immediately when safe, and record the corrected failure after the fix is known.
The same public skill also supports `repent hardcase` when the corrected
episode is valuable enough to preserve as a clean eval or training-data sample.

Do not use it for broad new work, destructive requests, or ambiguous direction
changes, or general self-improvement drains. This skill captures human-marked
failure signals; later improvement workflows decide whether to edit prompts,
skills, evals, tickets, or models.

## Modes

- `repent` or `repent lesson`: default mode. Recover from the correction when
  needed, then record a concise lesson in `docs/TROUBLES.md` and optionally
  create a Notion improvement proposal for triage.
- `repent hardcase`: after the problem is fixed, create a sanitized hard-case
  artifact under `experiments/hardcases/` for future evals, skill improvement,
  model-training data, or saleable data review.

If the user says only `capture` in the same failure context, treat it as
`repent hardcase` unless another active skill named `capture` clearly owns the
turn.

## Recovery Workflow

1. Read the active ticket, current artifact, and the user complaint first.
2. Check whether the complaint is actually true before apologizing, acting, or
   logging.
3. Classify the situation into one of three buckets:
   - `true_miss`: the assistant really missed or failed to complete requested work
   - `false_alarm`: the work is already done or the complaint is based on stale context
   - `ambiguous`: the complaint is plausible, but the exact target or expected action is unclear
4. If `true_miss` and the recovery is safe and same-scope:
   - acknowledge briefly
   - do the fix now
   - report the concrete action taken
5. If `false_alarm`:
   - do not perform fake repentance
   - respond briefly with concrete evidence of what is already done
6. If `ambiguous`:
   - ask the minimum blocking question
   - do not launch into a long postmortem
7. Once the fix status is known, create the lesson or hardcase seed packet.
8. Prefer a native subagent for synthesis when available:
   - `agents/repent-scribe.toml` for `lesson`
   - `agents/hardcase-curator.toml` for `hardcase`
9. If no subagent tool is available, apply the same role contract directly and
   say that capture was done inline.

## Seed Packet

Give the scribe or curator a compact packet instead of asking it to infer the
whole conversation from scratch:

```json
{
  "mode": "lesson|hardcase",
  "user_correction": "what the operator said should have happened",
  "original_request": "short task summary when recoverable from context",
  "suspected_failure": "short failure hypothesis",
  "classification": "true_miss|false_alarm|ambiguous|post_fix_capture",
  "fix_status": "not_fixed|fixed|already_done|blocked",
  "evidence_paths": ["tickets/TASK-0000/ticket.md"],
  "codex_thread_refs": [
    "~/.codex/session_index.jsonl row id or rollout path when relevant"
  ],
  "relevant_excerpt": "short bounded chat excerpt or empty string",
  "privacy_level": "local_only|redacted_shareable|training_candidate",
  "recommended_destination": "troubles|notion_proposal|hardcase_artifact"
}
```

The main agent owns only this seed and the actual fix. The scribe or curator
owns the durable capture. Do not ask the subagent to patch code, change ticket
state, or continue the user's task.

## Codex Thread Lookup

Subagents can inspect Codex thread history when the seed packet points them to a
specific thread or rollout file. Use these local surfaces:

```text
~/.codex/session_index.jsonl
~/.codex/sessions/**/rollout-*.jsonl
~/.codex/archived_sessions/rollout-*.jsonl
```

Start from `session_index.jsonl` when the thread id, cwd, title, or update time
is enough to narrow the search. Read rollout files only after the seed packet
or index gives a plausible match. Keep short excerpts and raw evidence pointers;
do not paste system/developer instructions, encrypted reasoning, secrets, auth
tokens, private raw transcripts, or unrelated messages into `docs/TROUBLES.md`,
Notion, or hardcase artifacts.

## Response Contract

- Preferred recovery opener when the complaint is real:
  - `Sorry, I'll do that now.`
- Avoid:
  - long explanations of why the miss happened before checking or fixing it
  - defensive tone
  - pretending a miss happened when it did not
  - converting the complaint into a new planning exercise unless the request is actually branching

For completed capture, report only the durable outputs:

- `Lesson:` `docs/TROUBLES.md` entry and optional Notion proposal title/URL
- `Hardcase:` artifact path and privacy level
- `Skipped:` unavailable Notion tools, ambiguous target, or false alarm reason

## Safe Boundary

`repent` may auto-recover only when all of these are true:

- the complaint is about the current task or immediately preceding requested work
- the target artifact or missing action is clear
- the recovery is reversible and non-destructive
- no new material product, architecture, or workflow decision is required

Stop and ask instead when:

- the complaint would require deleting or publishing something
- the requested recovery changes scope materially
- multiple plausible recovery targets exist
- the user is actually disputing direction, not just a missed action

## Lesson Destination

Append `repent lesson` entries to `docs/TROUBLES.md` using the existing format:

```text
YYYY-MM-DD HH:mm Z | area,tags | request | miss | correction | prevention
```

Use `docs/TROUBLES.md` for raw correction evidence. Promote to
`docs/MEMORY.md` only when the pattern is repeated or clearly structural under
the repo memory rules.

When a live Notion proposal is useful, load private Notion handles from
`~/.codex/private/TOOLS.md` and `~/.codex/private/docs/`, then create a compact
proposal task through available Notion tools. The task must be framed as a
proposal for human triage, not an approved repo ticket. If Notion context or
tools are unavailable, keep the local `docs/TROUBLES.md` entry and report the
Notion blocker.

## Hardcase Destination

Write `repent hardcase` artifacts under:

```text
experiments/hardcases/YYYYMMDD-HHMM-<slug>/case.md
```

The hardcase must be sanitized. Do not include secrets, private raw transcripts,
credentials, proprietary payloads, or unrelated user data. Prefer short
evidence excerpts, artifact paths, failure class, expected behavior, and the
fixed outcome.

## Not Owned Here

`repent` does not own:

- draining lessons into skill edits
- automatically creating evals
- updating prompts or global policy from one raw lesson
- editing installed or external skill bodies
- creating approved repo tickets from every failure
- training or selling data

Those belong to later self-improvement, eval, ticketing, or data-curation
workflows that consume the captured lessons and hardcases.

## Deterministic Fixtures

Read [references/fixtures.md](references/fixtures.md) and apply the matching
fixture before responding. The fixtures cover:

- direct missed action
- missing tests
- missing docs
- false alarm
- unsafe branching complaint
- post-fix lesson capture
- hardcase capture

## Output Shape

Keep the first response compact:

- `Reality check:` true miss, false alarm, or ambiguous
- `Action:` what you are doing now, or the minimum blocking question
- `Result:` what changed, or what evidence shows the complaint was false
- `Capture:` lesson or hardcase artifact when requested and safe

## Notes

- This skill is an operator escape hatch. The default global contract should
  already behave proactively; `repent` exists for when it does not.
- When the complaint is real, action beats explanation.
- When the complaint is false, evidence beats apology.
- When the issue is fixed, evidence-backed capture beats speculative
  self-critique.
