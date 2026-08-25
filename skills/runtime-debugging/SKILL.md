---
name: runtime-debugging
version: 0.1.0
description: "Turn reproducible runtime failures into instrumentation, evidence, root cause, fixes, and proof."
tier: 2
source: local
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep, Bash
---

# Runtime Debugging Skill

## Context

Use this for reproducible bugs where static reading is not enough. The skill
owns bug intake, hypotheses, instrumentation strategy, runtime evidence
analysis, and root-cause confirmation.

For configuration, package, discovery, or visibility failures, inspect the
affected item's nearest owner control before tracing global platform internals.

Route UI-first debugging to `visual-qa`, unresolved proof strategy to
`proof-advisor`. Keep shell-heavy command batching, dry runs, rollback, and
focused output in the native execution phase.

<!-- MEM-0001 decision: runtime debugging starts with hypotheses and evidence collection before speculative fixes; visual issues still route to visual-qa. -->
<!-- MEM-0003 decision: runtime-debugging stays thin at the top level and routes bug classes to focused reference playbooks. -->

## Skill Signature

```text
runtime_debugging(symptom, repro?, context?, ensemble?: auto | max) -> root_cause + fix + proof + escalation?
reads: code, logs, traces, tests, configuration, and runtime output
does: separates falsifiable causes from runtime evidence, applies the smallest
  matching fix, and proves the result
writes: instrumentation, fix, tests, or evidence when required
returns: root cause, smallest fix, verification proof, or a routed escalation
```

When `ensemble` is requested, load `ensemble.yaml`: `auto` selects three
relevant diverse personas and `max` selects all. Keep independent first passes
bound to the same repro, then synthesize back into the normal root-cause, fix,
proof, and escalation contract.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Qualify the runtime failure and select its evidence branch.**
  `symptom + repro + environment -> bounded repro + diagnostic reference | missing context`

  Rule: Capture expected versus actual behavior, scope, and success condition;
  load exactly one matching reference from the Reference Map. If the issue is
  visual, route to `visual-qa`; if only proof design is unresolved, route to
  `proof-advisor`.

  Assert:
  - The exact failing behavior and one faithful repro are named, or the missing
    runtime context is the explicit blocker.
  - The selected branch matches the evidence source, not a guessed fix.

- [ ] **N2 — Traverse the shortest control path before broad research.**
  `bounded repro + runtime state -> explanatory mismatch | remaining hypotheses`

  Rule: For configuration, package, discovery, visibility, or routing symptoms,
  inspect effective config -> installed package -> nearest item metadata ->
  consumer visibility. Patch and rerun when the first mismatch explains the
  symptom; only then expand to binaries, release sources, or broad codepaths.

  Assert:
  - The cheapest discriminating local check is recorded before broad research.
  - Any escalation names the local checks that did not explain the symptom.

  Example: `missing skill -> compare working neighbor -> local metadata mismatch
  -> patch and rerun`, before forming a platform-capacity hypothesis.

- [ ] **N3 — Separate the remaining causes with evidence.**
  `unexplained repro -> 2-4 predictions + minimum observation plan -> observed runtime evidence`

  Rule: Order hypotheses by separation power per cost. Add a targeted log,
  counter, timing marker, or repro harness only when existing runtime state
  cannot separate them.

  Assert:
  - Each hypothesis predicts distinct evidence.
  - Instrumentation observes a decision point and is no broader than needed.

- [ ] **N4 — Fix the observed root cause at its smallest owner boundary.**
  `observed evidence -> root-cause statement + smallest matching fix | reroute`

  Rule: Do not patch a surface symptom. Keep shell-heavy command plans inline,
  batch only independent reads, and preserve dry-run or rollback gates.

  Assert:
  - The cause is tied to observed runtime behavior, not a coincidence.
  - The patch changes the owner that produced that behavior.

- [ ] **N5 — Prove the fix and promote prevention only when warranted.**
  `fix + same repro -> verification receipt + residual risk | prevention follow-up`

  Rule: Re-run the same repro, remove temporary instrumentation when useful,
  and report exact proof. Load [root-cause-analysis](references/root-cause-analysis.md)
  only for prevention or postmortem work, and
  [debugging-knowledge-base](references/debugging-knowledge-base.md) only for
  a recurring learning.

  Assert:
  - The before/after behavior is demonstrated by the same repro or a named
    fidelity limitation.
  - A prevention follow-up has a durable owner or is explicitly declined.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not jump to a fix before naming hypotheses and the evidence needed to test
  them.
- Do not add broad noisy logging when one targeted marker, counter, or repro
  test would separate likely causes.
- Do not promote a count coincidence or ambiguous side effect into a platform
  hypothesis before inspecting the affected item's local control metadata.
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
