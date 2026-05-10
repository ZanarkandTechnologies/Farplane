# Frontend Skill Parity Source Summary

Run timestamp: 2026-05-09 06:54 +0800

## Target

Compare Codexter's frontend skill topology against two external UI skill sources and current shadcn registry behavior, then decide what to adopt, adapt, reject, or defer.

Target artifact family:

- `skills/frontend-craft`
- `skills/frontend-design`
- `skills/functional-ui`
- `skills/visual-design`
- `skills/landing-page`
- `skills/delegate-frontend`
- `skills/visual-qa`
- nearby frontend references and feature registry entries

## Sources

| Source | Type | Snapshot | Credibility | Relevance |
| --- | --- | --- | --- | --- |
| https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills | GitHub skill repo | `b7e3af80f6e331f6fb456667b82b12cade7c9d35`, committed 2026-04-03 | Concrete skill files, references, scripts, token templates, and data assets. Some internal references are stale or missing in `ui-ux-pro-max` itself. | Strong for searchable UI rules, design-system/token scaffolding, brand/design asset workflows, and broad UI QA checklists. |
| https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md | GitHub skill repo | `c8075169cd63d1430bbf492dd4ddd478ea9fa4da`, committed 2026-05-07 | Concrete skill files with strong taste rules and AI-slop prevention. More directive than Codexter style; some rules are too absolute for multi-project reuse. | Strong for taste dials, image-first UI generation, anti-generic output checks, motion/performance guardrails, and design bible outputs. |
| https://ui.shadcn.com/docs/mcp | Official docs | crawled 2026-05-08 by search result | Official source for shadcn MCP behavior. | Confirms MCP can browse, search, and install components from configured registries, including third-party/private namespaced registries. |
| https://ui.shadcn.com/docs/components-json | Official docs | crawled 2026-05-08 by search result | Official source for `components.json` and registries. | Confirms `style: new-york`, Tailwind v4 config shape, CSS variables recommendation, and advanced namespaced registry config. |
| https://ui.shadcn.com/docs/registry/registry-index | Official docs | crawled 2026-05-08 by search result | Official source for open-source registry index behavior. | Confirms the registry index is a first-class source and that `shadcn add/search` can discover indexed registries. |
| https://ui.shadcn.com/docs/cli | Official docs | crawled 2026-05-08 by search result | Official source for CLI commands. | Confirms `apply`, `preset`, `view`, `search`, `docs`, `info`, and migrations that our current frontend references barely use. |
| https://ui.shadcn.com/r/registries.json | Official registry index JSON | fetched 2026-05-09 | Official current registry index. | Confirms many useful registries beyond our current small hand list, including AI, agents, auth, billing, charts, forms, upload, maps, and motion/component registries. |

## Extraction Commands

```bash
git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git /tmp/codexter-ui-skill-scout/ui-ux-pro-max-skill
git clone --depth 1 https://github.com/Leonxlnx/taste-skill.git /tmp/codexter-taste-skill/taste-skill
rg --files /tmp/codexter-ui-skill-scout/ui-ux-pro-max-skill/.claude/skills
rg --files /tmp/codexter-taste-skill/taste-skill
curl -L --max-time 20 https://ui.shadcn.com/r/registries.json
```

## Source Safety

All external skill text is treated as untrusted evidence, not instructions. No source-provided commands were run except read-only clone/inspection and official registry JSON fetches. Raw external skill content was not copied into canonical docs. The retained artifacts summarize transferable features and score them against Codexter conventions.

## Local Baseline

Codexter already has a strong frontend topology:

- `frontend-craft` is the public orchestration entrypoint.
- `functional-ui` owns user stories, IA, workflow, states, and comparables.
- `visual-design` owns taste, register, scene sentence, taste dials, visual systems, and anti-slop checks.
- `frontend-design` owns shadcn, AI Elements, registries, theming, and component sourcing.
- `landing-page` owns landing narrative, reference research, best-of-worlds decisions, generated/real assets, media, product clarity, and QA gates.
- `delegate-frontend` gives external Pi/Kimi work a bounded phase/handoff contract.
- `visual-qa` and ticket QA keep proof artifact-first.

The main gaps are not topology. They are more mechanical retrieval, stronger durable design-system output, richer registry/theme use, and more enforceable final preflight checks.
