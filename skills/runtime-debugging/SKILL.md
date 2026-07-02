---
name: runtime-debugging
version: 0.1.0
description: "Turn reproducible runtime failures into instrumentation, evidence, root cause, fixes, and proof."
tier: 2
source: local
template_uses:
  skill-template: "0.3.2"
allowed-tools: Read, Glob, Grep, Bash
---

# Runtime Debugging Skill

## Context

Use this for reproducible bugs where static reading is not enough. The skill
owns bug intake, hypotheses, instrumentation strategy, runtime evidence
analysis, and root-cause confirmation.

Route UI-first debugging to `visual-qa`, broad test-strategy routing to
`testing`, shell-heavy execution-loop design to `bash-efficiency`, and budget
resolution to `budget-advisor`.

<!-- MEM-0001 decision: runtime debugging starts with hypotheses and evidence collection before speculative fixes; visual issues still route to visual-qa. -->
<!-- MEM-0003 decision: runtime-debugging stays thin at the top level and routes bug classes to focused reference playbooks. -->

## Skill Signature

```text
runtime_debugging(symptom, repro?, context?, budget?) -> root_cause + fix + proof + escalation?
state: reads(code, logs, traces, tests, config, runtime output); writes(instrumentation?, fix?, tests?, evidence?)
gates: repro_or_context_bound; hypotheses_named; evidence_before_fix; proof_after_fix
routes: visual-qa | testing | bash-efficiency | budget-advisor
fails: speculative fix; noisy instrumentation; no proof rerun; hidden root cause
```

Use `budget-advisor` when `budget` is present:

```text
RuntimeDebuggingBudget = {
  mode?: "base" | "plus" | "max",
  available_time?: string,
  persona_count?: 1 | 3 | 5,
  personas?: RuntimeDebuggingPersona[],
  coverage?: "smoke" | "focused" | "broad",
  evidence_depth?: "light" | "strong",
  delegate_budget?: Record<skill_name, BudgetRequest>
}
```

Child skills use their own base reviewed path unless `delegate_budget`
explicitly names them. Budgeted persona lanes must preserve the normal outcome
contract: root cause, smallest fix, exact verification proof, and escalation
note.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the debugging inputs.
   - [ ] Capture the exact symptom, repro path, scope, environment, and success
     criteria before proposing a fix.
   - [ ] If there is no reliable repro, stabilize the repro or ask only for the
     missing runtime context needed to reproduce.
- [ ] 2. Choose the branch and load only the relevant reference.
   - [ ] Reproducible runtime bug or regression: read
     [runtime-repro](references/runtime-repro.md).
   - [ ] Straightforward error or stack trace: read
     [from-error](references/from-error.md).
   - [ ] Logs, timestamps, or event sequence: read
     [from-logs](references/from-logs.md).
   - [ ] Flaky, intermittent, or race issue: read
     [flaky-race](references/flaky-race.md).
   - [ ] Performance, memory, or slow network path: read
     [perf-memory-network](references/perf-memory-network.md).
   - [ ] Support ticket or account-specific issue: read
     [support-and-account](references/support-and-account.md).
   - [ ] Unfamiliar code; understand before fixing: read
     [understand-first](references/understand-first.md).
- [ ] 3. Resolve budget when present.
   - [ ] Call `budget-advisor` with this skill contract, the bound bug input,
     and `RuntimeDebuggingBudget`.
   - [ ] For `plus` or `max`, use complete persona prompts from
     [budget-personas](references/budget-personas.md) unless the user supplied
     specific personas.
   - [ ] Do not copy the parent budget into nested debugging or proof calls
     unless `delegate_budget` explicitly names the child skill.
- [ ] 4. Map the relevant codepath, callers, side effects, and observability.
- [ ] 5. State 2-4 falsifiable hypotheses and what evidence would separate them.
- [ ] 6. Add the minimum instrumentation, logging, timing marker, counter, or
  repro harness needed to learn something real.
- [ ] 7. Reproduce and collect runtime evidence before patching.
- [ ] 8. Stop or reroute when this is not runtime debugging.
   - [ ] UI-first or visual issue: hand off to `visual-qa`.
   - [ ] Broad testing strategy issue: hand off to `testing`.
   - [ ] Shell-heavy loop design issue: hand off to `bash-efficiency`.
- [ ] 9. Apply the smallest fix that matches the observed root cause.
- [ ] 10. Re-run the repro, remove temporary instrumentation when appropriate,
  and report exact proof that the fix worked.
- [ ] 11. If prevention matters, read
  [root-cause-analysis](references/root-cause-analysis.md) and, for recurring
  learnings, [debugging-knowledge-base](references/debugging-knowledge-base.md).
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
RuntimeDebuggingPersona = {
  name: string,
  prompt: string,
  focus: string[],
  avoid?: string[],
  output_shape?: string
}
```

## Gotchas

- Do not jump to a fix before naming hypotheses and the evidence needed to test
  them.
- Do not add broad noisy logging when one targeted marker, counter, or repro
  test would separate likely causes.
- Do not let budgeted persona councils replace the core evidence loop; every lane must
  feed the same root-cause and verification contract.
- Do not fix the surface symptom without documenting the root cause, proof, and
  nearby risks.

## Reference Map

- [runtime-repro](references/runtime-repro.md) - read for reproducible runtime
  bugs or regressions.
- [from-error](references/from-error.md) - read for straightforward errors,
  exceptions, or stack traces.
- [from-logs](references/from-logs.md) - read when logs, timestamps, traces, or
  event sequences are the primary evidence.
- [flaky-race](references/flaky-race.md) - read for intermittent, timing, or
  concurrency failures.
- [perf-memory-network](references/perf-memory-network.md) - read for
  performance, memory, resource, or network-sensitive runtime failures.
- [support-and-account](references/support-and-account.md) - read for support
  tickets, account-specific repros, or production context.
- [understand-first](references/understand-first.md) - read when the codebase or
  ownership boundary is unfamiliar enough that mapping must precede fixes.
- [budget-personas](references/budget-personas.md) - read when `budget.mode`
  is `plus` or `max` and the caller did not supply complete persona prompts.
- [root-cause-analysis](references/root-cause-analysis.md) - read after the fix
  when prevention, postmortem, or residual-risk notes matter.
- [debugging-knowledge-base](references/debugging-knowledge-base.md) - read
  when a recurring learning should be preserved.
- [budget-advisor](../budget-advisor/SKILL.md) - read when `budget` is present
  and resolve base/plus/max persona council lanes, synthesis, child-budget
  policy, and guardrails before running expanded debugging work.

## Output

Return or update an artifact with:

- bug intake summary and reproduction path
- budget program summary when budget was used, including template refs,
  personas, synthesis, child-budget policy, and source refs
- short hypothesis list with what each hypothesis predicts
- instrumentation plan or exact evidence source used
- root cause statement tied to observed runtime behavior
- smallest fix summary
- verification result with exact repro/test proof
- escalation note when another skill should take over
