---
template_uses:
  skill-method-reference: "0.1.0"
---

# Low-Value Prose Scan

Use this reference during `refine_skill`, structure review, or compacting a
skill that feels bloated. It is a reusable subworkflow for `skill-maintenance`,
not a standalone script or validator.

```text
low_value_prose_scan(target_skill, claim?, context?)
  -> sentence_decisions + skill_delta_recommendation + evidence_note
state: reads(target SKILL.md, target qa_checklist.md?, relevant references?, audits?); writes(audit notes or owner-local edits when requested)
gates: sentence_value_decided; required_behavior_preserved; edits_classified
fails: deletes useful gates; keeps generic aspiration; treats length as the problem
```

## Use When

- A skill feels wordy, over-explained, moralizing, or bloated.
- A `refine_skill` pass needs to shorten first load without hiding required
  behavior.
- A reviewer asks whether prose actually changes execution, routing, proof,
  safety, ownership, or maintenance decisions.

## Inputs

```text
input_packet:
  required:
    target_skill: skills/<name>/SKILL.md
  optional:
    claim: what behavior should remain true after cleanup
    context: target qa_checklist.md, references, recent audit, usage evidence
  source_refs:
    - skills/skill-maintenance/qa_checklist.md
    - target skill package
```

## Workflow

1. **Slice sentences.** Review `SKILL.md` sentence by sentence, section by
   section, skipping code fences, frontmatter, and template literals.
2. **Apply the value test.** For each sentence, ask whether it changes at least
   one of these:
   - trigger or non-trigger boundary
   - next action in the todo path
   - branch routing or reference loading
   - required input, state read/write, output, proof, gate, or stop condition
   - safety, external side effect, or human handoff behavior
   - maintenance ownership or validation command
3. **Flag bullshit smells.** Mark candidates that match any smell:
   - "important", "helpful", "useful", "better", "robust", or "high-quality"
     without a concrete behavior or proof surface
   - "agents should be thoughtful/careful" where a gate would work
   - philosophy, history, or rationale in first load
   - workflow prose that repeats the numbered todo list
   - a sentence that could be pasted into five unrelated skills unchanged
4. **Classify each candidate.**
   - `keep`: it changes execution, routing, proof, safety, or ownership.
   - `rewrite`: it contains a useful rule but should become a todo, gate,
     route, fail, output condition, or reference load condition.
   - `move`: it is useful only after a branch is chosen; move it to
     `references/*`.
   - `delete`: it is rationale, aspiration, reassurance, duplicated workflow
     prose, or a generic quality claim with no executable consequence.
5. **Patch only after classification.** Preserve required behavior first, then
   apply the smallest owner-local edit and record the classification summary in
   the audit or final proof note.

## Output Shape

```text
low_value_prose_scan:
  target:
  candidates:
    - line:
      sentence:
      smell:
      decision: keep | rewrite | move | delete
      reason:
  skill_delta_recommendation:
  evidence_note:
  blockers:
```

## Quality Gates

- Every removed or moved sentence has a `rewrite | move | delete` decision.
- Required gates, routing, proof, and output contracts remain in first load.
- "Shorter" is never the proof; behavior preservation is the proof.

## Bad Output

- "This is fluff" with no sentence quote, smell, or decision.
- Deleting long text only because it is long.
- Keeping generic advice because it sounds nice.
- Moving required routing, proof, or stop conditions into a reference.
