# Tech Impl Plan Examples

## Good

````md
## Pitch
- Req: simplify plan output so approval is faster
- Bet: make pseudocode default; move deep detail to appendix
- Win: human sees intent + delta in seconds

## B -> A
- Before: long plan, repeated sections, high scroll cost
- After: pitch-first plan with compact top section
- Outcome: faster yes/no, less token waste

## Delta
- Touch: skill, prompt, template, examples
- Keep: split rule, proof discipline
- Change: section order, wording style
- Delete/Avoid: mandatory long dry-run and default diagram

## Core Flow
```pseudo
read context
if multi_commit: stop + split
pitch req back
show before -> after
show touched modules
show core pseudocode
show proof + ask
```

## Proof
- P1: low-risk plan readable from top section only
- P2: risky plan keeps details below fold
- Risk: over-compression
- Rollback: restore old template

## Plan Review
- Refs: prd, ticket, memory, local skill files
- Scope: pass, one commit stays inside skill docs/prompt/template
- Proof: pass, checks are observable in generated plan shape
- Guardrails: pass, reuses existing planning flow and adds no new moving parts
- Fixes: tightened proof wording and made the quality gate explicit

## Delegation
- Need: Not needed

## Ask
- Ready: yes
- Next: patch skill files
````

## Bad

```md
We should improve the planning system. Here is a long explanation of all the sections and all the possible future use cases...
```

Why bad:

- no sharp req understanding
- `Before -> After` buried or missing
- too much narrative before proof of value
- no compact approval surface
