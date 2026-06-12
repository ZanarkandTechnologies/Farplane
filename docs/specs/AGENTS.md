# `docs/specs/AGENTS.md`

Rules for canonical spec documents.

## Purpose

Files here define buildable system behavior, schemas, and flows.

## Keep Specs

- canonical
- concise
- diagram-first for material flow or architecture changes; see `MEM-0030`
- specific about data flow and responsibilities
- one file per current harness feature, contract, or doctrine surface; see
  `MEM-0135`

## Do Not

- duplicate exploratory research
- mix settled specs with open-ended comparison notes
- keep completed migration plans, superseded milestone notes, or skill-owned
  workflow contracts as active specs
- bury executable contracts in long prose when diagrams or examples would be clearer
- do not split simple delta views into separate before/after diagrams when one legend-backed diagram would be clearer

## Required Maintenance

- update `README.md` when adding new canonical spec files
- update `docs/HISTORY.md` when specs materially change the target system shape
- run `python3 bin/validators/check_doc_parity.py` when changing canonical README/spec/ticket docs that define the current public harness story
