# Feature Docs Instructions

This folder owns authored `FEAT-*` feature pages and generated feature
registry output.

Every surviving feature must have a readable `FEAT-*.md` page in this folder.
The generated registry reads plain YAML frontmatter fields such as
`feature_id`, `system_id`, `surfaces`, and `evidence_refs`; do not add a
duplicated `feature_record_json` block. If a capability is not worth a clear
page, delete the `FEAT-*` handle and remove active references to it.

Generated files:

- `docs/features/registry.jsonl`
- `docs/features/registry.md`

Rules:

- Do not hand-edit generated registry outputs.
- Keep system-level product layer prose in `docs/systems/*.md`.
- Keep feature-level problem, behavior, operating contract, surfaces, evidence,
  limits, and metrics in the owning feature page in this folder.
- Start from `docs/features/TEMPLATE.md` for new feature pages and keep the
  human explanation above implementation path lists.
- Keep raw transcripts, secrets, credentials, PII, or bulky proof out of
  feature docs; link to tickets or artifacts instead.
- Allocate the next unused `FEAT-####` ID only after reading current feature
  files and generated registry IDs.
- Add each surviving feature ID to exactly one system file's `feature_refs`.
- Run the registry generation and validation snippet in `README.md` after
  edits.
