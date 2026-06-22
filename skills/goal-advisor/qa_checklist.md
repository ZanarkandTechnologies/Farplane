---
title: Goal Advisor QA Checklist
owner: goal-advisor
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-22
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

## Evidence Note Template

```text
goal_advisor_qa:
  prompt_under_review:
  files_listed:
  delegated_lanes:
  final_evidence_rule:
  violations:
  fixes_or_deferrals:
```
