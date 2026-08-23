---
title: QA Skill Runtime Checklist
owner: qa
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-07-13
applies_to:
  - qa
  - ticket-proof
---

# QA Skill Runtime Checklist

Use this for material QA reports and after changing the `qa` skill. One QA
owner applies all five gates as one coherent proof journey and returns one
receipt. The gates are evidence categories, not separately spawned tasks.

```text
qa_journey(ticket, proof_policy, runtime_target?)
  -> verdict + best_evidence + blockers + residual_risk + learning_decision
```

## Five Gates

1. **Contract and critical path.** Read the selected ticket, `Done`, QA
   strategy, optional Agent Contract, proof weight, design baseline, and
   runtime handoff. Build the effective proof policy and name the
   claimed workflow and ordered sanity checks; never improvise it from chat or
   pass proxies while the real path remains implicit. Block app/API operation
   when the runtime target is ambiguous.

2. **Real mechanism and evidence.** Exercise the implementation that owns the
   result and capture concrete outputs, traces, API responses, logs, or files.
   For interactive agent demos, verify material claims come from the visible
   tool or state transition rather than narration or prerecorded output. Do
   not fabricate future commands or artifacts. When an external source is
   unavailable, preserve the source gap while still recording independent
   deterministic local checks that can honestly run.

3. **Responsive journey.** Preserve context across the meaningful state change
   under test. For editable or conversational demos, verify the exact edit,
   fresh run or explicit fork, changed result where expected, and retained
   prior trace. For long-form UI, scroll to bottom and retain desktop/mobile
   full-page plus readable top/middle/bottom evidence; map each required
   `design.md` section to a current capture. Record any unrun full-path step as
   residual risk or a blocker.

4. **Adversarial trust and presentation.** Exercise the most relevant failure,
   constraint, or stale-state risk. Use `qa-tester` for operated browser capture,
   `visual-qa` for visual judgment, and `agent-qa-test` for adversarial agent
   behavior when required, while keeping one primary journey owner.

5. **Receipt completeness and learning.** Produce `report.md`, a validated
   canonical `result.json`, supporting artifacts, gate verdicts, blockers,
   residual risk, judgment receipts, `best_evidence`, and one learning outcome.
   Prefer an image for user-visible work. Always update ticket `Links`; update
   `progress.md` only when it exists or Goal/blocker/review state requires it.
   Candidate reusable paths stay `ticket_only` before capture; verified
   reusable paths become `cookbook_update` with a concrete
   `qa/cookbook/*.md` reference.
   Return revise, fail, blocked, or `not_provable` when evidence cannot support
   the claim.
