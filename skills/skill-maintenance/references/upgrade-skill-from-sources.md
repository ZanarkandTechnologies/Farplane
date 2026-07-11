---
template_uses:
  skill-method-reference: "0.1.0"
---

# Upgrade Skill From Sources

Use this reference when an existing skill is structurally valid but too generic
or underpowered for its domain. The goal is not research notes. The goal is an
owner-local skill delta: stronger workflow moves, gates, examples, evals, or QA
checks.

```text
upgrade_skill_from_sources(target_skill, improvement_goal, source_budget?)
  -> source_packet + best_of_worlds_decisions + skill_delta + proof_plan
state: reads(target skill package, practitioner sources, public book summaries,
             video transcripts when available, book-to-skill extraction,
             best-of-worlds, skill-system docs)
       writes(target skill SKILL.md?, qa_checklist.md?, references?,
              examples?, evals/evals.json?, skill-local audit?)
gates: target_baseline_named; source_budget_bounded; source_confidence_labeled;
       book_inputs_use_book_to_skill; adopt_adapt_reject_recorded;
       owner_local_delta_applied; validation_run
fails: generic research dump; raw transcript pasted into repo; book-summary
       substitute; copies source prose; upgrades every shiny idea; skips proof
```

## Use When

- An existing skill is structurally valid but too generic for its domain.
- The operator asks to improve a skill from current practice, articles, books,
  frameworks, public summaries, videos, or source material.
- A skill needs stronger workflow moves, quality gates, examples, or evals
  before it can be trusted for real work.

Do not use this for tiny mechanical metadata edits, installed-copy imports, or
pure compaction. Use normal `harden_skill`, `refine_skill`, or
`low_value_prose_scan` for those.

## Inputs

```text
upgrade_skill_input:
  target_skill:
  improvement_goal:
  source_budget:
    practitioner_articles: 3
    books_or_frameworks: 3
  source_mode: discovery | pilot | full
  proof_need:
```

### Source Budget

Default to a representative pass before scaling:

- `3` practitioner articles, guides, talks, or current platform docs.
- `3` books, frameworks, public book notes, author interviews, lectures, or
  book-summary videos.
- For a pilot, one strong article plus one strong book-summary source is enough
  per skill when several skills are being sampled in one run.

Prefer workflow-bearing sources: steps, decision rules, examples, exercises,
pitfalls, checklists, or operating constraints. Drop sources that are only
motivation, history, shallow listicles, or vendor fluff unless they point to a
better source.

## Workflow

1. **Capture the local baseline.** Read the target `SKILL.md`,
   `qa_checklist.md`, `evals/evals.json`, examples, and recent audits. Name the
   generic behavior or missing domain strategy.
2. **Discover sources.** Search for `how to do <skill>`, current practitioner
   guides, and `best books on <domain>`. For platform-dependent skills, include
   official docs or current platform guidance.
3. **Score sources before extraction.** Label each `high`, `medium`, `low`, or
   `discovery_only` based on workflow signal and source confidence.
4. **Run book-to-skill for book inputs.** Load
   `skills/skill-creator/references/book-to-skill.md`. Use public summaries,
   author interviews, lectures, reviews, notes, or user-provided excerpts.
   Use `summarize` for YouTube/article extraction when available. Do not bypass
   paywalls or paste long expressive passages.
5. **Synthesize with best-of-worlds.** Use `best-of-worlds` to classify each
   candidate method as `adopt`, `adapt`, `reject`, or `defer` against the
   target skill's job.
6. **Patch the smallest owner-local surfaces.**
   - `SKILL.md` for every-invocation workflow moves, gates, routing, and output
     contract.
   - `qa_checklist.md` for reusable preflight/final review checks.
   - `evals/evals.json` for behavior regression cases.
   - `examples/*` for quality-dependent positive examples.
   - `references/*` for deeper formulas, source methods, or rare branches.
7. **Write the audit receipt.** Include source packet, decisions, skill delta,
   proof run, deferred sources, and residual risk.
8. **Validate and review.** Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
   Route material changes through `review` or a reviewer lane when available.

## Output Shape

```text
skill_source_upgrade_packet:
  target_skill:
  improvement_goal:
  local_baseline:
  sources:
    - title:
      url_or_ref:
      source_type: practitioner_article | official_doc | book_summary |
        author_interview | lecture | public_notes | user_notes
      source_confidence: high | medium | low
      workflow_signal: high | medium | low | discovery_only
      extraction_method: web_read | summarize | manual_from_supplied |
        discovery_only
      candidate_methods:
  book_to_skill_notes:
    - source_ref:
      takeaways:
      convergence: converged | single-source | conflicting | weak
      handling: adopt | adapt | reject | defer
  best_of_worlds:
    adopt:
    adapt:
    reject:
    defer:
  skill_delta:
    SKILL.md:
    qa_checklist.md:
    evals/evals.json:
    examples:
  proof_plan:
  residual_risk:
```

## Quality Gates

- Target baseline is named before research starts.
- Source budget is bounded and source confidence is labeled.
- Book, book-summary, author-interview, lecture, or public-notes inputs route
  through `book-to-skill` instead of becoming generic summaries.
- `best-of-worlds` decisions are recorded as `adopt`, `adapt`, `reject`, and
  `defer`.
- The applied delta changes skill behavior through a todo, gate, QA check,
  eval, example, reference, or output contract.
- Raw transcripts, long source wording, and book-substitute summaries stay out
  of durable skill files.
- `check_skills.py --write` passes, or the exact blocker is recorded.

## Upgrade Heuristics

- Prefer adding a decision gate over adding a list of tips.
- Prefer a named workflow object over vague quality language.
- Prefer a positive example or eval when the output quality depends on taste,
  persuasion, interpretation, or judgment.
- Treat current practitioner articles as recency signals and books as deeper
  method signals; neither source class automatically wins.
- Import the transferable mechanism, not the brand, author voice, examples, or
  long source wording.

## Bad Output

- A skill audit that says "researched best practices" without source links,
  source confidence, or adopt/adapt/reject decisions.
- A `SKILL.md` that contains a long reading list but no new action.
- A QA checklist that merely says "use best practices."
- An eval whose prompt leaks the exact framework name and only tests recall.
