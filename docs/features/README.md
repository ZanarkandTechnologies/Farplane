# Feature Registry

Farplane's feature registry is generated compatibility output. It preserves
stable `FEAT-*` handles for templates, tickets, sources, validators, and
adoption checks, but it is no longer the public product map.

The authored source of truth is the system stack:

```text
docs/systems/*.md
  -> docs/systems/registry.jsonl       # public system inventory
  -> docs/features/registry.jsonl      # internal capability inventory
```

Use [`docs/systems/README.md`](../systems/README.md) when deciding what
Farplane is made of. Use this folder when a tool needs a stable `FEAT-*`
capability handle.

## Record Shape

Each generated line in `registry.jsonl` is one JSON object:

```json
{
  "id": "FEAT-0064",
  "name": "Skill compounding score",
  "status": "implemented",
  "system_id": "SYS-0006",
  "system_name": "Skill System",
  "capability_role": "subcapability",
  "public": false,
  "category": "skills",
  "surfaces": ["docs/specs/skill-compounding-score.md"],
  "source_refs": ["docs/skills/system.md"],
  "external_refs": [],
  "evidence_refs": ["skills/taste-loop/SKILL.md"],
  "known_limits": "Prompt-consumed ranking contract; no standalone scorer yet.",
  "metrics": ["skill_compounding_score_traceability_pass"],
  "owner_spec": "docs/systems/skill-system.md",
  "last_verified": "2026-06-26"
}
```

## Field Contract

- `id`: stable `FEAT-####` identifier; never reuse an ID for a different
  capability.
- `name`: short, unique capability name.
- `status`: `implemented`, `partial`, `proposed`, `designed`, `deferred`, or
  `retired`.
- `system_id` / `system_name`: generated owner system.
- `capability_role`: `primary`, `subcapability`, `implementation_detail`,
  `retired_alias`, or `retired`.
- `public`: `true` only for primary system-facing capabilities. Most `FEAT-*`
  rows should stay internal.
- `category`: broad internal grouping such as `planning`, `proof`, `memory`,
  `source-ingestion`, `skills`, or `improvement-loop`.
- `surfaces`: repo paths that own the live behavior.
- `source_refs`: `SRC-*` records, local docs, tickets, memories, or specs that
  explain why the capability exists.
- `external_refs`: outside URLs, repos, videos, or standards that influenced the
  capability.
- `evidence_refs`: tickets, artifacts, commands, or experiment outputs that
  support the current status.
- `known_limits`: one concise caveat agents should preserve when comparing
  source ideas.
- `metrics`: metric names or scorecards associated with the capability. Leave
  empty when it is not benchmarked yet.
- `owner_spec`: generated path to the owning `docs/systems/*.md` file.
- `last_verified`: date when the record was checked against live surfaces.

## Update Rules

1. Add or update `capability_records_json` in the owning `docs/systems/*.md`
   file.
2. If no current system should own the capability, update the system stack
   before allocating another `FEAT-*` ID.
3. Keep raw transcripts, bulky summaries, and one-off logs in `experiments/` or
   ticket artifacts, not in capability records.
4. Link to ticket evidence instead of copying proof into the record.
5. Use `harness-scout` to dedupe source identity in
   `docs/sources/registry.jsonl` before creating new capability handles.
6. Run:

   ```bash
   python3 docs/features/validate_features.py --write
   python3 docs/features/validate_features.py
   ```

Do not hand-edit generated JSONL registries.

## ID Allocation

1. Read generated `id` values before adding a record.
2. Pick the next unused numeric ID in `FEAT-####` form.
3. Do not fill gaps without checking tickets and archived branches that may
   already reference the missing ID.
4. Do not rename or reuse an ID after another doc, ticket, scorecard, source
   run, or template references it.

## Skill-Applicable Capabilities

Use the same generated registry for capabilities that apply to Farplane skill
packages. Put skill-related records in
[`docs/systems/skill-system.md`](../systems/skill-system.md) unless another
system is the clearer owner.

Do not create a second hand-authored skill feature registry. The skill package
inventory already lives in generated form at `docs/skills/registry.jsonl`, and
versioned templates can keep referencing stable `FEAT-*` handles from this
registry.
