# UI Review

Load from `review` (or `clean`) mode when the target touches UI source, React,
Next.js, or client data fetching. It holds two source-level lanes. Rendered
screenshots and layout geometry belong to `qa` visual mode; dashboard clarity
belongs to `review-dashboard`; a TAS verdict belongs to `review`.

## Web Interface Guidelines lane

Use for accessibility, focus, forms, navigation, animation, responsive
behaviour, content semantics, and interface basics.

1. Fetch the current rules before judging. Do not rely on memory and do not
   copy the rule list into Farplane:
   `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
2. Read the changed UI files from the diff or ticket. Ask for a pattern only
   when no target was supplied.
3. Report terse `file:line` findings with severity and the correction, in the
   format the fetched command specifies. State `Grounding:` with the fetch.
4. Keep raw findings separate from any TAS. `review` converts them into the
   `frontend-guidelines` verdict
   ([rubric](../../../docs/review/rubrics/frontend-guidelines.md)).

A clean guideline audit does not prove the UI is useful or tasteful, and a
screenshot does not replace the source-level check.

## React and Next.js performance lane

Vercel's React best-practice rules (upstream
`https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices`,
version 0.1.0) live in [react-rules/](react-rules/). Read
[the section index](react-rules/_sections.md), then only the rule files whose
prefix matches the touched code. Each rule has an incorrect and a correct
example.

| Priority | Category | Impact | Prefix |
| --- | --- | --- | --- |
| 1 | Eliminating waterfalls | critical | `async-` |
| 2 | Bundle size | critical | `bundle-` |
| 3 | Server-side performance | high | `server-` |
| 4 | Client-side data fetching | medium-high | `client-` |
| 5 | Re-render optimisation | medium | `rerender-` |
| 6 | Rendering performance | medium | `rendering-` |
| 7 | JavaScript performance | low-medium | `js-` |
| 8 | Advanced patterns | low | `advanced-` |

Example: a page awaits three independent fetches in sequence ->
[async-parallel](react-rules/async-parallel.md) -> one critical finding with the
`Promise.all()` fix. Project module boundaries still decide where code lives.

## Convex repositories

For a repo with Convex backend files, read the project's installed Convex AI
instructions first (`npx convex ai-files install` refreshes them), else the
official upstream skill at
`https://github.com/get-convex/agent-skills/blob/main/skills/convex/SKILL.md`.
Farplane keeps no parallel Convex playbook.
