---
name: code-review
description: "Turn local diffs and branch context into maintainability, modularity, and code-smell findings before pushing agent-written code."
tier: 2
source: local
skill_template_version: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Code Review

## Context

`code-review` owns maintainability-focused local review. It is the reusable
contract for Codex SDK pre-push reviewers, human local review, and branch-level
consolidation checks before agent-written code is pushed.

The primary failure mode is not "the task did not run." The primary failure
mode is locally sensible code that makes the project worse over time: duplicated
helpers, misplaced modules, oversized files, feature logic split across
unrelated folders, missing docs, and React code that ignores established
project or framework guidance.

This skill is not the material Farplane reviewer lane. Use
[review](../review/SKILL.md) and `agents/reviewer.toml` for TAS-gated plans,
implementations, evidence bundles, skills, prompts, docs, evals, or completion
claims that need an independent verdict.

## Skill Signature

```text
code_review(branch_context, check_logs?, project_rules?, framework_guides?, budget?)
  -> maintainable + findings + consolidation_plan? + follow_ups + escalation?
state: reads(git history since base, changed files, deterministic checks, project/module docs, framework guides); writes(review artifact?)
gates: maintainability_first; cross_commit_consolidation_checked; project_structure_checked; actionable_findings_only
routes: review for material TAS-gated review; external heavyweight review when useful
fails: only checking local correctness; missing duplicated logic across commits; approving misplaced modules; treating lightweight review as TAS pass
```

Review budget is compact:

```text
CodeReviewBudget = {
  scope?: "staged" | "uncommitted" | "branch" | "pre-push";
  strict?: boolean;
  diff_lines?: number;
  include_untracked_contents?: boolean;
}
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Confirm the review input: staged diff, uncommitted diff, branch diff,
  or generated pre-push context.
- [ ] 2. Read the commit list, changed-file list, project rules, module docs,
  and deterministic check output before judging individual code hunks.
- [ ] 3. Look for branch-level consolidation opportunities across all commits:
  duplicated helpers, parallel abstractions, split feature ownership, and
  related changes implemented in different folder structures.
- [ ] 4. Inspect changed files plus the smallest neighboring module surfaces
  needed to verify correct ownership, shared utilities, exports, docs, and
  React patterns.
- [ ] 5. Return only actionable maintainability, modularity, documentation,
  framework-guideline, or correctness findings introduced or exposed by the
  branch.
- [ ] 6. Rank findings by long-term project damage and merge risk: critical,
  high, medium, then low.
- [ ] 7. Decide whether the lightweight review is enough or whether to route to
  [review](../review/SKILL.md), `agents/reviewer.toml`, or an external
  heavyweight review.
- [ ] 8. Review before completion.
  - [ ] No generic style nits.
  - [ ] At least one pass considered cross-commit structure and module
    placement.
  - [ ] Failed checks are explained only when they affect maintainability,
    integration, correctness, or confidence.
  - [ ] `patch_correct` is false when a blocking correctness, security,
    maintainability, modularity, documentation, build, or integration issue
    remains.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Review Priorities

Use this order:

1. Branch maintainability: duplicated domain logic across commits, parallel
   abstractions, over-specific one-off helpers, feature code split across
   unrelated folders, dead compatibility layers, or commits that should be
   consolidated into one shared module.
2. Project structure: misplaced files, module boundaries ignored, public
   exports missing or over-exported, helpers promoted too early, global utility
   buckets used for domain behavior, or module-local docs/tests absent for
   substantial new surfaces.
3. File and API shape: oversized files, deeply nested functions/classes, mixed
   side effects and pure logic, unclear names, broad mutable state, weak types,
   missing return types on exported APIs, or brittle adapter contracts.
4. React and frontend guidelines: component work that ignores installed React
   guidance, creates avoidable rerenders, duplicates derived state, mutates
   props/state, bundles heavy code eagerly, or hides lifecycle cleanup inside ad
   hoc effects.
5. Documentation and operating memory: material new modules without README or
   AGENTS guidance, durable rules left only in code, missing migration notes, or
   stale docs that will mislead the next agent.
6. Correctness, security, and integration: broken runtime behavior, failed
   builds, secret exposure, unsafe inputs, data loss, or adapter/API breaks.

## Branch Consolidation Checks

For pre-push review, judge the branch as a small refactor opportunity, not only
as a pile of independent hunks.

Ask:

- Did two commits solve the same problem in two places?
- Did the branch add a helper near the call site when an existing module, hook,
  adapter, system, or domain library already owns that behavior?
- Did related UI, state, adapter, and docs changes land in different ownership
  surfaces without a clear public module boundary?
- Would future agents know where to extend this feature from the folder
  structure alone?
- Is the right fix to consolidate, extract, rename, or move files before push?

When the answer is yes, return a finding with a concrete consolidation plan,
for example: "move both helpers into `ui/src/modules/runtime/lib/...`, export
only from `modules/runtime/index.ts`, and update both call sites."

## Framework And Project Guides

Use project-local docs first: `PROJECT_RULES.md`, root `AGENTS.md`,
module-local `README.md` / `AGENTS.md`, and `docs/code_review.md`.

When React, Vite, Next.js, client data fetching, rendering, or component
performance is touched, also use the installed `vercel-react-best-practices`
skill when it is available. Treat those rules as advisory maintainability and
performance guidance; project module boundaries still decide where code belongs.

## Output Contract

For SDK or script use, return structured output equivalent to:

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

Use `patch_correct = true` only when there are no blocking maintainability,
modularity, documentation, correctness, security, build, or integration findings
in the reviewed branch scope. Low-risk follow-ups may remain when they are
explicitly non-blocking.

## Escalation Rules

Escalate to `review` or the `reviewer` agent when:

- the caller needs a TAS verdict;
- the change completes a ticket or material plan;
- review depends on evidence quality, UI proof, prompt/skill/eval quality, or
  integration readiness as a hard gate;
- the diff context is too truncated to judge honestly;
- the reviewer finds a systemic issue outside the local diff scope.

Escalate to an external heavyweight PR or branch review only when the branch is
small enough, setup is available, and the operator explicitly wants that pass.

## Gotchas

- Do not read `agents/reviewer.toml` as the default lightweight review prompt.
  That file is an actor identity for material TAS review.
- Do not review each commit as isolated work. The point of pre-push review is to
  catch branch-level consolidation opportunities before the history hardens.
- Do not call a branch merge-ready just because the lightweight review passed.
  It is a second pair of eyes, not a full proof bundle.
- Do not require a ticket pointer for ordinary pre-push diff review. Require one
  only when the caller asks for material TAS review.
- Do not bury check failures in `follow_ups`; put maintainability-impacting or
  confidence-impacting failures in findings or the overall explanation.

## Reference Map

- [review](../review/SKILL.md) - canonical TAS review wrapper and rubric
  contract for material work.
- [docs/review/rubrics/desloppify.md](../../docs/review/rubrics/desloppify.md)
  - anti-slop search playbook for code, cleanup, and integration-heavy review.
- `vercel-react-best-practices` - installed external skill for React and
  Next.js performance, rendering, bundle, and data-fetching guidelines when
  frontend code is touched.
