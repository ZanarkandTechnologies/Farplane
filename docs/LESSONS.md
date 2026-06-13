# Lessons

Append distilled lessons here after a trouble, repent pass, review failure, or
hardcase has been fixed or classified.

`docs/TROUBLES.md` is the raw pain-point log. This file is the smaller,
actionable learning log used to improve prompts, skills, policies, evals, and
review gates.

## When To Write Here

- `repent lesson` produced a reusable prevention rule after the fix.
- a `docs/TROUBLES.md` row recurred or revealed a stable prompt/skill gap.
- review or QA found a repeatable agent failure worth encoding.
- a hardcase should inform future evals, prompt guidance, or skill behavior.

## Format

```text
YYYY-MM-DD HH:mm Z | area,tags | source | lesson | owner | next_prompt_or_skill_change
```

## Promotion Rule

Promote durable rules from this file into `docs/MEMORY.md`, `AGENTS.md`, the
owning skill, a validator, or an eval only after the lesson is stable enough to
guide future work.

2026-06-07 19:17 +0800 | behavior-correction,evals,prompt-ownership | user correction after global AGENTS eval work | High-priority corrected misses should not stop at a lesson: after the same-scope fix lands, `eval` should capture a narrow regression eval in the owning project eval surface, and use `agent-qa-test` or `agent-behavior-test` when visible child-agent behavior needs proof. | skills/eval/SKILL.md | Keep behavior-correction cases flowing through `gap-analysis` / `optimize-harness` and project-level eval canaries.
2026-06-07 19:24 +0800 | communication,multitopic,global-agent | user correction during AGENTS/eval/hardcase work | In long multitopic threads, substantial replies should name the active topics or focus before answering so the agent does not silently drift between prompt, eval, and hardcase work. | templates/global/AGENTS.md | Add a communication rule plus a `.codex/evals` canary for multitopic focus.
2026-06-07 19:32 +0800 | communication,multitopic,thread-splitting | user clarification after topic-focus proposal | Long-thread replies should maintain a whole-thread topic ledger extracted from the conversation, not only the newest topic, and should suggest new-thread handoffs for independently executable or context-heavy tangents. | templates/global/AGENTS.md | Update the global communication rule, README/feature docs, and add a return-to-root-topic eval canary.
2026-06-07 19:32 +0800 | skill-maintenance,hardcase,validators | user correction after tier-check catch | Clear validator-detected skill todo contract violations should leave a deduplicated hardcase artifact so the failure can feed eval or self-improvement follow-up instead of vanishing after the local fix. | bin/validators/check_skill_todo_tiers.py | Add `--hardcase-on-failure`, wire it into skill-maintenance, and add a `.codex/evals` canary.
2026-06-07 22:33 +0800 | demo-realism,source-provenance,public-data | user correction after a blueprint QA prototype used a synthetic blueprint despite public artifacts being acceptable | Demo realism collapses when source-critical artifacts are invented while public, user-provided, or local real artifacts are available. Synthetic fixtures may be useful for mechanics, but they must be labeled as fallback and cannot prove real-world demo credibility. | skills/demo-realism/SKILL.md | Add a source-artifact ladder, provenance output, and rubric gate that prefers real public/user-provided/local artifacts before synthetic fallback.
2026-06-12 22:31 +0800 | learning-docs,notion,hooks | related trouble 2026-06-12 learning-docs Notion correction | The every-N-turn learning reviewer is the canonical local docs writer: it should review bounded windows, dedupe, pair resolved trouble->lesson, append compact rows, and return no_change without invoking Notion or optimize-harness. | skill-opportunity-applier role / Stop-hook learning reviewer | Keep weekly drain as the later optimize-harness escalation layer; keep live learning writes restricted to docs/TROUBLES.md and docs/LESSONS.md.
2026-06-13 11:16 +0800 | docs,harness-algebra,conceptual-framing | related trouble 2026-06-13 harness-algebra operator-card correction | When rewriting conceptual harness docs, first lock the intended reader journey and preserve the core formulas, lever taxonomy, and system-specific background; only then prune, reorder, or move advanced applied operators such as `optimize-harness`. | docs/fundamentals/harness-algebra.md | Add a pre-edit framing check for course/reference docs: teaching goal, required levers, preserved DNA, applied-operator placement, and proof commands.
2026-06-13 12:10 +0800 | docs,doc-quality,skills | related trouble 2026-06-13 doc-quality harness-algebra correction | Documentation edits should end with a focused doc-quality pass: remove agent-facing commentary, standardize terms and symbols, eliminate duplicate definitions, delete stale sections, and verify examples match the current model. | skills/documentation/SKILL.md | Keep `documentation:doc-quality` as a Tier 2 method and run targeted `rg` checks on revised docs before claiming completion.
2026-06-13 14:03 +0800 | goals,portfolio,heartbeat | related trouble 2026-06-13 goal-surface confusion | Goal architecture should optimize around timeboxed durable execution: tickets define proof, Goals execute the current leaf or batch, heartbeats resume parent portfolios, subagents provide parallelism, and GoalContextRefs should point to child ticket/program/progress files instead of flattening requirements. | skills/goal-advisor/SKILL.md | Add GoalContextRefs/child packet arrays plus Work/Ralph/Batch standards to goal-advisor templates before deprecating public helper skills.
2026-06-13 15:10 +0800 | skills,checklists,progressive-load | related trouble 2026-06-13 skill checklist placement correction | Skill structure QA should split principle from procedure: shared docs state the placement rule, while the owning skill keeps the runnable checklist, per-item review prompt, and subagent handoff as lazy `references/` material. | skills/skill-maintenance/references/skill-structure-checklist.md | Make skill-creator and skill-maintenance load the checklist only at finish/review time and report pass/violation evidence per changed file.
2026-06-13 17:29 +0800 | subagents,deliberative-advice,context | related trouble 2026-06-13 thin council prompts | Council mode and other nontrivial subagent handoffs should create or identify a durable Context Packet, then give each lane the same context_ref plus narrow role/focus/output shape so independent advice stays grounded without ticket clutter. | skills/deliberative-advice/SKILL.md and templates/global/AGENTS.md | Keep Council Context Packet examples/evals in deliberative-advice and use optional ticket binding only when the task already has ticket state.
