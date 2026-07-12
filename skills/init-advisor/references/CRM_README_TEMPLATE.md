# CRM

Ignored local customer and relationship state for this project.

Use this directory for a small entity ledger. Skill-produced reports live under
their producing skill, such as `.farplane/customer-research/reports/`, and link
back here with stable `entity_refs`.

## Layout

```text
.farplane/crm/
  README.md
  entities.json
```

`entities.json` is hand-authored relationship state. Keep it deliberately small:

```json
{
  "entities": [
    {
      "id": "jane-smith",
      "name": "Jane Smith",
      "description": "Founder of Acme and a prospective design partner.",
      "links": ["https://example.com/jane"],
      "status": "researching"
    }
  ]
}
```

## Report Links

Keep frontmatter minimal:

```yaml
---
skill: "customer-research"
entity_refs:
  - "jane-smith"
  - "acme"
name: "Person Name"
links:
  - "https://example.com/profile"
industry: "Industry or field, when useful for search."
relevance: "Why this person is relevant to the call or project."
created_at: "YYYY-MM-DD"
---
```

`entity_refs` values must resolve to IDs in `entities.json`. Do not hand-maintain
report arrays on CRM entities; discover backlinks by scanning
`.farplane/*/reports/**/*.md`. CRM has no report index. Any future derived
cross-skill report index must live outside CRM and be introduced through a
ticketed reporting change.

Put role, story, field overview, pain hypotheses, conversation questions,
confidence, unknowns, and next actions in the report body.
