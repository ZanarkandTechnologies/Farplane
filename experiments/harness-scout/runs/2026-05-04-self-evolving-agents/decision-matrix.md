# Decision Matrix

| Feature | Source anchor | Source evidence | Local match | Scores | Decision | Reason | Ticket action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Program-driven autoresearch loop | `00:59-02:15` | Program file, eval, baseline, keep/discard | `FEAT-0005` | value 5, evidence 4, fit 5, novelty 1, cost 5, risk 5, benchmark 5 | `already-dominating` | Codexter already has artifact-backed autoresearch. | none |
| Skill-specific eval improvement | `00:59-02:15`, `10:54-12:47` | Self-evolving harness and skills | `FEAT-0006` | value 5, evidence 4, fit 5, novelty 1, cost 5, risk 5, benchmark 5 | `already-dominating` | Codexter's `self-improve` is more explicit about binary evals and run memory. | none |
| Hot/warm memory split | `04:30-08:52`, `12:49-14:59` | Always-loaded memory index plus on-demand memory | `FEAT-0001`, `FEAT-0007` | value 4, evidence 4, fit 4, novelty 2, cost 4, risk 4, benchmark 3 | `hybrid` | Codexter has progressive disclosure through maps, docs, tickets, and skills, but not branded as hot/warm memory. | no ticket; registry covers current shape |
| Async memory consolidation | `07:57-08:52` | Background review updates memory after sessions | partial closeout/docs writeback | value 4, evidence 3, fit 3, novelty 4, cost 2, risk 2, benchmark 2 | `defer` | Useful principle, but autonomous memory mutation risks stale hidden state and needs separate design. | possible future research ticket |
| Searchable raw conversation history | `09:11-10:18`, `13:17-14:59` | SQLite/raw history search | transcript is disposable by policy | value 3, evidence 3, fit 1, novelty 4, cost 2, risk 1, benchmark 2 | `reject` | Codexter intentionally makes tickets/docs canonical instead of transcript history. | none |
| Autonomous skill generation after N steps | `10:54-12:47` | Background skill reviewer and skill manager | `skills/skill-creator`, `skills/self-improve` | value 4, evidence 3, fit 3, novelty 4, cost 2, risk 2, benchmark 3 | `adapt` | Good idea as a gated skill-opportunity reviewer; unsafe as auto-write/autopublish. | `TASK-0104` |
| Skill safety scan | `12:17-12:38` | Skill guard rejects unsafe generated skills | `quick_validate`, review gates | value 4, evidence 3, fit 4, novelty 3, cost 3, risk 4, benchmark 4 | `adapt` | Worth pairing with any future autonomous skill proposal loop. | `TASK-0104` |
| Hook-driven learning reminders | `15:21-16:24` | Prompt submit and post-tool hooks nudge learning updates | `hooks.json`, `capture_user_turn`, `stop_hook` | value 3, evidence 3, fit 3, novelty 3, cost 3, risk 2, benchmark 3 | `needs-benchmark` | Could help, but hook spam and context pollution are real risks. | `TASK-0105` |
| Error/learnings folder | `15:21-16:24` | Separate learnings/errors/feature requests | `docs/TROUBLES.md`, `docs/MEMORY.md` | value 4, evidence 4, fit 5, novelty 2, cost 4, risk 4, benchmark 3 | `hybrid` | Codexter already has curated durable memory; source reinforces current pattern. | none |
| Strict memory caps | `12:49-13:42` | Small hot memory files | concise maps; no hard cap validator | value 3, evidence 3, fit 4, novelty 3, cost 3, risk 4, benchmark 3 | `defer` | Could reduce prompt bloat, but no repeated current failure justifies a validator yet. | none |
| Semantic memory layer | `13:17-14:59` | Optional semantic DB | none active | value 2, evidence 2, fit 1, novelty 4, cost 1, risk 1, benchmark 1 | `reject` | Too heavy for the current high-ROI source-scout workflow. | none |
| Deterministic versus agentic architecture choice | `03:12-04:30` | Do not make every workflow fully agentic | `FEAT-0009`, `MEM-0074` | value 5, evidence 4, fit 5, novelty 1, cost 5, risk 5, benchmark 4 | `already-dominating` | Codexter's serial Ralph and explicit future boundary already embody this. | none |

## Dominance Summary

- `Codexter dominates:` autoresearch, skill self-improvement, ticket memory,
  conservative autonomy boundaries, source synthesis.
- `Source dominates:` autonomous skill/memory review loops, if judged only by
  automation level.
- `Hybrid wins:` hot/warm memory framing, error/learnings structure, hook-based
  reminders.
- `Reject/defer:` raw conversation search, semantic memory, async consolidation
  until there is a focused ticket and metric.
