---
title: "Initial Unslop adaptation"
status: active
owner: skill-maintenance
created_at: 2026-08-19
refs:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md
  - tickets/TASK-0440/ticket.md
---

# Initial adaptation

Adopted the upstream four-step idea: scan, rewrite, add appropriate human
voice, and self-audit. Kept concrete pattern classes such as puffery, filler,
vague attribution, generic prose, dense sentences, and needless jargon.

Changed for Farplane:

- made invocation explicit rather than “always apply” because the global prompt
  already owns the default voice;
- preserved exact meaning, certainty, Markdown, code, and technical terms;
- rejected punctuation bans, banned-word enforcement, forced opinions, and
  personality that does not fit the genre;
- added focused QA and runnable behavior evals.

`no_self_improve_reason:` the first version needs ordinary eval and review
proof before a measured optimization loop would be useful.
