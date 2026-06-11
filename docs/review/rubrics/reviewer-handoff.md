# Reviewer Handoff

Use this when a caller skill, ticket, or workflow asks the native `reviewer`
agent to run material review.

## Ownership

- The calling skill or workflow owns rubric routing because it knows the domain
  intent.
- The ticket `Proof Contract` stores the filled-in handoff for ticketed work.
- The reviewer validates the declared routing and may add an obvious missing
  hard-gate family with a short explanation.
- The `review` skill owns TAS semantics, family definitions, hard gates, and
  output shape.

## Template

```json
{
  "task_path": "tickets/TASK-XXXX/ticket.md",
  "review_focus": "implementation | planning | skill-change | prompt-change | eval-change | docs | evidence | demo | video | completion",
  "changed_files": [],
  "evidence": [],
  "rubric_families": [],
  "required_tas": {
    "evidence-quality": "TAS-A",
    "integration-readiness": "TAS-A"
  },
  "hard_gates": [],
  "expected_output": "tickets/TASK-XXXX/artifacts/review/<timestamp>-review.json"
}
```

## Caller Defaults

Use these as starting points, then narrow or expand based on the concrete task:

- Planning: `spec-contract`, `implementation-plan`, `evidence-quality`
- Code/backend/api: `code-quality`, `integration-readiness`,
  `evidence-quality`
- Skill or harness-workflow change: `skill-contract`,
  `integration-readiness`, `evidence-quality`
- Prompt change: `prompt-quality`, `evidence-quality`,
  `integration-readiness`
- Eval change: `eval-quality`, `evidence-quality`, `integration-readiness`
- UI or user-facing workflow: `user-intent-satisfaction`, `ui-quality`,
  `frontend-guidelines`, `frontend-code-maintainability` when source structure
  matters, `vercel-react-best-practices` when React/Next.js performance is in
  scope, and `evidence-quality`
- Cleanup/refactor/runtime/doc simplification: `debloatability`,
  `integration-readiness`, `evidence-quality`
- Final completion review: `user-intent-satisfaction` when user-facing,
  `integration-readiness`, `evidence-quality`

## Skill-Change Gate

For skill creation or maintenance, include these hard gates when relevant:

- Another agent can rerun the skill from files alone.
- First-load checklist logic is concise, branch-aware, and not duplicated
  across references.
- Actor identity, subagent routing, tool policy, and artifact writeback stay in
  actor prompts or caller workflows, not reusable skill contracts.
- Proof commands and generated-registry sync are explicit.

## Output

The reviewer returns or writes the standard review result:

- `work_type`
- `search_scope`
- `rubrics_used`
- `overall_tas`
- `verdict`
- `rerun_required`
- `hard_gate_failures`
- `finding_log`
- `rubric_sections`
- `blocking_findings`
- `next_action`
