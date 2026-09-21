---
name: experimental-research
description: "Turn a technical research question into traced papers, researchers, code, and ranked experiments with reproducibility and learning-value evidence."
tier: 2
source: local
template_uses:
  skill-template: "0.6.2"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, Bash, web_search
---

# Experimental Research

## Context

Use this skill when choosing among research-backed technical approaches or
designing an experiment requires tracing papers, authors, labs, code,
benchmarks, replications, and demonstrations. It owns evidence trails and the
ranked experiment slate. It does not run the experiment or turn the result into
production behavior.

## Skill Signature

```text
experimental_research(question, local_constraints?, evaluation_target?, budget?)
  -> experimental_research_brief + ranked_experiment_slate
reads: papers, citations, author/lab trails, code, datasets, demos, local constraints
does: traces evidence, qualifies approaches, and designs discriminating experiments
writes: none unless the caller supplies an artifact owner
returns: evidence graph, approach ranking, experiment protocols, recommendation
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the decision and falsifiable claims.**
  `research question + constraints -> evaluation contract + hypothesis tree`

  Rule: State the baseline, outcome metric, guard metrics, resource limits,
  transfer assumptions, and the observation that would reject each approach.

  Assert:
  - The hypotheses are distinguishable by an experiment.
  - Marketing or author prestige is not used as an outcome metric.

- [ ] **N2 — Trace papers, people, implementations, and critiques.**
  `hypothesis tree -> evidence graph + candidate approaches`

  Rule: Search arXiv and relevant journals or conferences, then follow backward
  and forward citations, authors, labs, project pages, repositories, datasets,
  replications, critiques, X threads, talks, and YouTube demonstrations. Follow
  [researcher and experiment trails](references/researcher-trails.md).

  Example: `paper claim -> author repo -> missing dataset -> independent
  replication search -> claim downgraded and next query follows the baseline`.

  Assert:
  - Every claim retains paper/version/date provenance and its code/data links.
  - Search continues beyond the first paper, lab, or impressive demo.

- [ ] **N3 — Qualify approaches before deep investigation.**
  `candidate approaches -> finalists + rejection ledger | insufficient-evidence branch`

  Rule: Score relevance, evidence quality, independent replication, artifact
  availability, evaluation comparability, resource fit, and vendor or hardware
  dependency. Promote only candidates that cross the stated threshold.

  Example: `three approaches -> two reproducible on local hardware -> vendor
  demo remains in the rejection ledger`.

  Assert:
  - Top-k is a ceiling and weak candidates remain rejected.
  - Conflicts of interest, missing artifacts, and incomparable benchmarks are explicit.

- [ ] **N4 — Investigate finalists in independent lanes.**
  `finalists -> approach dossiers + evidence conflicts | parallel-lane branch`

  Rule: With multiple finalists and bounded delegation, assign one lane per
  approach or researcher trail. Capture method, data, baseline, metric,
  ablations, negative results, replication, compute/hardware, code maturity,
  and likely transfer failures.

  Assert:
  - Each dossier includes supporting and contrary evidence.
  - Claimed gains are normalized against the actual baseline and protocol.
  - Conflicting evidence updates the hypothesis tree and triggers the next
    discriminating query; exhausted branches backtrack to the best unresolved sibling.

- [ ] **N5 — Rank experiments by learning value and feasibility.**
  `approach dossiers + local constraints -> ranked experiment slate`

  Rule: Prefer the smallest experiment that distinguishes live hypotheses.
  Rank expected information gain, reproducibility, transfer fit, cost, duration,
  and downstream value; state the result that promotes, revises, or stops each
  candidate.

  Assert:
  - Every experiment names the hypothesis, baseline, controlled variables,
    protocol, metrics, artifacts, falsifier, and stop condition.
  - The recommendation states its downside and routes execution to
    `prototyping`, `ml-autoresearch`, or the relevant experiment owner.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Citation count and author reputation are discovery signals, not validation.
- Benchmark wins are incomparable when datasets, baselines, budgets, or metrics differ.
- A polished demo without code, protocol, or independent evidence stays low confidence.

## Output

Return an `Experimental Research Brief` with the evaluation contract,
hypothesis tree, query and researcher trails, evidence graph, candidate and
rejection ledger, approach dossiers, conflicts and transfer risks, followed by
a ranked experiment slate and one recommended next experiment.
