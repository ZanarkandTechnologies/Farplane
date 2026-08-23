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

Route UI-first debugging to `visual-qa`, unresolved proof strategy to
`proof-advisor`. Keep shell-heavy command batching, dry runs, rollback, and
focused output in the native execution phase.

<!-- MEM-0001 decision: runtime debugging starts with hypotheses and evidence collection before speculative fixes; visual issues still route to visual-qa. -->
<!-- MEM-0003 decision: runtime-debugging stays thin at the top level and routes bug classes to focused reference playbooks. -->

## Skill Signature

```text
runtime_debugging(symptom, repro?, context?, ensemble?: auto | max) -> root_cause + fix + proof + escalation?
state: reads(code, logs, traces, tests, config, runtime output); writes(instrumentation?, fix?, tests?, evidence?)
gates: repro_or_context_bound; hypotheses_named; evidence_before_fix; proof_after_fix
routes: visual-qa | proof-advisor
fails: speculative fix; noisy instrumentation; no proof rerun; hidden root cause
```

When `ensemble` is requested, load `ensemble.yaml`: `auto` selects three
relevant diverse personas and `max` selects all. Keep independent first passes
bound to the same repro, then synthesize back into the normal root-cause, fix,
proof, and escalation contract.

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
- [ ] 3. Resolve ensemble mode when requested.
   - [ ] Load `ensemble.yaml`; `auto` selects three relevant diverse personas
     and `max` selects all.
   - [ ] Keep nested debugging and proof calls on their normal paths.
- [ ] 4. Map the relevant codepath, callers, side effects, and observability.
- [ ] 5. State 2-4 falsifiable hypotheses and what evidence would separate them.
- [ ] 6. Add the minimum instrumentation, logging, timing marker, counter, or
  repro harness needed to learn something real.
- [ ] 7. Reproduce and collect runtime evidence before patching.
- [ ] 8. Stop or reroute when this is not runtime debugging.
   - [ ] UI-first or visual issue: hand off to `visual-qa`.
   - [ ] Unresolved proof strategy: hand off to `proof-advisor`.
   - [ ] Shell-heavy loop design: keep the command plan inline; batch only
     independent reads, add dry-run/rollback gates, and preserve focused output.
- [ ] 9. Apply the smallest fix that matches the observed root cause.
- [ ] 10. Re-run the repro, remove temporary instrumentation when appropriate,
  and report exact proof that the fix worked.
- [ ] 11. If prevention matters, read
  [root-cause-analysis](references/root-cause-analysis.md) and, for recurring
  learnings, [debugging-knowledge-base](references/debugging-knowledge-base.md).
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not jump to a fix before naming hypotheses and the evidence needed to test
  them.
- Do not add broad noisy logging when one targeted marker, counter, or repro
  test would separate likely causes.
- Do not let ensemble personas replace the core evidence loop; every lane must
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
- [ensemble.yaml](ensemble.yaml) - read for `ensemble: auto | max`.
- [root-cause-analysis](references/root-cause-analysis.md) - read after the fix
  when prevention, postmortem, or residual-risk notes matter.
- [debugging-knowledge-base](references/debugging-knowledge-base.md) - read
  when a recurring learning should be preserved.

## Output

Return or update an artifact with:

- bug intake summary and reproduction path
- selected personas, synthesis, and dissent when ensemble mode was used
- short hypothesis list with what each hypothesis predicts
- instrumentation plan or exact evidence source used
- root cause statement tied to observed runtime behavior
- smallest fix summary
- verification result with exact repro/test proof
- escalation note when another skill should take over
