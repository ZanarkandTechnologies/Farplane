---
name: runtime-debugging
version: 0.1.0
description: "Hypothesis-driven runtime debugging skill for reproducible bugs, flaky failures, regressions, and performance or memory issues where reading code alone is insufficient. Use when you need instrumentation, runtime evidence, root-cause analysis, and proof of the fix."
allowed-tools: Read, Glob, Grep, Bash
---

# Runtime Debugging Skill

Use this for reproducible bugs where static reading is not enough.

<!-- MEM-0001 decision: runtime debugging starts with hypotheses and evidence collection before speculative fixes; visual issues still route to visual-qa. -->
<!-- MEM-0003 decision: runtime-debugging stays thin at the top level and routes bug classes to focused reference playbooks. -->

## First-Load Contract (Non-Negotiable)

### Trigger Conditions

- Reproducible bug, flaky failure, regression, race, perf issue, or leak
- Logs, timestamps, stack traces, support context, or account-specific repro exist
- Root cause is unclear and likely needs instrumentation or repeated runs

Do not use for obvious stack-trace fixes with a direct patch path.

### Workflow (6 Steps)

1. **Intake**: capture exact symptom, repro path, scope, and success criteria.
2. **Map**: inspect the relevant codepath, callers, side-effects, and existing observability.
3. **Hypothesize**: state 2-4 falsifiable causes and what evidence would prove each one.
4. **Instrument**: add the minimum logs, timing markers, counters, or repro test needed to separate those causes.
5. **Observe**: reproduce the bug, collect runtime evidence, and identify the root cause.
6. **Fix and verify**: apply the smallest fix, rerun the repro, remove temporary instrumentation when appropriate, and report proof.

### Bug Type Selector

- **Reproducible runtime bug or regression** -> read [references/runtime-repro.md](references/runtime-repro.md)
- **Straightforward error or stack trace** -> read [references/from-error.md](references/from-error.md)
- **Logs, timestamps, or event sequence** -> read [references/from-logs.md](references/from-logs.md)
- **Flaky, intermittent, or race issue** -> read [references/flaky-race.md](references/flaky-race.md)
- **Performance, memory, or slow network path** -> read [references/perf-memory-network.md](references/perf-memory-network.md)
- **Support ticket or account-specific issue** -> read [references/support-and-account.md](references/support-and-account.md)
- **Unfamiliar code; understand before fixing** -> read [references/understand-first.md](references/understand-first.md)
- **Post-fix root cause and prevention pass** -> read [references/root-cause-analysis.md](references/root-cause-analysis.md)
- **Recurring learnings to preserve** -> read [references/debugging-knowledge-base.md](references/debugging-knowledge-base.md)

### Core Decision Branches

- **Obvious error** -> stay in normal agent mode.
- **UI-first issue** -> hand off to `visual-qa`.
- **Timing-sensitive or intermittent issue** -> prefer repeated runs and targeted instrumentation before patching.
- **No reliable repro** -> stabilize repro first or ask for missing runtime context.

### Top 3 Gotchas

1. Jumping to a fix before naming hypotheses and the evidence needed to test them.
2. Adding broad noisy logging instead of the minimum instrumentation that separates likely causes.
3. Fixing the surface symptom without documenting the root cause, proof, and nearby risks.

### Outcome Contract

When this skill is used, the response or artifact must include:

1. Bug intake summary and reproduction path
2. Short hypothesis list with what each one predicts
3. Instrumentation plan or exact evidence source used
4. Root cause statement tied to observed runtime behavior
5. Smallest fix summary
6. Verification result with exact repro/test proof
7. Escalation note when another skill should take over (`visual-qa`, `testing`, or `bash-efficiency`)

## Skill Boundaries

Own bug intake, hypotheses, instrumentation strategy, runtime evidence analysis, and root-cause confirmation.

Do not duplicate:

- `visual-qa` for browser-first visual or interaction debugging
- `testing` for broader test-strategy routing
- `bash-efficiency` for shell-heavy execution loops

## References

- [references/runtime-repro.md](references/runtime-repro.md)
- [references/from-error.md](references/from-error.md)
- [references/from-logs.md](references/from-logs.md)
- [references/flaky-race.md](references/flaky-race.md)
- [references/perf-memory-network.md](references/perf-memory-network.md)
- [references/support-and-account.md](references/support-and-account.md)
- [references/understand-first.md](references/understand-first.md)
- [references/root-cause-analysis.md](references/root-cause-analysis.md)
- [references/debugging-knowledge-base.md](references/debugging-knowledge-base.md)
