# Feature Docs

Canonical feature specs live here once ideas move past exploration. Each
first-class Farplane capability should have one `FEAT-*.md` owner file with
frontmatter, behavior, surfaces, evidence, limits, and registry metadata.

Top-level companion docs:

- `ARCHITECTURE.md` - top-level system map and canonical surface guide
- `README.md` - product story and setup
- `docs/systems/README.md` - system/product grouping and boundaries

Current feature specs:

- add the live feature specs for this repo here

Use this folder for:

- product or system capabilities that deserve a stable `FEAT-*` handle
- API, data-contract, or workflow behavior owned by a feature
- evidence-backed decisions that should survive chat history and appear in the generated feature registry

Use `docs/systems/` for the larger product or system layer. System docs group
related feature specs and define boundaries; they do not replace feature specs.

## Doc Gardening Loop

When the public story changes:

1. Run the repo's structural validators.
2. Re-read `ARCHITECTURE.md`, `README.md`, and the changed feature specs.
3. Patch only the canonical surfaces that drifted.
4. Re-run the validators.
