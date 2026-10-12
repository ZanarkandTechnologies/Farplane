# Agent Testability

Load this at Todo step 5 when the change touches UX or runtime an agent must
operate or prove: canvas, game, simulation, animation, realtime, media,
multi-client, or multi-job work, or any state QA cannot reach or see cheaply.
Folded from `agent-testability-plan` and proof-advisor's instrumentation guide
(#41). The output is change units and `QA Strategy` lines in the same ticket,
not a separate brief.

```text
agent_testability(change, system_class) -> friction_map + smallest_surfaces + proof_surfaces
```

## Friction map

Answer each only where it bites:

- **Reachability:** which states are too slow or flaky to reach by replaying
  the app by hand?
- **Hidden state:** which runtime facts are invisible from the UI or logs?
- **Coordination:** where do several jobs, workers, clients, or nested runs need
  one summary view?
- **Proof:** which claim cannot be asserted deterministically today?

## Smallest surfaces

| Bucket | Examples |
| --- | --- |
| Control accelerators | deep links to the screen or panel; seed, reset, pause, resume, step; seeded scenarios; camera presets; a debug route that jumps to the case |
| State probes | `data-testid` on every interactive and assertion target; selected object id and key properties mirrored as DOM text; a test-only state API (`window.__TEST__ = { getState, seed, reset }` or `/test/seed`) behind an env flag; debug overlay with bounding boxes and labels; current time, frame, or tick as text |
| Coordination views | run tree or job dashboard; failure summary; logs correlated by run id; for multiplayer, two browser contexts driven together, deterministic join-by-code, room and player ids in the DOM |
| Proof surfaces | event log or counters rendered in the DOM; serialized state snapshots; deterministic test mode (animations off, fixed RNG seed); golden frames within tolerance |

Bias by system class:

1. Canvas, game, simulation, animation: accelerators and probes first.
2. Distributed jobs, cloud, worker trees: coordination views plus correlated
   evidence.
3. CRUD, form, route apps: only the cheapest hooks (deep link, seed/reset,
   `data-testid`).
4. Already testable: say existing surfaces suffice; add nothing.

## Rules

- If an agent cannot reliably assert it, add instrumentation until it can, but
  plan only the smallest set the ticket's proof needs; record the rest as
  follow-up candidates.
- Each surface is a change unit with files and an assertion. Test-only hooks stay
  behind a dev/test flag and never ship enabled.
- Record reusable shortcuts, deep links, seeds, and hooks in the project's
  `AGENTS.md` Agent QA section (or `docs/qa/<flow>.md` for a long flow) so the
  in-app Browser and Playwright reuse one entry path.
- Do not redesign the architecture here; consume the settled design.
