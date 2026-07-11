---
title: Goal Advisor QA Checklist
owner: goal-advisor
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-27
applies_to:
  - goals
  - goal-prompts
  - proof-routing
---

# Goal Advisor QA Checklist

Use this after changing Goal Advisor prompts, Goal Packet templates, or
proof-routing behavior.

```text
goal_advisor_qa(goal_prompt, ticket?, program?) -> checklist_verdicts + fixes_or_deferrals + evidence_note
```

## Checks

1. `file-list-compactness`
   - Question: Does the generated Goal prompt point to listed files instead of
     restating long ticket/program/design content?
   - Violation: The prompt duplicates large context that belongs in
     `ticket.md`, `program.md`, `progress.md`, or `design.md`.

2. `proof-route-named`
   - Question: Does the prompt name the proof route for `qa`, `visual_qa`,
     `agent_qa`, `review`, or `demo` proof weights?
   - Violation: It only says "satisfy proof" without naming delegated lanes.

3. `no-self-certification`
   - Question: Are judgment-heavy, QA, visual, adversarial, and final
     completion claims delegated to the right lane?
   - Violation: The same executor may mark its own UI/QA/review proof as pass.

4. `turn-drift-check`
   - Question: Does each turn compare progress against ticket/program files and
     request delegated drift/proof review when required?
   - Violation: Drift is purely memory-based or optional for proof-heavy Goals.

5. `final-image-evidence`
   - Question: For UI/user-visible work, does completion require a Markdown
     image link to best screenshot evidence or a blocker for missing proof?
   - Violation: The final answer can claim UI completion with prose only.

6. `packet-approval-before-run`
   - Question: For material Goal-backed work, is the Goal Packet marked
     `approval: pending` until the human approves the ticket plan, `program.md`,
     `progress.md`, and native `/goal` prompt together?
   - Violation: The packet can be run after plan approval without showing the
     compiled execution contract.

7. `packet-regenerated-after-plan-change`
   - Question: If the ticket plan changed after the packet was compiled, does
     the workflow rerun `goal-advisor` and replace the packet before execution?
   - Violation: The native `/goal` prompt still reflects an older plan.

8. `blocking-questions-resolved`
   - Question: Were missing files, budget, metric, QA Strategy, drift policy,
     human gates, or destructive/deploy/spend boundaries resolved or asked
     before compiling the packet?
   - Violation: The Goal Packet guesses at execution-safety inputs.

9. `coding-grounding-evidence`
   - Question: For implementation feature work, does the Goal prompt require
     code documentation or maintained implementation evidence before final
     completion, using Ref MCP, official docs, GitHub code search, maintained
     examples, or web sources unless the work is explicitly local-only?
   - Violation: A coding Goal can complete from local files and tests alone
     without a final `Grounding:` source-class line or local-only reason.

10. `critical-path-proof`
   - Question: For material feature work, does the Goal prompt require the
     executor to follow the ticket's `QA Strategy` critical-path notes, run
     smaller sanity checks before claiming a long workflow/lifecycle, and report
     unrun final-path risk as a blocker or residual risk?
   - Violation: The Goal can complete from proxy checks while the real claimed
     workflow, hook lifecycle, user path, or session path was never exercised or
     explicitly marked as unrun.

11. `final-completion-checkpoint`
   - Question: For material ticket work, does the prompt require QA evidence
     review and completion review before `stop_complete`, with writeback to
     `ticket.md`, `progress.md`, and artifact links?
   - Violation: The Goal prompt assumes a Stop hook, transcript memory, or the
     executor's own final summary will catch missing proof.

12. `delayed-checkin-program-ownership`
   - Question: Does every delayed Reward packet contain an executable
     `Check-In Program` with inputs, ordered procedure, writeback, decisions,
     idempotency, and source-gap handling, while immediate packets keep only a
     compact `not_applicable` reason?
   - Violation: Pulse or a launcher prompt must reconstruct the experiment's
     scoring policy, or immediate work inherits unused delayed-check-in debt.

## Evidence Note Template

```text
goal_advisor_qa:
  prompt_under_review:
  files_listed:
  approval_state:
  delegated_lanes:
  grounding_evidence_rule:
  final_evidence_rule:
  critical_path_proof_rule:
  final_completion_checkpoint:
  violations:
  fixes_or_deferrals:
```
