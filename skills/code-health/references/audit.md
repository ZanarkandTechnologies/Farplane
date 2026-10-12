# Audit Mode

Load after `SKILL.md` selects `audit`. An audit ranks, inspects and tickets; it
does not rewrite. Implementation starts only when the operator picks a ticket.

## Bind

Name the codebase, PRD or spec refs, architecture refs, project rules, runtime
commands, ticket history, non-goals and budget (`smoke | focused | broad`,
ticket limit). When the request is really one known bug, one cleanup target or
one hardening target, switch to that mode instead.

## Rank components

Inventory product-critical workflows, entry points, modules, data boundaries,
dependencies, auth/secrets/config surfaces, tests, docs and scripts. Rank by:

- value: the operator loses the core result if it fails;
- centrality: many modules call, import or depend on its contract;
- blast radius: defects corrupt data, break auth, leak secrets or block work;
- churn: recent or frequent edits;
- plus complexity, security exposure, dependency risk, test weakness, and
  docs that describe a different boundary than the code.

```text
Component: name, paths, priority (critical|high|medium|low),
  audit_depth (architecture|focused-module|smoke-only|defer),
  evidence, confidence, why_before_others
```

Use `critical` only for the primary workflow, a security boundary, data
integrity or the task lifecycle. Prefer a short top wave over a full inventory
nobody acts on. When a component looks important but evidence is thin, record
an evidence gap rather than inflating confidence.

## Architecture before modules

Architecture pass: ownership boundaries, dependency direction, public
contracts against docs and callers, state flow through named boundaries, side
effects isolated at edges, observability of lifecycle failures, recovery from
partial failure, and a test strategy matched to the critical paths.

Module pass, in ranked order: one coherent job per module; size and nesting
justified by the domain; clear interfaces; stale shims, legacy names and dead
code supported by evidence.

## Route each finding once

| Route | When |
| --- | --- |
| `clean` | behaviour is known; shape slows future work |
| `harden` | abuse, failure, security or operational risk |
| `debug` | a concrete reproducible defect |
| `proof-advisor` | behaviour plausible, proof strategy unresolved |
| `document` | code fine, docs mislead |
| `delete` | evidence shows the surface is unused or duplicated |
| `split-ticket` | crosses independent proof or ownership boundaries |
| `no-action` | the smell is justified or not worth it now |

## Ticket spec

One ticket per coherent finding; group only findings that share a component,
proof route and owner. Keep broad waves as the audit artifact, not as tickets.

```text
Ticket: title, finding + evidence refs, scope_in, scope_out,
  owner (code-health mode | impl-plan | proof-advisor | doc-advisor),
  done_when, proof, residual_risk, next_action
```

When the audit context is only a README, return a smoke or discovery plan and
name the next files or commands that would raise confidence, not
implementation tickets.
