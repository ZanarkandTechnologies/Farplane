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
2026-06-07 19:32 +0800 | skill-maintenance,hardcase,validators | user correction after tier-check catch | Clear validator-detected skill todo contract violations should leave a deduplicated hardcase artifact so the failure can feed eval or self-improvement follow-up instead of vanishing after the local fix. | bin/check_skill_todo_tiers.py | Add `--hardcase-on-failure`, wire it into skill-maintenance, and add a `.codex/evals` canary.
2026-06-07 22:33 +0800 | demo-realism,source-provenance,public-data | user correction after a blueprint QA prototype used a synthetic blueprint despite public artifacts being acceptable | Demo realism collapses when source-critical artifacts are invented while public, user-provided, or local real artifacts are available. Synthetic fixtures may be useful for mechanics, but they must be labeled as fallback and cannot prove real-world demo credibility. | skills/demo-realism/SKILL.md | Add a source-artifact ladder, provenance output, and rubric gate that prefers real public/user-provided/local artifacts before synthetic fallback.
