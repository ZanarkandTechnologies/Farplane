---
title: SEO Content Advisor Initial Skill Audit
owner: seo-content-advisor
status: active
kind: skill-audit
created_at: 2026-07-09
ticket_id: TASK-0317
---

# SEO Content Advisor Initial Skill Audit

## Scope

Created the initial `seo-content-advisor` package for people-first SEO article
briefs, outlines, drafts, refresh plans, and QA verdicts.

## Source Grounding

- Google Search Central: helpful, reliable, people-first content.
- Ahrefs and Semrush 2026 guidance: on-page SEO, search intent, titles/meta,
  URLs, technical health, and AI-search-readable structure.
- Copywriting grounding is intentionally delegated to `copywriting-advisor`
  when article voice and product promise are fuzzy.

## Checklist Verdicts

- `first_load_sufficiency`: pass - `SKILL.md` includes trigger, signature,
  todo path, routes, gates, and outputs.
- `reference_load_precision`: pass - root QA and neighboring skills have
  explicit use conditions.
- `prompt_size_tokens`: pass - first load is compact and examples live outside
  `SKILL.md`.
- `proof_surface_fit`: pass - behavior-sensitive quality is guarded by
  `qa_checklist.md`, one example, and one eval smoke case.
- `human_gate`: pass - public publication and expert claims require human
  review.

## Proof Plan

Run `python3 skills/skill-maintenance/scripts/check_skills.py --write` and
`python3 -m json.tool skills/seo-content-advisor/eval_task.json`.
