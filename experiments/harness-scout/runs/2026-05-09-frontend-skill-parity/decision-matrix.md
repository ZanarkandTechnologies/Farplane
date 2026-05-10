# Frontend Skill Decision Matrix

Scores are `user-value/evidence-strength/local-fit/novelty/implementation-cost/risk-control/benchmarkability` on a 1-5 scale.

| Feature | Source anchor | Source evidence | Local match | Scores | Decision | Reason | Ticket action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Keep Codexter topology instead of replacing it | Local baseline vs both repos | Codexter already splits frontend orchestration, UX, visual, landing, implementation references, delegation, and QA; sources are broader or more monolithic. | `frontend-craft`, `functional-ui`, `visual-design`, `landing-page`, `frontend-design`, `delegate-frontend` | 5/5/5/2/5/5/5 | already-dominating | Codexter's topology is safer and more maintainable than importing a monolithic UI skill. | No replacement; adapt selected mechanics only. |
| Current shadcn registry/CLI upgrade | Official shadcn docs and registry JSON | MCP supports registry browsing/search/install; `components.json` supports registries/auth; CLI supports `apply`, `preset`, `view`, `search`, `docs`, `info`, migrations; registry index has many current registries. | `frontend-design/references/shadcn-setup.md`, `registries.md`, `theming.md` | 5/5/5/4/4/5/5 | adopt | This directly addresses the user's "more shadcn/tweakcn" concern and is official/current. | Update `frontend-design` refs with registry discovery, preset/theme apply, domain registry shortlist, and MCP/Codex config caveat. |
| Durable frontend design brief / design bible | `ui-ux-pro-max` persisted design system; `taste-skill/stitch-skill` `DESIGN.md` | External sources require master/page overrides or a semantic design system artifact. | `visual-design` output contract, tickets, landing specs | 5/4/5/4/4/5/4 | adapt | Codexter should persist a Codexter-native design brief for substantial app UI, not import their exact paths. | Add `DESIGN_BRIEF.md` template/reference and route from `visual-design`/`frontend-craft`; include master/page override pattern. |
| Three-layer token architecture | `ui-ux-pro-max/design-system` | Primitive -> semantic -> component token structure plus token validation scripts/templates. | `frontend-design/references/theming.md` | 4/4/4/4/4/4/4 | adapt | Token layering would make tweakcn/shadcn theming more rigorous, but exact scripts need local review. | Add token architecture reference; defer validator scripts unless a ticket needs them. |
| Component state/spec matrices | `ui-ux-pro-max/design-system` | States, state priority, component anatomy, variants, sizes, ARIA requirements. | `functional-ui` states, `frontend-design` component refs | 5/4/5/3/4/5/5 | adopt | Low-risk mechanical improvement for shared UI quality and handoffs. | Add component-state matrix template to `frontend-design` and require it for reusable/shared components. |
| Numeric taste dials | `taste-skill` | Design variance, motion intensity, visual density drive layout and motion choices. | `visual-design/references/taste-dials.md` | 4/5/5/3/5/4/4 | adapt | Codexter already has dials; numeric values make handoffs more enforceable without adopting absolute taste rules. | Update `visual-design` output contract to include 1-10 numeric dials plus rationale. |
| Frontend stack/package/Tailwind guard | `taste-skill` | Check `package.json` before imports; distinguish Tailwind v3/v4; isolate RSC client components. | General repo patterns, `frontend-craft`, `motion-routing.md` | 5/5/5/4/5/5/5 | adopt | High-value mechanical guard; prevents common broken builds. | Add pre-build "stack facts" step to `frontend-craft` and implementation references. |
| RSC/client motion isolation | `taste-skill` | Motion/liquid glass should be isolated into client leaf components; avoid continuous React state for cursor/motion physics. | `frontend-craft/references/motion-routing.md` | 5/5/5/3/5/5/4 | adopt | Fits Next.js App Router default and reduces performance regressions. | Update `motion-routing.md` and `frontend-craft` gotchas. |
| Taste archetype packs | `taste-skill` minimalist/brutalist/soft/brandkit/etc. | Concrete style packs and anti-patterns. | `visual-design` and `landing-page` visual rules | 4/4/4/4/3/4/3 | adapt | Useful as reference recipes, but top-level skill sprawl would weaken Codexter's routing clarity. | Add optional archetype reference to `visual-design`; do not create many public frontend skill entrypoints yet. |
| Image-first web/mobile reference workflow | `taste-skill` imagegen web/mobile and image-to-code skills | Requires enough images/screens, consistent design language, section slicing, extraction discipline. | `landing-page` asset evidence, `frontend-craft` imagegen route | 4/4/4/4/3/4/3 | adapt | Strong for landing/product pages and complex visual builds, less necessary for every app UI task. | Strengthen landing asset/reference plan and add optional app-screen visual reference lane for premium UI. |
| Broad UI priority checklist | `ui-ux-pro-max` | Accessibility, interaction, performance, style, responsive, typography, animation, forms, nav, charts. | `visual-qa`, `frontend-craft/references/qa.md`, `web-design-guidelines` | 5/4/5/3/4/5/5 | adopt | Improves proof without disrupting topology. | Add frontend preflight checklist to `frontend-craft`/`visual-qa` including small phone, landscape, dynamic text, reduced motion, contrast, touch targets. |
| Searchable frontend rule corpus | `ui-ux-pro-max` and `design-system` scripts | Search command claims in `ui-ux-pro-max`; actual BM25 scripts in `design-system` for slides. | Static references across frontend skills | 3/3/4/5/2/4/3 | defer | Useful, but source's main `ui-ux-pro-max` search script is absent in cloned path, so evidence is mixed. | Defer until a small local search script over Codexter frontend references is scoped. |
| Brand/logo/icon/banner skill family | `ui-ux-pro-max` brand/design/banner skills | Concrete brand guideline templates, logo/icon/social/banner workflows. | `landing-page`, `imagegen`, no dedicated brandkit | 3/4/3/5/2/3/2 | defer | Valuable adjacent capability, but not the user's immediate frontend skill concern and would need its own product boundary. | Consider later `brandkit` or `design-assets` skill via separate scout/ticket. |
| Strict absolute bans from taste-skill | `taste-skill` | Bans Inter, Lucide, centered hero, purple/blue, 3-column cards, etc. | Codexter anti-slop rules | 3/5/2/3/5/2/4 | reject | Too absolute for Codexter's multi-project constraints; convert only durable principles into contextual checks. | Do not import as policy; use contextual anti-slop language. |
| External source as live dependency/base | Both repos | Repos provide skill material but differ in contracts and source assumptions. | Codexter stable local skills | 2/4/1/2/2/2/2 | reject | Violates Codexter's external-source rule and would make local contracts less stable. | Keep snapshots as evidence only. |

## Best-Of-Worlds Workflow

1. `frontend-craft` still classifies the surface and routes lanes.
2. Before implementation, `frontend-craft` records a compact stack facts card:
   - framework/router,
   - Tailwind major version,
   - available motion/icon/ui packages,
   - shadcn `components.json` and registry config,
   - theme/preset status,
   - whether an existing design system must be preserved.
3. `functional-ui` still owns user stories, IA, states, and interaction rules.
4. `visual-design` emits numeric taste dials plus a durable design brief when the work is substantial.
5. `frontend-design` uses official/current shadcn flow:
   - inspect `components.json`,
   - use registry index/domain shortlist,
   - use MCP/CLI search/view/docs before installing unfamiliar components,
   - use `apply --only theme` or `apply --only font` when a preset is appropriate,
   - preserve/private registry auth hygiene.
6. For reusable components, add a state/spec matrix covering default, hover, focus, active, disabled, loading, error, empty/success where relevant.
7. Motion work follows client-leaf isolation and transform/opacity-only default, with GSAP/Three/WebGL isolated to earned narrative or rendering surfaces.
8. QA adds small-phone, landscape, dynamic text, reduced-motion, touch target, contrast, theme parity, and no-horizontal-scroll checks.
