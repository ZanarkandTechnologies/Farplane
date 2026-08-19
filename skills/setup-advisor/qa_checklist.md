---
title: Setup Advisor QA Checklist
owner: setup-advisor
status: active
kind: qa-checklist
applies_to:
  - setup-receipts
  - generated-setup-wizards
---

# Setup Advisor QA Checklist

Read before operating a setup and apply again before returning its receipt.

```text
setup_qa(project_state, setup_map, changes, wizard?, receipt)
  -> pass | violation | blocked
```

## Checklist

- [ ] Discovery covers relevant repo configuration and CI references, and
  every prescribed command or dashboard journey is grounded in current
  official provider documentation rather than memory. The receipt names every
  source actually inspected with its URL, or marks it not inspected and limits
  the claim accordingly. Fixture URLs and recalled URLs do not prove
  inspection. Read-only fixtures and supplied-context-only plans default to
  `not_inspected`; account for every discovered dependency or safety step in
  the setup map.
- [ ] Every safe authorized automatable step was attempted by the agent before
  assigning a human gate; external, destructive, spend, deploy, DNS, legal,
  and account-authority boundaries remain explicit. Wizard stages never bundle
  an automatable install, local write, link, or probe into the human action.
- [ ] Secret values never appear in tracked files, commands shown in chat,
  logs, receipts, or verification output; destinations are named and Farplane
  projects default to Doppler for runtime secrets. Every captured value maps to
  one exact destination store and key rather than a broad category. Presence
  checks list names or exercise a redacted consumer and never retrieve a plain
  secret value.
- [ ] Each generated wizard has accurate dependency-ordered stages, one focused
  human task per stage, safe reruns, exact value destinations, confirmation for
  irreversible actions, and passing `bash -n` plus `shellcheck` when available.
- [ ] The receipt gives every requested service one honest status, cites
  redacted verification evidence, distinguishes remaining human work from
  completion, and includes rollback or recovery for material changes. A
  cutover includes explicit pre-change and post-change routing, delivery, or
  consumer probes rather than treating rollback triggers as verification.

## Reviewer Prompt

```text
Review the setup map, changes, wizard, and receipt against
skills/setup-advisor/qa_checklist.md. Return pass, violation, or blocked for
each item with exact artifact evidence. Never request or reproduce secret
values. Treat an unverified configured status as a violation.
```
