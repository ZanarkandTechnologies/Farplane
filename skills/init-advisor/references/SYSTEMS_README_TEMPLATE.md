# Systems

System docs describe the product or system layer above individual feature
specs. Use this directory when deciding what the project is made of, where
boundaries sit, and which first-class features belong together.

```text
docs/systems/*.md
  -> system/product grouping and boundaries
  -> related docs/features/FEAT-*.md specs
```

Use `docs/features/` when a capability deserves its own `FEAT-*` feature spec,
owner surfaces, evidence, limits, and metadata. Use `docs/systems/` when a set
of capabilities needs a stable product/module boundary.

Current systems:

- add the live systems for this repo here

## System Doc Shape

For each durable system, create one Markdown owner file that names:

- system name and purpose
- primary feature or feature set
- product/module boundary
- what belongs here
- what belongs elsewhere
- links to related `docs/features/FEAT-*.md` specs

## Doc Gardening Loop

When a system boundary changes:

1. Update the owning system doc.
2. Update or create the related feature specs in `docs/features/`.
3. Regenerate any project-owned registries or indexes.
4. Re-run the repo's structural validators.
