---
template_uses:
  skill-qa-checklist: "0.1.0"
---

# Skill Creator QA Checklist

Use this checklist as preflight guardrails before creating or updating a skill,
then apply it again before claiming completion. Record each item as `pass`,
`violation`, `not_applicable`, or `deferred` in the audit or final proof notes
for material skill work.

## Checklist

- [ ] Ownership is explicit: create a new skill only for a stable reusable
  trigger; otherwise update the existing owner surface.
- [ ] The target `SKILL.md` first load is executable without hidden chat context:
  trigger, contract, todo path, gates, proof, and output are visible.
- [ ] Template metadata is truthful, conditional references have precise load
  conditions, and reusable method references declare `skill-method-reference`.
- [ ] Scaffolding is conservative: no default-path behavior is hidden only in
  references, scripts, examples, audits, or chat, and no placeholders are added
  unless needed.
- [ ] Proof and QA match the behavior risk, including skill-local and
  skill-maintenance checklists for material structure or runtime guardrail
  changes.
