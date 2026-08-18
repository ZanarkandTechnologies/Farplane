---
skill: newsletter-writer
date: 2026-08-18
change_type: behavior
owner: skill-creator
status: pass
review_route: reviewer
before_ref: skills/copywriting-advisor; Zanarkand weekly-office-showcase formatter
after_ref: skills/newsletter-writer
reasoning_basis: first_principles + best-of-worlds + reviewer
proof_artifacts:
  - skills/newsletter-writer/examples/weekly-office-showcase/example.md
  - skills/newsletter-writer/evals/evals.json
  - .farplane/evals/runs/20260817-205120-newsletter-writer-final/summary.json
  - .farplane/evals/runs/20260817-204557-newsletter-writer-baseline/summary.json
  - skills/newsletter-writer/audits/2026-08-18-review.json
eval_required: yes
eval_result: pass
no_self_improve_reason: "A bounded upstream adaptation now has a focused 3/3 eval and does not need an ongoing Goal-backed optimization loop."
---

# Newsletter Writer Upstream Import Audit

## Change

- Before: Farplane had page conversion copy and SEO/article skills, while the
  company showcase formatter converted evidence cards directly into generic
  project paragraphs.
- After: one marketing skill owns recurring newsletter blueprint, issue,
  editorial QA, source receipt, and human publication gate.
- Why: recurring relationship writing has a stable trigger and a distinct
  artifact contract that neither page copy nor evidence aggregation owns.
- Tradeoff accepted: one additional Tier 3 skill is preferable to bloating the
  evidence aggregator or weakening the page-specific copywriting contract.

## Source Inventory

| Source | Type | Version / recency | Credibility | Use |
| --- | --- | --- | --- | --- |
| `sanky369/vibe-building-skills/skills/marketing/newsletter/SKILL.md` | maintained implementation | commit `e9714d8decbc9a76eaab3bd85866117b8010e9bc`, inspected 2026-08-18 | primary source; MIT licensed | upstream workflow and quality-bar baseline |
| `skills/copywriting-advisor` | local implementation | current checkout | canonical local page-copy owner | boundary and reusable source-truth discipline |
| Zanarkand `weekly-office-showcase` | local implementation | current local package | canonical evidence aggregator | before behavior and downstream input contract |

## Best-Of-Worlds Decisions

| Feature | Source | Evidence | Scores: value/evidence/transfer/cost/risk/synergy | Decision | Reason |
| --- | --- | --- | --- | --- | --- |
| Newsletter as recurring relationship | upstream | prime directive and intake | 5/4/5/5/5/5 | adopt | directly corrects activity-digest prose |
| Six formats with decision rules | upstream | explicit format/cadence table | 5/4/5/4/5/5 | adopt | provides a real editorial branch without new runtime code |
| Exactly one idea and one CTA | upstream | draft and QA contract | 5/5/5/5/5/5 | adopt | strongest guard against report-shaped sludge |
| Subject/preview/paragraph limits | upstream | deterministic quality checks | 4/5/5/5/5/5 | adopt | cheap and inspectable mobile/email guardrails |
| Voice from examples | upstream + local copy skill | voice intake and source atoms | 5/4/5/4/5/5 | adapt | add explicit hypothesis mode and ban invented autobiography |
| External skill routing | upstream | references to its own marketing suite | 2/4/2/3/3/1 | reject | those packages are not Farplane owners |
| Direct drafting inside showcase aggregator | local formatter | current fixture output | 2/5/4/5/3/2 | reject | mixes evidence selection with editorial judgment |
| Publishing automation | neither source authorizes it | explicit publication gates | 1/5/5/5/5/5 | reject | human approval remains mandatory |
| Open/reply optimization | upstream blueprint metrics | metrics list | 3/3/4/3/4/3 | defer | needs real Beehiiv history before optimization |

## Placement Decision

- Primary lever: one local Tier 3 `skills/newsletter-writer/` contract.
- Rejected primary surface — `weekly-office-showcase`: keep it responsible for
  allowlisted evidence, privacy, exclusions, and facts; it should supply an
  editorial brief rather than own prose quality.
- Rejected primary surface — `copywriting-advisor`: its awareness-stage,
  persuasion-formula, and page-section contract would distort a recurring
  relationship issue.
- Rejected primary surfaces — `AGENTS.md`, global template, agent prompt,
  hook, validator, and script: newsletter judgment is selected, non-global,
  human-judged work rather than universal policy or deterministic runtime.
- Secondary sync: generated skill registry and later Zanarkand showcase handoff.
- Proof: structure validator, skill-local evals, source-based preview, and
  independent skill-contract review.

## Lean Receipt

```yaml
target: recurring newsletter writing from verified weekly office facts
current_need: the existing formatter produces accurate but generic activity prose
rung: minimum_new_code
evidence:
  - no newsletter owner exists in docs/skills/registry.jsonl
  - copywriting-advisor owns page conversion copy
  - weekly-office-showcase owns evidence aggregation and publication safety
smallest_next_action: add one text-only skill package and one representative example
proof_preserved: source truth, privacy exclusions, and human publication approval remain mandatory
review_route: review:skill-contract+integration-readiness+evidence-quality
```

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | trigger, signature, five-step todo, format rules, template, gate |
| `reference_load_precision` | pass | only the long showcase example is conditional |
| `missing_context_rate` | pass | audience, evidence, voice, goal, format, cadence inputs named |
| `noisy_context_rate` | pass | external suite routing and tutorial detail removed |
| `duplicated_instruction_count` | pass | evidence selection remains upstream; prose remains here |
| `prompt_size_tokens` | pass | `SKILL.md` is 199 physical lines and the surface-budget validator passes |
| `task_success_rate` | pass | final focused suite is TAS-A 3/3; no-skill baseline is 0/3 |
| `review_tas_rate` | pass | independent completion review is TAS-A |
| `maintenance_locality` | pass | one owner-local package |
| `composition_clarity` | pass | aggregator -> editorial brief -> newsletter issue boundary |

## Before Behavior

- Three generic subject candidates.
- One paragraph per selected project card.
- No one-idea selection, relationship promise, format choice, voice mode, CTA
  discipline, or editorial rewrite pass.

## After Behavior

- One audience-bound idea uses project cards as proof.
- Six sustainable issue formats, deterministic subject/preview constraints,
  one CTA, source receipt, hypothesis-voice branch, and publication approval.
- A source-grounded weekly-office preview demonstrates the intended handoff.

## Followups

- Integrate the Zanarkand showcase handoff in its owning checkout after this
  reusable skill is accepted; do not edit that external checkout from here.

## Eval Evidence

- Initial run: 0/3, exposing over-blocking and an overly rigid word target.
- Repaired full run: 2/3; the remaining blocked-response case was tightened.
- Smallest failing-case rerun: TAS-A 1/1.
- Final post-repair suite: TAS-A 3/3 at
  `.farplane/evals/runs/20260817-205120-newsletter-writer-final/summary.json`.
- Same prompts without skill context: 0/3 at
  `.farplane/evals/runs/20260817-204557-newsletter-writer-baseline/summary.json`.
- Rerun rule: fix the smallest failing case, rerun it, then require one clean
  full-suite 3/3 result before readiness.
