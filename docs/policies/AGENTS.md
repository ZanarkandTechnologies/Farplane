# Policy Docs

This folder is a navigation and consistency layer for Farplane policy.

Do not move canonical policy ownership here by default. Durable rules still
belong in `docs/MEMORY.md`, active agent routing belongs in `AGENTS.md` and
`templates/global/AGENTS.md`, procedural rules belong in the owning skill, and
system contracts belong in `docs/specs/*`.

Keep policy pages link-heavy and duplication-light. A policy entry should say
what the rule is for, where the canonical owner lives, and how to verify drift.
