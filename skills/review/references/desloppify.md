# Desloppify

Use this cross-cutting reference when review needs to behave like a skeptical,
repository-grounded anti-slop pass rather than a changed-file skim.

This is not a separate public review skill and not a separate scored rubric
family. It is the search-and-challenge playbook that sits on top of the scored
families, especially `code-quality`, `integration-readiness`,
`evidence-quality`, and `debloatability`.

## Purpose

Turn review into an inconsistency hunter:

- search beyond the changed file when the claim obviously touches neighboring
  surfaces
- challenge confident prose against actual repo evidence
- catch drift, dead weight, duplicate policy, and weak integration assumptions
- return high-signal findings with severity, confidence, and file references

## Search Scope Ladder

Start at the changed surface, then widen only as needed:

1. changed files and ticket claims
2. directly imported/exported neighbors
3. constants, schemas, types, or config surfaces that define the same rule
4. docs, specs, or memory entries that claim the same invariant
5. nearby tests, fixtures, or evidence artifacts that should prove the claim

Stop widening when you can explain why the work is coherent or where the real
defect lives. Do not search the whole repo without a concrete reason.

## High-Signal Slop Patterns

Prioritize these over style commentary:

- `invariant drift`: code, docs, or ticket claims disagree about the same rule
- `naming drift`: renamed behavior or fields were not propagated to related surfaces
- `contract drift`: schema/type/interface assumptions changed in one place only
- `claim inflation`: prose or comments promise more than the proof actually shows
- `dead compatibility`: old fallback paths or wrappers remain after the new path landed
- `copy-shift bugs`: duplicated logic was patched in one location but not its siblings
- `test theater`: a test exists, but it does not actually cover the claimed behavior
- `hidden coupling`: the changed file looks isolated, but a nearby caller or invariant now breaks
- `stale docs`: canonical docs still teach the old behavior
- `debug residue`: TODOs, logs, dead flags, or half-removed escape hatches remain

## Core Questions

Ask these before scoring:

- Which neighboring surface is most likely to disagree with this change?
- What claim sounds true in the summary but is not actually proven?
- What would a skeptical human reviewer search next?
- What stale compatibility layer or duplicate policy is still hanging around?
- If this change were copied from another file, where is the sibling bug likely to remain?
- What exact file or invariant would I cite if I had to defend rejection?

## Finding Priority

Use severity for substance, not theatrics:

- `critical`: unsafe, contradictory, or likely to break production/runtime correctness immediately
- `high`: materially blocks trust, merge readiness, or core correctness
- `medium`: real weakness that should be fixed before pass, but with lower blast radius
- `low`: useful improvement, polish, or cleanup that does not decide the verdict alone

Use confidence to separate proof from suspicion:

- `high`: directly supported by the code/evidence/docs you inspected
- `medium`: likely and grounded, but still partly inferential
- `low`: plausible concern to verify, not yet a defended finding

Default rule: only `high` and `critical` findings should normally appear in
`blocking_findings`, unless a cluster of `medium` issues collectively prevents
trust.

## Output Contract

When this playbook is used, return:

- `search_scope`
- `finding_log`

`search_scope` should list the changed files plus the specific related surfaces
you checked. Keep it compact.

`finding_log` entries should include:

- `severity`
- `confidence`
- `rubric`
- `summary`
- `file_refs`
- `evidence`
- `next_action`

## Anti-Patterns

- Treating the changed file as self-sufficient when the same rule clearly lives elsewhere
- Reporting only style nits while missing contract or invariant drift
- Using vague phrases like "may be inconsistent" without naming the conflicting surface
- Converting every mild concern into a blocking finding
- Searching the entire repo without a hypothesis
