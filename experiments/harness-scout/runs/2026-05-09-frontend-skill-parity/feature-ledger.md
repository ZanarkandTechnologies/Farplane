# Frontend Skill Feature Ledger

## Local Codexter Matches

| Capability | Local surface | Current strength | Current limit |
| --- | --- | --- | --- |
| Frontend lane routing | `skills/frontend-craft/SKILL.md`, `references/routing.md` | Clear separation between UX, visual taste, landing, implementation references, assets, and QA. | Does not yet force a compact pre-build "capability card" with stack/package/theme checks. |
| shadcn and registry guidance | `skills/frontend-design/SKILL.md`, `references/shadcn-setup.md`, `references/registries.md`, `references/theming.md` | Already covers shadcn, AI Elements, tweakcn, Aceternity, Animate UI, 8bitcn, RetroUI, ElevenLabs UI. | Small static registry list; misses current shadcn CLI `search/view/docs/apply/preset`, registry index, advanced namespaced auth, and richer app-domain registry categories. |
| Visual taste dials | `skills/visual-design/SKILL.md`, `references/taste-dials.md` | Codexter already has density, variance, motion, color, materiality, product/brand split, and anti-slop bans. | Less operational than taste-skill: no numeric dial output schema, no preflight matrix, no specific RSC/client isolation check, no style archetype library. |
| Functional UI states | `skills/functional-ui/SKILL.md`, `references/implementation-handoff.md` | Strong workflow/state handoff for default/loading/empty/error/success/disabled/max-content. | Could borrow state priority and component-state spec shape from external design-system source. |
| Landing spec-first workflow | `skills/landing-page/SKILL.md` | Much stronger than sources for premium/cinematic page planning, media evidence, product clarity, and QA. | Could borrow image-first section slicing and a "design bible" output for visual consistency across sections/screens. |
| External frontend delegation | `skills/delegate-frontend/SKILL.md` | Strong bounded phase model, artifact/handoff requirements, and rejection/downgrade rules. | Could require the delegate prompt to include a design-system/design-bible path and registry/theme plan before implementation. |
| Visual QA | `skills/visual-qa`, landing QA references | Strong artifact-first proof, screenshots, section checks, designer judgment. | Could add source-inspired checks for dynamic type, safe areas, small-phone landscape, touch targets, theme parity, and reduced-motion. |

## External Feature Candidates

