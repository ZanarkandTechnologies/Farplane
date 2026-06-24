---
kind: goal-progress
ticket_id: TASK-0218
status: active
created_at: 2026-06-24
template_id: goal-loop-progress
template_version: "0.1.0"
---

# TASK-0218 Goal Progress

Append one entry per Goal turn, heartbeat, feedback resume, or drift checkpoint.
Keep entries compact. Use this file for after-turn reflection, compact
decision entries, drift notes, evidence links, and completion notes. Link
artifacts instead of pasting raw transcripts.

## 2026-06-24 00:00 +0800 - setup

- `trigger:` manual_resume
- `intent:` create a Goal Packet for minimizing top-level `bin/` as far as
  compatibility allows.
- `actions:` created `ticket.md`, `program.md`, and `progress.md`; bound files,
  metric provider, drift policy, proof route, and stop conditions.
- `decision:` use `active_goal` because this is a bounded cleanup window with a
  mechanical metric and no cadence or external feedback dependency.
- `files_changed:` `tickets/TASK-0218/ticket.md`,
  `tickets/TASK-0218/program.md`, `tickets/TASK-0218/progress.md`
- `artifacts:` pending `tickets/TASK-0218/artifacts/proof/irreducible-bin.md`
- `metric_sample:` current observed `find bin -maxdepth 2 -type f | wc -l`
  was 83; current observed top-level `find bin -maxdepth 1 -type f` was 36
  before this Goal begins implementation.
- `feedback_sample:` none
- `drift_verdict:` aligned
- `drift_evidence:` operator asked to set a `goal-advisor` Goal to tidy bin
  and minimize file count until no safe reductions remain.
- `next_action:` start native Goal execution over this packet.
- `blocker:` none

## 2026-06-24 00:00 +0800 - completion

- `trigger:` native_goal
- `intent:` minimize top-level `bin/` as far as safe compatibility allows.
- `actions:` removed 19 non-installed top-level wrappers; rewired active docs,
  skill guidance, feature registry rows, tests, and `install.sh` to owner paths;
  wrote the irreducible-bin report; removed generated `__pycache__` directories.
- `decision:` stop at 17 remaining top-level files because each remaining file
  is either bin-local policy/docs, shared wrapper loader, live installed
  hook/runtime shim, global CLI edge, or public Core command alias that should
  not be dropped without a compatibility migration decision.
- `files_changed:` `bin/README.md`, top-level `bin/*` wrapper removals,
  `install.sh`, active docs and skill references to owner paths,
  `tickets/TASK-0218/ticket.md`, `tickets/TASK-0218/progress.md`,
  `tickets/TASK-0218/artifacts/proof/irreducible-bin.md`
- `artifacts:` `tickets/TASK-0218/artifacts/proof/irreducible-bin.md`
- `metric_sample:` top-level `bin` file count reduced from 36 to 17; depth-2
  bin file count observed as 63 after generated cache removal.
- `feedback_sample:` none
- `drift_verdict:` complete_candidate
- `drift_evidence:` every remaining top-level file is justified in the
  irreducible-bin report; removed wrapper names have no active references
  outside generated/archive surfaces.
- `next_action:` stage and commit only the TASK-0218 cleanup set.
- `blocker:` none
