# `skills/farplane-invocation/AGENTS.md`

Rules for the Farplane invocation skill.

## Purpose

This skill teaches normal Codex sessions how to honor a Farplane run envelope.
Farplane remains Codex plus installed repo skills, hooks, templates, and proof
conventions.

## Keep

- one work item per envelope
- filesystem tickets as the v1 adapter
- helper commands diagnostic and artifact-writing only
- existing phase skills as the actual execution owners
- proof packets parseable without transcript access

## Do Not

- introduce a public `farplane run` product
- launch Codex from this skill or from `bin/farplane_invocation.py`
- add polling, leases, cloud execution, or remote board adapters here
- duplicate the detailed contracts for `impl-plan`, `$impl`, `qa`, `review`, or
  `close-ticket`
