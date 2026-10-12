# Review Mode

Load after `SKILL.md` selects `review`. This file is also the contract that
project pre-push reviewers load (setup-advisor's `scripts/codex_review_agent.ts`
reads `~/.codex/skills/code-health/references/review.md`), so it stands alone.

Review mode is a maintainability-first second pair of eyes for a staged,
uncommitted, branch or pre-push diff. The failure it exists to catch is locally
sensible code that makes the project worse over time: duplicated helpers,
misplaced modules, oversized files, a feature split across unrelated folders,
missing docs, and frontend code that ignores project or framework guidance. It
is not a TAS verdict; that belongs to the `review` skill and the reviewer agent.

## Order of work

1. Confirm the input: staged, uncommitted, branch, or generated pre-push
   context.
2. Read the commit list, changed-file list, project rules, module docs and
   deterministic check output before judging any hunk.
3. Look across all commits for consolidation opportunities.
4. Inspect changed files plus the smallest neighbouring modules needed to check
   ownership, shared utilities, exports, docs and framework patterns.
5. Return only actionable findings the branch introduced or exposed, ranked by
   long-term damage and merge risk: critical, high, medium, low.

## Priorities

1. Branch maintainability: the same domain logic in two commits, parallel
   abstractions, one-off helpers, feature code split across unrelated folders,
   dead compatibility layers.
2. Project structure: misplaced files, ignored module boundaries, missing or
   over-broad exports, global utility buckets holding domain behaviour,
   substantial new surfaces without module docs or tests.
3. File and API shape: oversized files, deep nesting, side effects mixed with
   pure logic, unclear names, broad mutable state, weak exported types.
4. Frontend: avoidable rerenders, duplicated derived state, mutated props or
   state, heavy eager bundles, ad hoc effects hiding cleanup. When React,
   Next.js or client data fetching is touched, apply
   [ui-review](ui-review.md) and its React rules; project module boundaries still decide
   where code belongs.
5. Docs and operating memory: new modules without README or AGENTS guidance,
   durable rules left only in code, stale docs that will mislead the next agent.
6. Correctness, security and integration: broken behaviour, failed builds,
   secret exposure, unsafe inputs, data loss, adapter or API breaks.

## Branch consolidation questions

- Did two commits solve the same problem in two places?
- Did the branch add a helper near the call site when an existing module, hook,
  adapter or domain library already owns that behaviour?
- Did related UI, state, adapter and docs changes land in different ownership
  surfaces without a clear public module boundary?
- Would a future agent know where to extend this feature from the folder
  structure alone?
- Is the right fix to consolidate, extract, rename or move files before push?

When the answer is yes, the finding carries a concrete plan, for example: "move
both helpers into `src/modules/runtime/lib/`, export only from
`modules/runtime/index.ts`, and update both call sites." For docs, skills,
registries or eval rows, route the consolidation to `doc-advisor` consolidate mode.

## Project overlay

Use project docs first: root `AGENTS.md`, module `README.md` or `AGENTS.md`, and
`docs/code_review.md` when present.

## Output contract

```json
{
  "patch_correct": true,
  "overall_explanation": "Short grounded verdict.",
  "confidence": 0.82,
  "findings": [
    {
      "severity": "high",
      "file": "src/example.ts",
      "line": 42,
      "title": "Specific issue",
      "body": "Why this harms maintainability or project structure.",
      "recommendation": "Concrete consolidation, move, extraction, or fix."
    }
  ],
  "follow_ups": ["Escalate to review if this is the final ticket proof."]
}
```

`patch_correct` is true only when no blocking maintainability, modularity,
documentation, correctness, security, build or integration finding remains in
the reviewed scope. Non-blocking follow-ups may remain when marked as such.
Put check failures that affect maintainability or confidence in findings or the
explanation, not in `follow_ups`.

## Escalation

Escalate to the `review` skill or the reviewer agent when the caller needs a
TAS verdict, the change completes a ticket or material plan, readiness depends
on evidence, UI, prompt, skill or eval quality, the diff is too truncated to
judge honestly, or the issue is systemic beyond the diff. A passing review mode
is not merge-readiness proof. Do not require a ticket pointer for ordinary
pre-push review.
