---
title: Initial customer-research skill audit
owner: customer-research
status: complete
created_at: 2026-07-07
---

# Initial Customer Research Skill Audit

## Change

Created `customer-research` as a Tier 3 call-prep skill for sourced person and
field research, conversation planning, and minimal CRM indexing.

## Checklist Verdicts

- `skill-creator qa`: pass. The skill has a stable reusable trigger, first-load
  contract, template, example, eval task, and proof command.
- `skill-maintenance structure`: pass. Normal path is executable from
  `SKILL.md`; optional script and template are precisely referenced.
- `frontmatter minimality`: pass. Report frontmatter is only `skill`, `name`,
  `links`, optional `industry`, optional `farplane_product_id`, `relevance`,
  and `created_at`.
- `project-specific isolation`: pass. Skill defines generic CRM roots and does
  not embed one customer's private context.

## Proof

Run:

```bash
tmpdir="$(mktemp -d)"
mkdir -p "$tmpdir/reports"
cp skills/customer-research/examples/first-call/example.md "$tmpdir/reports/maya-tan.md"
python3 skills/customer-research/scripts/sync_crm_frontmatter.py "$tmpdir"
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

The first command should write one JSONL row from the example fixture. The
second command should refresh skill metadata and report no blocking structure
errors.
