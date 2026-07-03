---
kind: project-ops-memory
status: active
project: Farplane
created_at: 2026-06-30
updated_at: 2026-07-03
framework_template_version: "0.1.1"
owner: interval-update
source_of_truth:
  - farplane/harness.md
  - farplane/goals.yaml
  - farplane/products.md
  - docs/farplane-framework/pulse-and-interval-loop.md
---

# Farplane Ops Memory

This file is Farplane's active operating memory: the compact, mutable place for
what the autonomous team is trying to accomplish now. Stable strategy stays in
`farplane/goals.yaml`, product lanes stay in `farplane/products.md`, executable
work stays in `tickets/`, and dated receipts stay under `.farplane/reports/`.

## Current Focus

Convert the clean active board into execution-first autonomous work. Pulse
should do manager planning inside the parent beat, then create or run only
worker tickets that are immediately executable and end in a concrete artifact,
proof packet, state change, QA result, draft, rendered asset, dataset, or review
receipt that advances a named product, lane, reward, or artifact workflow from
`farplane/products.md`.

## Active Projects

### Pulse / Interval Autonomy

- `lane:` productization
- `goal_axes:` project_control, quality_and_proof, validated_self_improvement
- `contribution_mode:` reusable_harness_capability + proof_quality
- `weekly_runway_decision:` continue
- `expected_reward:` Pulse and Interval stop creating one-ticket crumbs and
  produce strategy-grounded execution work with visible proof.
- `done_signal:`
  - Pulse can name the active focus and next frontier before creating tickets.
  - Daily and Weekly can refresh the active focus without rewriting goals or
    products.
  - Maintenance stays parked unless it unblocks the active frontier.
  - Pulse does not create tickets whose main deliverable is planning,
    prioritization, or ticket generation.
- `critical_path:`
  1. Preserve the clean-board closure proof from `TASK-0275`.
  2. Keep `pulse-update` responsible for manager planning and worker portfolio
     reconciliation.
  3. Admit or create only execution tickets with concrete deliverables that
     contribute to `farplane/products.md`.
  4. Judge the next Pulse beat by whether it produces artifact-bearing work,
     not more planning-to-plan.
- `next_frontier:`
  - With the board clean after `TASK-0275`, use this memory and
    `farplane/products.md` to select one small execution wave.
  - Prefer ablation, experiment, local proof, content draft, video/demo asset,
    QA/review, or packaging tickets that can finish without posting,
    publishing, spending, deploying, external contact, account mutation, or
    destructive cleanup, and require each ticket to name the product lane or
    artifact workflow it advances.

### Evidence-To-Content Loop

- `lane:` experiments, ablations, trust_distribution
- `goal_axes:` distribution_from_evidence, validated_self_improvement
- `contribution_mode:` distribution + validated_learning + proof_reuse
- `weekly_runway_decision:` continue
- `expected_reward:` accepted harness evidence becomes content-ready proof,
  social KPI readings, and missing-feedback instrumentation.
- `done_signal:`
  - one accepted ablation or experiment proof
  - one findings report
  - one paper-style diagram or content-ready visual plan
  - one technical X/Instagram content draft
  - one KPI or feedback capture note
- `critical_path:`
  1. Produce an artifact-bearing ablation or experiment output for a shipped
     Farplane claim.
  2. Write findings from local evidence without overclaiming metrics.
  3. Convert accepted findings into a technical draft, storyboard, video/demo
     asset, or visual packet.
  4. Stop before human-gated final actions such as posting, publishing,
     spending, deploying, external contact, or account mutation.
- `next_frontier:`
  - Next Pulse may create or run one to three execution tickets from this path
    when they have concrete deliverables and parseable rewards.

## Next Frontier

- `primary:` create or run an execution-first wave from the clean board:
  ablation proof, experiment evidence, local findings, draft content/video
  assets, QA/review receipts, or packaging artifacts that map to
  `farplane/products.md`.
- `secondary:` keep project-control maintenance bounded to work that directly
  unblocks the primary frontier.

## Tracked Feedback

- `social_content:` X and Instagram account skills own post/metrics observations;
  tracked content IDs belong in snapshot item breakdowns, not in goals.
- `repo_adoption:` `github_repo_feedback` reads
  `ZanarkandTechnologies/Farplane` through `gh api` for stars, forks, issues,
  PRs, daily views, and daily unique cloners.
- `autonomy_time:` `autonomy_time_feedback` reads local Codex/Farplane event
  ledgers for human prompt count, estimated human attention minutes,
  autonomous worker elapsed minutes, auto-time ratio, and output per human
  prompt.
- `source_gaps_to_watch:` retention scores, social posts, framework adoption
  events, and weekly runway review rows until their providers write readings.

## Constraints

- Caps and cadence live in `.farplane/automation/heartbeat-policy.json`, not in
  this file.
- Weekly runway decisions use active project contribution mode, ticket Reward
  blocks, metric snapshots, and source gaps. They are planning evidence, not
  permission for spend, publishing, customer contact, or product-boundary
  changes.
- Do not mutate `farplane/goals.yaml`, `farplane/products.md`, publishing,
  accounts, spend, deploys, or customer contact from ops-memory alone.
- Do not create a roadmap registry, project schema, database, UI, hidden
  scheduler, or ticket-drainer from this file.
- Use this file to choose the active frontier; use tickets to execute work.
- Pulse manager planning stays in the parent beat. Do not create worker tickets
  whose main deliverable is choosing the next direction, refreshing strategy,
  prioritizing tickets, or planning more tickets.
- A worker artifact is valid only when it contributes to a named product, lane,
  reward, or artifact workflow in `farplane/products.md`.

## Parking Lot

- `TASK-0246` Kenji Review metadata cleanup if it continues to confuse Pulse.
- Strict YAML frontmatter validation for ticket metadata.
- `autonomy_profile` / `review_mode` metadata idea; not needed for the current
  MVP.
- Dirty-surface closeout work that does not unblock the current frontier.
- Pure planning tickets for Pulse-created workers. Use parent Pulse reports,
  Daily/Weekly intervals, or direct bounded manager writeback instead.

## Recent Decisions

- Use `farplane/ops-memory.md`, not `farplane/ops.md`, to make the memory split
  explicit.
- Keep roadmaps and projects as flexible Markdown sections inside ops-memory,
  not as new artifact families.
- Plan from the active frontier, execute up to policy cap, and record receipts.
- `2026-07-03:` Replace the completed `TASK-0251` frontier after clean-board
  closure. The next useful Pulse wave should be execution-first and
  artifact-bearing; manager planning belongs in Pulse, not in worker tickets.

## Pulse Notes

- When creating next-wave tickets, cite the active project and frontier step
  that justified the ticket.
- Created worker tickets must be immediately executable and end in a concrete
  artifact, proof packet, local state change, QA result, draft, rendered asset,
  dataset, or review receipt that contributes to `farplane/products.md`.
- If the next useful move is planning, prioritization, ops-memory refresh, or
  queue reconciliation, do it in the parent beat or ask Daily/Weekly for
  planning; do not create a worker ticket for it.
- If this file is stale, missing, or contradicted by the latest Daily/Weekly
  strategy, record that in the Pulse report instead of guessing.
- If maintenance is selected, name the active frontier it unblocks.
- Treat open worker threads as the live worker surface, not an approval queue.
  When a worker is waiting for Kenji review or a final human-gated action, Pulse
  may record a compact manager note with ticket id, thread id, waiting reason,
  and reminder status, then keep safe local work moving. Detailed review state
  stays in the worker thread, ticket, Telegram log, and Pulse report.
