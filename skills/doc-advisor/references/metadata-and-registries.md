---
template_uses:
  skill-method-reference: "0.1.0"
---

# Metadata And Registries

Use this reference when documentation edits touch front matter, feature refs,
system refs, template metadata, generated registries, or validation commands.

```text
metadata_and_registries(doc_delta, target_file) -> metadata_delta + validation_plan
state: reads(target frontmatter, nearest registry README, feature/system/template docs); writes(target frontmatter?, generated registry via validators)
gates: schema_preserved; generated_outputs_not_hand_edited; validators_named
fails: invents version fields; edits JSONL registry rows by hand
```

## Use When

- Adding or changing YAML front matter.
- Editing `docs/features/*`, `docs/systems/*`, `docs/templates/*`, or skill
  template metadata.
- References, status, owner, feature IDs, system IDs, source refs, or registry
  rows may change.

## Inputs

```text
input_packet:
  required:
    target_file:
    metadata_reason:
  optional:
    feature_id:
    system_id:
    template_id:
  source_refs:
    - docs/features/README.md
    - docs/features/TEMPLATE.md
    - docs/systems/README.md
```

## Workflow

1. **Preserve local schema.** Update existing schema fields; do not invent a
   universal metadata model for ordinary docs.
2. **Update source docs first.** Feature pages and system pages are sources;
   generated JSONL and registry Markdown are outputs.
3. **Run the right generator.**
   - Feature/system metadata: `python3 docs/features/validate_features.py --write`
   - Skill metadata or links: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
   - General doc refs: `python3 bin/validators/check_doc_refs.py`
4. **Report generated output.** Summaries should name source docs changed and
   validators run, not pretend generated rows were hand-authored.

## Output Shape

```text
metadata_result:
  source_files:
  generated_files:
  validators:
  deferrals:
```

## Quality Gates

- Generated registries are not hand-edited.
- Metadata changes match owner schemas and do not expose secrets or bulky prose.
- Validation output is recorded or explicitly deferred.

## Bad Output

- Adding `last_edited` or `health_score` fields because they feel useful.
- Fixing registry drift by directly editing `registry.jsonl`.
