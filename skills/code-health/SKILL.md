---
name: code-health
description: "Use for \"fix this bug\", \"clean this up\", \"review my changes\" or \"audit the codebase\": pick the mode, change the smallest thing, prove behaviour held, report residual risk."
source: local
department: delivery
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Code Health

## Context

Use this when working code needs a bug fixed, a tidy-up, a pre-push review, a
safety pass, or a whole-repo audit. One pass runs one mode on one target and
returns one receipt. It does not design features, plan tickets (`impl-plan`),
debug UI from screenshots (`qa` visual mode), or issue a TAS verdict (`review`).
To map or explain unfamiliar code, use the `explore` agent first. For a Convex
repo, read the official Convex AI instructions before changing backend code.

## Skill Signature

```text
code_health(target, mode?: debug | clean | review | harden | audit) -> branch_receipt
reads: code, tests, git diff and churn, logs or repro, project rules and docs
does: runs one mode behind the lean gate and proves behaviour held
writes: the fix, refactor, mitigation or tests (audit and review write findings only)
returns: finding or fix + proof + residual risk + next owner
```

## Lean Gate

Applies to every mode before any change. Stop at the first sufficient rung:
`skip` (no current need) -> `reuse_local` -> `standard_library` ->
`native_platform` -> `installed_dependency` -> `inline` -> `minimum_new_code`.
Name the rung and its evidence; never a numeric score. A smaller diff is not
lean when it drops a test, safety check, accessibility behaviour, migration, or
proof. Label prototype-only shortcuts as such; prove on the hard case, not the
sample easiest to demo. Example: a date-picker ask lands on `native_platform`
(`<input type="date">`).

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Pick the mode and bind the target.**
  `request + target -> mode + files, callers, behaviour boundary | blocked`

  Rule: Infer the mode: a symptom, error or failing test is `debug`; a diff,
  branch or "before I push" is `review`; tidy, simplify or messy is `clean`;
  safe, robust, abuse or security is `harden`; a whole repo or "what should we
  improve first" is `audit`. A finding outside the mode becomes a follow-up.

  Example: "it's slow and the code is a mess" -> `debug` the measured slow path
  first; `clean` only after the behaviour is locked.

  Assert:
  - One mode and a named target boundary, or the missing input is the blocker.
- [ ] **N2 — debug: find the cause before the fix.**
  `symptom + faithful repro -> observed root cause + smallest fix | escalation`

  Rule: For config, package, discovery or visibility bugs walk effective config
  -> installed package -> item metadata -> consumer visibility, and compare a
  working neighbour before any platform hypothesis. Otherwise list 2-4
  hypotheses ordered by separation power per cost; instrument only the decision
  point that separates them. Load [debug](references/debug.md) for the branch.

  Example: one skill missing from a list -> diff its metadata against a visible
  neighbour -> patch the mismatch, before suspecting a platform cap.

  Assert:
  - The fix is proven on the same repro; a flaky fix passes 20 consecutive runs.
- [ ] **N3 — clean: restructure without changing behaviour.**
  `working code -> locked behaviour + smaller-step refactor + smell delta`

  Rule: Lock behaviour first (existing tests, characterisation tests or
  snapshots). Target smell x change frequency x feature relevance: churned code,
  never whole-repo scores. Small steps, no feature mixed in, no public API
  change unless scoped. On Claude, built-in `/simplify` can apply the fixes.
  Load [clean](references/clean.md) for metrics and tooling.

  Assert:
  - The same proof passes before and after; no split made only to cut lines.
- [ ] **N4 — review: judge the branch as one refactor opportunity.**
  `diff + commits + checks + project rules -> ranked findings + patch_correct`

  Rule: Read the whole branch before any hunk. Look for duplicated helpers
  across commits, parallel abstractions and misplaced modules; ask "would a
  future agent know where to extend this from the folder structure alone?"
  Load [ui-review](references/ui-review.md) when UI, React or Next.js is
  touched. Load [review](references/review.md) for priorities and the JSON
  contract.

  Assert:
  - Findings are actionable and ranked; no style nits.
  - `patch_correct` is false while any blocking finding remains.
- [ ] **N5 — harden: prove each mitigation against its abuse case.**
  `working feature -> ranked risk map + mitigations + adversarial proof`

  Rule: Map entry points and trust boundaries, then rank by impact x likelihood
  x exploitability x exposure. Every mitigation needs a failing or adversarial
  case, or an explicit residual-risk note. Install no scanner, paid service or
  live automation without approval. Load [harden](references/harden.md).

  Assert:
  - Each mitigation names its proof, and intended behaviour still passes.
- [ ] **N6 — audit: rank before reading modules.**
  `codebase + PRD + architecture docs -> ranked waves + one ticket per finding`

  Rule: Rank components by value x centrality x blast radius x churn; audit
  architecture before modules; work in waves. Each finding needs local file,
  command, test or doc evidence and routes to one mode or owner. Newer-model
  confidence is not evidence. Load [audit](references/audit.md).

  Example: "new model, upgrade the whole repo" -> ranked wave of three tickets,
  not a rewrite epic.

  Assert:
  - Low-confidence ideas stay evidence gaps, not implementation tickets.
- [ ] **N7 — Prove and return the branch receipt.**
  `mode output + proof run -> branch receipt | escalation`

  Rule: Re-run the proof that locked behaviour, remove temporary
  instrumentation, and name what remains risky. Escalate to `review` when the
  caller needs a TAS verdict or the change completes a ticket.

  Assert:
  - The receipt names the exact proof command or repro and its result.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Fixing the surface symptom: a null check where bad data surfaced hides the
  upstream cause; trace to the owner that produced it.
- Broad noisy logging instead of one marker that separates hypotheses.
- Reviewing commit by commit: two commits solving one problem in two folders
  only show up at branch level.
- Claiming hardening from a checklist: an untested rate limiter is a residual
  risk, not a mitigation.

## Reference Map

- [debug](references/debug.md) - evidence branches: error, logs, flaky, perf,
  account, unfamiliar code, prevention.
- [clean](references/clean.md) - smell priority, anti-gaming, tooling, stops.
- [review](references/review.md) - priorities, branch consolidation, the
  `patch_correct` JSON contract, escalation. Also loaded by pre-push reviewers.
- [harden](references/harden.md) - risk model, proof choice, residual risk.
- [audit](references/audit.md) - component ranking, architecture pass, finding
  routes, ticket spec.
- [ui-review](references/ui-review.md) - Web Interface Guidelines audit, Vercel
  React/Next.js rules in `references/react-rules/`, Convex pointer.

## Output

```yaml
mode: debug | clean | review | harden | audit
target: <files, boundary>
lean: <rung> + <evidence>
finding_or_fix: <root cause + fix | refactor + smell delta | findings | mitigations | ranked waves + tickets>
proof: <command or repro> -> <result>
residual_risk: <what remains, owner>
next_owner: none | review | <ticket or mode>
```

Review mode also returns the `patch_correct` JSON from
[review](references/review.md).
