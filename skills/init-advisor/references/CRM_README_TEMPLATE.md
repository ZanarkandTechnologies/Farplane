# CRM

Ignored local customer and relationship research state for this project.

Use this directory for customer research reports produced before calls. These
reports may include private notes, sourced public facts, and operator judgment,
so they stay under `.farplane/` by default.

## Layout

```text
.farplane/crm/
  README.md
  reports/
    YYYY-MM-DD-person-name.md
  index.jsonl
```

`reports/*.md` are the source of truth. `index.jsonl` is derived from report
frontmatter and can be rebuilt.

## Report Frontmatter

Keep frontmatter minimal:

```yaml
---
skill: "customer-research"
name: "Person Name"
links:
  - "https://example.com/profile"
industry: "Industry or field, when useful for search."
relevance: "Why this person is relevant to the call or project."
created_at: "YYYY-MM-DD"
---
```

`skill` names the report-producing skill so other report workflows can share
the same index and still be filtered by source. `industry` is optional. Link a
report to its owning ticket or capability skill when additional provenance is
needed; do not introduce a product-catalog foreign key.

Put role, story, field overview, pain hypotheses, conversation questions,
confidence, unknowns, and next actions in the report body.
