---
title: Agent QA Test Runtime Checklist
owner: agent-qa-test
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-22
applies_to:
  - agent-qa-test
  - adversarial-proof
---

# Agent QA Test Runtime Checklist

Use this after changing `agent-qa-test` or before accepting an adversarial proof
bundle.

## Checks

1. `adversarial-scope`
   - Question: Is the target a claim, skill, prompt, app, workflow, or
     regression that needs adversarial proof?
   - Violation: The skill is used as ordinary ticket QA.

2. `claim-under-test`
   - Question: Is the claim under test written before the run?
   - Violation: The tester can narrow scope without calling that out.

3. `tester-evidence`
   - Question: Does the tester lane gather concrete artifacts?
   - Violation: Tester confidence or prose substitutes for screenshots/logs/files.

4. `independent-evidence-review`
   - Question: Does a separate evidence-review lane attack the tester artifacts?
   - Violation: The tester self-approves.

5. `verdict-scope`
   - Question: Does the final verdict match the evidence scope?
   - Violation: A narrow pass is reported as proof of the broader claim.
