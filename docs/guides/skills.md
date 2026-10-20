---
title: Skills
status: active
owner: harness
created_at: 2026-10-16
updated_at: 2026-10-16
refs:
  - config/skill-workflows.toml
  - skills/registry.jsonl
  - skills/harness/SKILL.md
  - skills/harness/references/skill-system/README.md
  - skills/harness/templates/SKILL_TEMPLATE.md
tags:
  - farplane
  - skills
---

# Skills

How Farplane's skills are organized, installed, called, and kept honest. This
guide explains the system; it does not list every skill (run the commands
below for the current set) and it does not repeat the authoring rules, which
live in the `harness` skill.

## What a skill is

A skill is one folder under `skills/<name>/` that turns a request into one
deliverable: a plan, a report, an image, a verdict. The folder holds:

```text
skills/<name>/
  SKILL.md        # when to use it, its signature, and a checklist of steps
  references/     # detail loaded only when a step needs it
  templates/      # files the skill fills in
  scripts/        # deterministic helpers it runs
  evals/          # test cases that prove its behavior
```

Everything a skill needs to do its job lives inside its folder. Installed
skills run in other projects where this repo's `docs/` does not exist, so a
skill never depends on a path into `docs/` ([Doc Or Skill](../AGENTS.md#doc-or-skill)).

Project-specific workflows that are not reusable live in the project's
`.agents/skills/<name>/` instead, and move to `skills/` only after repeated
cross-project use.

## How skills are organized

Skills are grouped by business unit, one skill per deliverable a unit hands
out (the Capability Map). Six departments hold specialist desks; each desk has
a primary skill, its default verb:

| Department | What its desks deliver |
| --- | --- |
| leadership | business reviews, Goal architecture, progress reports |
| sales | prospect research, outreach, proposals and pricing |
| intelligence | research, video intelligence, feed scouting, bookmarks, the Wiki |
| marketing | storyboards, social posts, copy, landing pages, images, video, ads, 3D |
| delivery | PRDs, UI design, plans, code health, QA, review, docs, setup |
| operations | automations, the harness itself, evals, dispatch, usage |

A few skills sit on no desk because every desk uses them: thinking aids
(`advise`, `brainstorm`, `problem-framing`, `feasible-roadmap`, `lean-check`,
`recap-task`), writing and drawing aids (`unslop`,
`diagramming`), and workspace tools (`commit`, `pm`).

To see the current map:

```bash
farplane desk --list          # every desk and its skills
farplane desk <desk>          # launch Codex or Claude as one desk, with only its skills
```

`config/skill-workflows.toml` owns the map; `skills/registry.jsonl` is the
generated inventory of every skill (never hand-edited).

## How a skill runs

1. **Triggering.** Each skill's description leads with the phrases an operator
   would say ("plan this change", "is it ready"), so the runtime picks the
   right one from the request.
2. **The checklist.** `SKILL.md` carries a Todo List of 3–7 steps. Each step
   has a rule (the non-obvious decision) and assertions (what must be true
   before moving on). The agent works through the steps and checks its own
   assertions as it goes.
3. **Loading detail.** A step names the reference it needs; the agent opens it
   only then, so first load stays small.
4. **Calling other skills.** A skill calls another by name and input, never by
   path. For example, a skill whose output needs judging ends with: run
   `review` with family `implementation-plan` until it returns TAS-A, at most
   three rounds, otherwise stop with the open checks as the blocker. `review`
   finds its rubric inside its own folder.

## How skills prove their work

- **Assertions** in each checklist step catch mistakes while the skill runs.
- **A review gate** closes skills whose output has a matching review family
  (the template's optional last step, above). Self-review never counts.
- **QA** proves anything a user sees or operates (`qa`), and `outbound-check`
  grades anything outsiders receive.
- **Evals** (`evals/evals.json`) are test prompts with expected behavior. The
  `eval` skill runs them and compares a skill against having no skill or its
  previous version.

## Installing

`bash install.sh` (Codex) or `bash install.sh --runtime claude` links each
skill into `~/.codex/skills/` or `~/.claude/skills/` as a symlink, so edits in
this repo are live without reinstalling. Rerun the install only after adding or
removing a skill. A skill that keeps fixture skills under `tests/` (today
`eval` and `harness`) is copied instead, so reinstall after editing it.

## Making and changing skills

The `harness` skill owns this work, in four modes:

| Mode | Use when |
| --- | --- |
| `create` | a new, stable, reusable request has no owner |
| `maintain` | an existing skill needs a fix, an upgrade, or compaction |
| `optimize` | a measurable gap needs several bounded improvement rounds |
| `place` | it is unclear whether a rule belongs in a skill, a doc, a validator, or the global prompt |

New skills start from the [skill template](../../skills/harness/templates/SKILL_TEMPLATE.md);
the rules for structure, length (200 lines for `SKILL.md`), descriptions, and
references are in the [skill-system references](../../skills/harness/references/skill-system/README.md).
After any change, `python3 skills/harness/scripts/check_skills.py --write`
validates every skill and regenerates the registry.
