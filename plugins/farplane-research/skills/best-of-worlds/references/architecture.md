# Best Of Worlds Architecture

`best-of-worlds` sits between external research and implementation.

It does not replace:

- [research:parity](../../research/SKILL.md#researchparity): use for broad
  category parity before a synthesis target is known.
- [research:gap](../../research/SKILL.md#researchgap): use for repo-local
  current state versus production expectation.
- [research:source-synthesis](../../research/SKILL.md#researchsource-synthesis):
  use for compact source normalization before a full best-of-worlds pass.
- `advise`: use for judgement calls when the metric or adoption decision is not
  mechanical.
- `impl-plan`: use after the best-of-worlds decision becomes a concrete ticket
  plan.

The skill owns the synthesis contract:

1. source inventory
2. feature extraction
3. metric discovery
4. adopt/adapt/reject/defer decision matrix
5. implementation handoff

## Source Quality Order

Prefer:

1. maintained repos and real code paths
2. official docs or standards
3. detailed implementation writeups with concrete artifacts
4. product screenshots or marketing claims only as weak signals

## Decision Boundary

The winning design should be a coherent local workflow. It should not be an
unfiltered bundle of source features.

## Stable Skill Import Rule

For Farplane skills, external implementations are research inputs, not live
dependencies. Do not auto-sync external skill behavior and do not copy upstream
command families wholesale. Import only the reviewed ideas that earn an
`adopt`, `adapt`, `reject`, or `defer` decision. See `MEM-0073`.
