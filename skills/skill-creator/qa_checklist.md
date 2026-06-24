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

- [ ] Ownership is explicit: the change creates a new skill only for a stable
  reusable trigger; otherwise it updates an existing `SKILL.md`, reference,
  script, eval, checklist, or template surface.
- [ ] The target `SKILL.md` first load is executable without hidden chat
  context: trigger, signature or equivalent contract, todo path, gates, proof,
  and output are visible.
- [ ] The target skill uses current template metadata truthfully; do not stamp
  `template_uses.skill-template` unless structure matches that version.
- [ ] Conditional references are linked from `SKILL.md` with precise load
  conditions; reusable method references declare `skill-method-reference`.
- [ ] No default-path behavior is hidden only in references, scripts, examples,
  audits, or chat.
- [ ] Scaffolding is conservative: no placeholder helper scripts, empty
  references, assets, prompts, or templates are created unless the skill needs
  them.
- [ ] Proof matches the behavior risk: validators for mechanical structure,
  script smoke for scripts, eval or behavior test for agent-comprehension
  claims, and explicit blocker when proof cannot run.
- [ ] QA is named, not hand-waved: the skill-local checklist and the
  skill-maintenance structure checklist were applied when material structure or
  runtime guardrails changed.
