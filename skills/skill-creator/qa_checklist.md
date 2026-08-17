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
- [ ] The target `SKILL.md` is at most 200 physical lines and its first load is
  executable without hidden chat context: trigger, contract, todo path, gates,
  proof, and output are visible.
- [ ] Template metadata is truthful, conditional references have precise load
  conditions, reference-map link labels name the target surface instead of
  generic basenames such as `SKILL.md`, and reusable method references declare
  `skill-method-reference`.
- [ ] Scaffolding is conservative: no default-path behavior is hidden only in
  references, scripts, examples, audits, or chat, and no placeholders are added
  unless needed.
- [ ] Proof and QA match the behavior risk, including domain-specific todo/QA
  review, skill-local examples, skill-local QA, and skill-maintenance checks
  for material structure or runtime guardrail changes. Behavior-sensitive
  creation hands its canonical `evals/evals.json` to `eval` for evidence-backed
  execution and candidate/baseline comparison; `skill-creator` does not
  self-grade or own a parallel eval runner.

## Domain-Specificity Rubric

Use this compact rubric when a new or revised skill could become generic
assistant scaffolding:

```text
todo_specificity_check(skill_domain, todo_list, qa_checklist?)
  -> pass | weak | violation
```

- `pass`: the todo path names the domain's real inputs, transformations,
  artifacts, quality bars, and failure modes.
- `weak`: the todo path has a few domain words, but most actions could be
  pasted into unrelated skills with minor edits.
- `violation`: the todo path mostly says to gather context, draft, review, and
  finalize without teaching the agent the domain's distinctive strategy.

Repair `weak` or `violation` by adding at least one domain-specific workflow
move, one judgment gate, and one positive example or fixture before polishing
checklist prose.