| Candidate | Source evidence | Transferable principle | Local match |
| --- | --- | --- | --- |
| Searchable design intelligence | `ui-ux-pro-max` claims broad design rule categories and domain search workflow; `design-system` includes BM25 slide search scripts/data. | A skill can provide curated, queryable rule references instead of one giant prompt. | Codexter has reference files but no query script for frontend rules/registries/themes. |
| Mandatory design-system artifact | `ui-ux-pro-max` Step 2 requires a design system and Step 2b persists `design-system/MASTER.md` plus page overrides. | For substantial frontend work, persist a project-local design brief with master and page-specific overrides. | Codexter has visual briefs and landing specs, but app UI does not consistently write a durable `DESIGN.md` or design-system artifact. |
| Three-layer tokens | `design-system` uses primitive -> semantic -> component tokens and provides token validation scripts/templates. | Add token-layer guidance and optional validators to `frontend-design`. | Codexter mentions CSS variables/tweakcn but not a full token layer or validation pattern. |
| Component state/spec matrices | `design-system/references/states-and-variants.md` and `component-specs.md` define states, priority, variants, sizing, anatomy, and ARIA. | Use state/spec matrices for reused components and high-risk shared UI. | Codexter state coverage exists at UX level, but component-level state matrices are not a formal handoff shape. |
| Broad UI critical checklist | `ui-ux-pro-max` prioritizes accessibility, touch/interaction, performance, layout/responsive, typography/color, animation, forms, nav, charts. | Upgrade visual/QA preflight into a concise critical/high checklist. | Codexter has QA but can add more mechanical checks. |
| Current shadcn registry operations | Official shadcn docs support MCP browsing/search/install, registry index, namespaced registries, private auth, `search`, `view`, `docs`, `apply`, `preset`, `info`, and migrations. | `frontend-design` should teach agents to inspect/search/apply current registries and presets rather than rely on a static mini-list. | Local references include MCP init and a small registry table, but underuse current CLI surface. |
| Taste numeric dials | `taste-skill` uses design variance, motion intensity, and visual density as active variables. | Codexter's existing taste dials can gain numeric values and output schema without adopting absolute bans. | `visual-design` already has dials but no required numeric scoring. |
| Dependency and Tailwind version guard | `taste-skill` requires checking `package.json` before imports and Tailwind v3/v4 syntax. | Add a pre-build stack/package/theme check to `frontend-craft` and `frontend-design`. | Codexter says use repo patterns but lacks a frontend-specific mechanical package/Tailwind guard. |
| RSC/client isolation for motion | `taste-skill` isolates motion/liquid glass into client leaf components and avoids continuous React state for magnetic hover. | Add Next.js App Router/RSC motion isolation guidance to `motion-routing.md`. | Codexter has motion routing but can get more explicit on client boundaries and continuous animation state. |
| Anti-AI-tell content rules | `taste-skill` bans generic names, fake numbers, startup-slop names, filler phrases, broken Unsplash links. | Add content realism checks to visual and functional handoffs. | Codexter has demo-realism elsewhere and visual anti-slop, but frontend skills do not consistently require data/copy realism. |
| Image-first visual direction | `taste-skill` has web/mobile image-generation skills, section image counts, image consistency, and design-to-code extraction. | Strengthen landing asset planning and optionally add app-screen image/reference generation before complex builds. | Landing already plans assets; app UI lacks an image/reference loop except generic `imagegen`. |
| Design bible / Stitch output | `taste-skill/stitch-skill` emits a `DESIGN.md` with atmosphere, palette, typography, component styling, layout, motion, anti-patterns. | Create a Codexter-native `DESIGN_BRIEF.md`/section in ticket for substantial frontend builds. | Visual-design returns a visual brief, but the durable artifact convention is under-specified. |
| Style archetype packs | `taste-skill` has minimalist, brutalist, soft, brandkit, imagegen web/mobile modes. | Use archetypes as optional reference packs under `visual-design`, not separate public top-level skills. | Codexter visual-design is flexible but thin on concrete archetype recipes. |
| Brand/design asset workflow | `ui-ux-pro-max` has `brand`, `design`, `banner-design`, logo/icon/social photo/CIP skills with scripts/templates. | Useful as future non-app visual skill family; mostly out of current frontend-craft scope. | Codexter landing/media rules cover some; no dedicated brandkit/logo/icon skill. |

## Parity Brief

Capability + parity lens:

Improve Codexter frontend skills so agents can reliably produce richer, less generic, more current frontend work while keeping Codexter's artifact-first routing and QA discipline.

Comparable implementations:

- `ui-ux-pro-max`: broad UI rule corpus, searchable guidance claim, design-system/token assets, shadcn/Tailwind/ui-styling references.
- `taste-skill`: high-agency taste rules, numeric dials, image-first generation, preflight matrices, anti-generic content checks.
- Official shadcn docs: current registry/MCP/CLI mechanics.

Common surfaces:

- explicit design/taste variables before build,
- durable design-system/design-bible artifacts,
- component and state matrices,
- source/component registry lookup,
- mechanical package/theme/version checks,
- accessibility/responsive/motion preflight.

Repo delta:

Codexter already has better orchestration, landing gates, external delegation, and QA ownership. External sources dominate on concrete design-system persistence, searchable/checklist mechanics, image-first design direction, current shadcn registry operations, and taste preflight specificity.

Recommendation:

Do not use either external repo as the base. Keep Codexter's topology and adapt their strongest mechanics into `frontend-design`, `visual-design`, `frontend-craft`, `landing-page`, `delegate-frontend`, and `visual-qa`.
