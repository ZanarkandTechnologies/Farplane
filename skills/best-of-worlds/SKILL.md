---
name: best-of-worlds
version: 0.1.0
description: Use when the user gives multiple projects, GitHub URLs, tools, blogs, repos, or implementations and wants the best features extracted, scored, adapted, and turned into a concrete workflow or implementation plan.
allowed-tools: Read, Glob, Grep
---

# Best Of Worlds

Build a best-of-all-worlds design from multiple source projects without turning
research into a feature dump. This skill compares real implementations, extracts
transferable features, discovers useful metrics when the target is fuzzy, and
returns adopt/adapt/reject decisions with an implementation handoff.

Codexter skills are stable local contracts. External skills, repos, blogs, and
command families are research inputs, not live dependencies. This skill is the
normal import gate for outside ideas: decide `adopt`, `adapt`, `reject`, or
`defer` before changing local skill behavior. See `MEM-0073`.

## Trigger Conditions

Use when the user asks to:

- compare several GitHub repos, projects, products, blogs, or implementations
- pick the best features from multiple sources
- design a unified workflow from competing examples
- decide what to adopt, adapt, reject, or defer
- find metrics or judgement questions before optimizing a workflow

Use [research:parity](../research/SKILL.md#researchparity) when the ask is
only "what do peers include?" Use
[research:gap](../research/SKILL.md#researchgap) when the local missing scope
is already the main question. Use
[research:source-synthesis](../research/SKILL.md#researchsource-synthesis) to
normalize source facts before this skill when the source set is noisy.

## Workflow

1. **Frame target:** define the target user, job-to-be-done, artifact to change,
   and any local constraints.
2. **Catalog sources:** list each URL/repo/project, source type, credibility,
   recency, and why it is relevant.
3. **Extract features:** capture concrete features, workflows, file structures,
   guardrails, scripts, metrics, and operating practices from each source.
4. **Discover metrics:** if the optimization target is fuzzy, build a metric
   card with primary metric, guard metrics, anti-metrics, and judgement
   questions.
5. **Score candidates:** rate each feature for user value, transferability,
   evidence strength, implementation cost, risk, and synergy with other
   features.
6. **Decide:** mark each feature `adopt`, `adapt`, `reject`, or `defer`, with a
   one-line reason and source evidence.
7. **Synthesize:** produce the recommended best-of-worlds workflow, file layout,
   metric contract, and implementation steps.
8. **Handoff:** route implementation to the right skill such as
   `impl-plan`, `autoresearch-plan`, `self-improve`, `research:gap`, or
   `functional-ui`.

Load `references/feature-scoring.md` before scoring features and
`references/metric-discovery.md` when the metric is unclear.

## Judgement Questions

Use `advise` when these cannot be answered mechanically:

- Which source is most credible for the target user and why?
- Is this feature a must-have, a useful adaptation, or distracting parity bait?
- What metric would prove the combined workflow is better?
- Which guard metric prevents gaming the primary metric?
- What should be rejected even if it looks impressive?

## Artifact Setup

For bigger comparisons, scaffold a durable synthesis workspace:

```bash
python3 skills/best-of-worlds/scripts/init_synthesis.py \
  --name autoresearch-skill-suite \
  --target "Codexter skill self-improvement workflow" \
  --source https://github.com/karpathy/autoresearch \
  --source https://www.mindstudio.ai/blog/claude-code-autoresearch-self-improving-skills
```

This creates:

```text
experiments/best-of-worlds/<name>/
  sources.jsonl
  feature-ledger.md
  decision-matrix.md
  metrics.md
  handoff.md
```

## Core Decision Branches

- **Sources are mostly code repos:** use code/repo exploration first, then score
  implementation patterns.
- **Sources are mostly blogs/docs:** extract workflows and file contracts, then
  verify against real repos where possible.
- **Metric is unknown:** use the metric discovery card before recommending
  implementation.
- **Feature is source-specific:** adapt only the underlying principle, not the
  exact file layout or vendor assumptions.
- **User wants changes now:** produce the decision matrix, then implement only
  the adopted/adapted features that fit the current repo.

## Top Gotchas

1. Do not merge every attractive idea; reject flashy features that do not serve
   the target job.
2. Do not treat a blog claim as implementation evidence when a repo or official
   doc can verify it.
3. Do not optimize without a primary metric, guard metric, or explicit
   judgement-call reason.
4. Do not bury tradeoffs; every adopt/adapt/reject decision needs a reason.
5. Do not skip local constraints when copying layouts from another ecosystem.

## Outcome Contract

After this skill runs, the output should include:

- source inventory with links and credibility notes
- feature ledger with source evidence
- metric card or judgement questions
- adopt/adapt/reject/defer decision matrix
- recommended best-of-worlds workflow or file layout
- implementation handoff with next skill or direct changes

Reference split:

- `references/architecture.md` for boundaries with parity/gap/advise
- `references/workflows.md` for detailed phases
- `references/gotchas.md` for research and synthesis failure modes
- `references/feature-scoring.md` for the decision matrix
- `references/metric-discovery.md` for metrics when the target is fuzzy
- `references/judgement-calls.md` for generalized advise-style questions
