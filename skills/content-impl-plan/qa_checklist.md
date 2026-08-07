---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Content Impl Plan QA Checklist

- [ ] `ticket-contract`: The output is one canonical ticket. Its `Change Plan`
  contains the target deliverable, audience/promise, accepted creative context,
  action graph, and dependency order; `Done` and `QA Strategy` contain the
  proof path and `plan_ready | blocked` state. It does not create a separate
  plan file/schema or present child-owned work as parent-authored.

- [ ] `creative-direction`: Brand Kit remains approved identity/policy truth;
  Tasty Pack remains optional inspiration with visible choose/augment/reject/
  block decisions. The plan states a testable creative hypothesis and explicit
  assumptions without inventing demographics, a third style source, or provider
  details before the owning advisor is selected.

- [ ] `action-ownership`: Every applicable action has `owner`,
  `accepted_inputs`, `primary_output`, `acceptance_or_blocker`, and
  `next_handoff`. Storyboard owns final scenes; Asset Advisor owns source/
  rights/reuse/generation and realization-child selection; Editing Advisor owns
  timed edit direction; Remotion owns implementation/render; QA/review own
  verdicts.

- [ ] `dependency-order`: The graph schedules Storyboard before asset
  resolution, Asset Advisor before its selected execution children, and accepted
  media/timing/edit direction before Remotion. Provider choice is not duplicated
  by the parent, accepted upstream inputs are not reopened, and no production
  owner self-approves.

- [ ] `proof-boundary`: The plan names the required child receipts and terminal
  review/QA path, distinguishes `plan_ready` from materialized production, and
  returns exact action-level blockers instead of generic missing-context prose.

## Reviewer Prompt

```text
Review the canonical content ticket against this checklist. Confirm that its
content action graph is complete, not a second author of child work; each
applicable action has a sole owner and an observable handoff.
Return pass, violation, or deferral with the smallest ownership repair.
```
