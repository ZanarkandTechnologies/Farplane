---
template_id: skill-qa-checklist
template_version: "0.1.0"
feature_refs:
  - FEAT-0057
consumer_scope: skill
applies_to:
  - skills/*/qa_checklist.md
---

# Skill QA Checklist

Use this file only when a skill has repeatable runtime guardrails that should be
read before execution and checked again before completion.

## Checklist

- [ ] Preflight context is sufficient for the current request.
- [ ] Required references, scripts, evals, or templates were loaded only when
  the active branch needed them.
- [ ] The output satisfies the skill's stated contract.
- [ ] Proof, blocker, or skipped-proof evidence is recorded before completion.
