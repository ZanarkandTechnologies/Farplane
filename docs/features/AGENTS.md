# Feature Docs Instructions

This folder owns authored `FEAT-*` feature pages and generated feature
registry output.

Every surviving feature must have a `FEAT-*.md` page in this folder with a
`feature_record_json` block. If a capability is not worth that page, delete
the `FEAT-*` handle and remove active references to it.

Generated files:

- `docs/features/registry.jsonl`
- `docs/features/registry.md`

Rules:

- Do not hand-edit generated registry outputs.
- Keep system-level product layer prose in `docs/systems/*.md`.
- Keep feature-level behavior, surfaces, evidence, limits, and metrics in the
  owning feature page in this folder.
- Keep raw transcripts, secrets, credentials, PII, or bulky proof out of
  feature docs; link to tickets or artifacts instead.
- Allocate the next unused `FEAT-####` ID only after reading current feature
  files and generated registry IDs.
- Add each surviving feature ID to exactly one system file's `feature_refs`.
- Run the registry generation and validation snippet in `README.md` after
  edits.
