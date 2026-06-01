# Skill Tier Rollout Plan

Date: 2026-05-15
Status: planning draft

## Recommendation

Create a dedicated skill registry before doing another broad skill rewrite.
Do not put per-skill tier data into `docs/features/registry.jsonl`; that file
tracks harness features and techniques, not individual skill package contracts.
Use skill frontmatter as the source of truth for package-level fields, then
generate the package registry from it.

Best path:

1. Keep this document as the human-readable rollout plan.
2. Add only the manual package metadata fields to `skills/*/SKILL.md`
   frontmatter: `tier`, `source`, Tier 3 `group`, optional `methods`,
   optional `upstream_url`, and optional Tier 3 `common_chains`.
3. Add a script such as `bin/sync_skill_registry.py` that reads skill
   frontmatter, validates tiered checklist links, and writes a generated
   `docs/skills/registry.jsonl`.
4. Generate flow or graph views from Tier 3 `group` plus `common_chains`; do
   not maintain a second hand-authored sequence registry.
5. Put required every-invocation checklist items directly in `SKILL.md` and
   prune redundant `todos.md` files once migration is complete.
6. Consolidate only after the registry exposes real duplicate surfaces; prefer
   one owning skill with `skill:method` addresses when several wrappers share
   the same workflow, proof contract, and references.

## Tier Contract

Treat skills as a dependency hierarchy, not a hidden router tree.

- **Tier 1 primitives** are core judgment and quality defaults:
  `advise`, `reference-grounding`, `review`, and skill first-load checklist
  loading.
  Add a new Tier 1 primitive only when multiple Tier 2 interfaces need that
  move as a base dependency. If the behavior is common but primarily
  evidence-gathering, planning, execution, or review shaped, keep it as a Tier
  2 method first.
- **Tier 2 interfaces** are generic workflow surfaces:
  `brainstorm`, `research`, `plan`, and `execute`.
- **Tier 2 methods/helpers** are evidence, proof, or workflow support surfaces
  that can be called by many domains without becoming domain workflows.
  User research belongs here as `research:user-grounding` unless it later proves
  to be a base primitive required by several Tier 2 interfaces.
- **Tier 3 application skills** bind the generic interfaces to a domain:
  coding tickets, frontend, landing pages, image/video assets, content
  production, data visualization, docs, presentations, and harness operations.
  Tier 3 skills may chain to other Tier 3 skills, but flow or graph views
  should be generated from local metadata instead of hand-maintained as a
  second registry.
- **`skill:method` names** should identify explicit methods inside one owning
  skill. They should not create nested router traversal.
- **Router-style skills** should use conditional checklists, not sequential
  "run every method" checklists. Pick one primary method first, add supporting
  methods only when a trigger appears, and stop when the next skill has enough
  evidence or plan shape.

## Registry Shape

The future registry should use different shapes for the different tiers.

### Source Of Truth

Split the source of truth by ownership:

- `skills/*/SKILL.md` frontmatter owns package-local metadata:
  existing `name` and `description`, plus only the added fields that require
  human judgment: `tier`, `source`, Tier 3 `group`, optional `methods`,
  optional `upstream_url`, and optional Tier 3 `common_chains`.
- The sync script derives file-local facts:
  `path`, `has_checklist`, legacy `has_todos`, `version`, `allowed_tools`, and
  Markdown skill links.
- The sync script rejects Tier 3 checklists that direct-link Tier 1
  primitives. Tier 3 checklists should link the relevant Tier 2 surface and let
  that surface carry Tier 1 obligations.
- `docs/skills/registry.jsonl` is generated output. Do not hand-edit it.
- Flow and graph views are generated from Tier 3 `group` and `common_chains`
  metadata. Do not maintain a separate hand-authored sequence registry.

Keep checklist coverage as a derived field instead of a frontmatter field. The
source of truth is the marker-delimited `## Important Checklist` section inside
`SKILL.md`; legacy `todos.md` files are migration inputs only.

Do not add `role`, `depth_dependencies`, `consolidation`, or `notes` to
frontmatter in the first registry pass. Those are either inferable from the
directory and Markdown content or temporary planning judgments that should stay
in this rollout document until they prove stable. `group` is the one deliberate
Tier 3 classification field because it lets tooling generate application views
without a separate sequence registry.

Use `source: external` for skill packages that are upstream-owned and should be
refreshable from an outside source, such as `agent-browser`. A Codexter wrapper
that merely reads external docs can remain `source: local`. Codexter-specific
wrapper logic belongs in local caller skills like `qa`, not in the external
skill body.

Use `upstream_url` when one canonical upstream file is enough to refresh or
audit an external skill. Do not add an `update_command` field until more than
one external skill needs command-shaped refresh logic.

For Tier 3 skills, frontmatter may include `common_chains` as a local adjacency
hint. Use it for common next skills only, not for full orchestration graphs:

```yaml
tier: 3
group: coding
common_chains:
  after: ["impl"]
```

This field is useful for generated registry search, discovery, and graph views.
Keep it one-directional: a skill may list the common next skills it hands off
to, but downstream skills should not also list matching `before` entries. The
sync script can derive reverse lookup views when needed. Loops such as "for
each ticket, run `impl-plan` then `$impl` then `close-ticket`" should be
described in the owning skill docs or todos, not duplicated as hand-authored
registry rows.

### Tier 1 And Tier 2 Rows

Tier 1 and Tier 2 entries can stay skill-shaped because they are called in
depth by other skills. Use numeric tiers only:

```json
{
  "name": "research",
  "tier": 2,
  "path": "skills/research/SKILL.md",
  "description": "Tier 2 evidence workflow with method-addressed research passes...",
  "methods": ["research:parity", "research:gap", "research:competitor"],
  "has_checklist": true,
  "has_todos": false,
  "skill_links": ["advise", "reference-grounding", "review"]
}
```

Recommended generated package fields:

- `name`: existing frontmatter.
- `description`: existing frontmatter.
- `tier`: added frontmatter, numeric `1`, `2`, or `3`.
- `source`: added frontmatter, `local` or `external`.
- `path`: generated from the directory.
- `methods`: optional frontmatter only when the skill owns method addresses.
- `group`: required frontmatter for Tier 3 skills only.
- `common_chains`: optional frontmatter, Tier 3 only, one-directional.
- `upstream_url`: optional frontmatter for upstream-owned skill packages.
- `has_checklist`: generated from the direct checklist or temporary legacy todo
  source.
- `has_todos`: generated from the filesystem for migration visibility only.
- `version`: existing frontmatter when present.
- `allowed_tools`: existing frontmatter when present.
- `skill_links`: generated from Markdown links in `SKILL.md` and optional
  legacy `todos.md`.

This is intentionally small. Anything that can be calculated should be
calculated. Higher-level flow views should be generated from `group`,
`common_chains`, and Markdown links rather than hand-maintained as another
registry.

### Tier Classification Rule

Classify a new skill or method by where it is reused:

- Tier 1 only for primitives that multiple Tier 2 surfaces call as base
  obligations.
- Tier 2 for generic interfaces and reusable methods that many Tier 3
  application skills can call directly.
- Tier 3 for domain/application skills, including application-specific routers
  or execution surfaces.

Do not promote a common task to Tier 1 just because many Tier 3 skills may need
it. If Tier 3 skills can call it through one owning Tier 2 surface, keep it
there. `research:user-grounding` is the example: functional UI, PRDs, landing
pages, content, docs, and onboarding may all need user lenses, but the work is
research-shaped and should live under `research` first.

### Tier 3 Groups And Chains

Tier 3 skills are application skills. Some are full application entrypoints
(`video-production`, `landing-page`, `impl-plan`), and some are application
execution surfaces that other Tier 3 skills commonly call (`image-generation`,
`video-generation`, `remotion-render`, `frontend-craft`). That is okay: Tier 3
can have local routers or method surfaces when the domain needs them.

Use `group` to keep Tier 3 discoverable without over-modeling sequences:

```yaml
tier: 3
group: content-video
```

Use `common_chains.after` only when a skill has a stable next handoff worth
showing in generated views. Do not force every possible relationship into
frontmatter. Loops, recipes, and execution semantics should remain in the owning
skill body, where agents will actually read them.

## Current Package Inventory

The current package inventory is generated instead of hand-maintained. Use:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 bin/sync_skill_registry.py --write
python3 bin/sync_skill_registry.py --check
```

Current generated baseline should be read from the generated registry:

- `docs/skills/registry.jsonl`: generated package rows
- Tier counts and source counts: generated from skill frontmatter
- Checklist coverage: generated from direct `SKILL.md` checklists or temporary
  legacy `todos.md` migration inputs
- External skills without local checklists may include `agent-browser`,
  `convex`, and `vercel-react-best-practices`
- Method-addressed skill metadata exists where it is real, with `research`
  owning the main research method list and `social-content` owning the
  social-content method list
- Tier 3 application views should be generated from `group`,
  `common_chains`, and Markdown links

This generated registry replaces the earlier hand-written package table. Use the
rollout ticket for decisions and use the generated files for current-state
truth.

For future bulk skill-system upkeep, use `skill-maintenance` instead of putting
all skill-maintenance rules into the always-loaded system prompt. It owns the
periodic workflow for tier classification, source ownership, checklist audits,
registry sync, and consolidation planning.

## Application Flow Parallels

Coding and content work already share an abstract flow. The difference is the
domain artifact and proof surface.

| Generic stage | Coding example | Landing/content example | Image/video/social example |
| --- | --- | --- | --- |
| Intent intake | `prd`, `deep-system-design` | offer, audience, narrative gates | campaign brief, platform, audience, asset goal |
| Reference grounding | local code, specs, peers, official docs | competitors, inspiration sites, product assets | platform specs, examples, upstream guides, model docs |
| Plan | `spec-to-ticket`, `impl-plan` | `LANDING_SPEC.md`, section matrix, asset plan | script, shot list, slide plan, prompt plan |
| Execute | `$impl`, workers, QA lanes | `frontend-craft`, generated assets, page build | `image-generation`, `video-generation`, `remotion-render` |
| Proof | tests, lint, QA artifacts, review | screenshots, scroll QA, asset manifest, visual QA | saved prompt/input/result bundles, renders, platform-fit review |
| Closeout | `close-ticket`, docs, commit | handoff, publish/export if explicit | final asset paths, no publish unless explicit |

The more general application pattern is:

1. **Spec planning:** understand the goal, references, options, and constraints.
2. **Spec execution:** write the accepted spec, brief, storyboard, content plan,
   or implementation contract.
3. **Work-unit creation:** create tickets, assets, pieces, shots, slides,
   prompts, scenes, or sections.
4. **Work-unit planning:** plan the selected unit with dependencies, proof, and
   accepted tradeoffs.
5. **Work-unit execution:** build, generate, render, write, or assemble the unit.
6. **Proof, review, and closeout:** verify the output, review quality, record
   evidence, and hand off or publish only when explicitly authorized.

Coding uses literal tickets as work units. Content creation often uses assets,
pieces, prompts, shots, slides, scenes, or sections instead. The registry should
allow both without pretending every domain needs filesystem tickets.

This makes content creation a good next proving ground for the tier model:
content skills are domain-specific enough to need Tier 3 checklists, but similar
enough that one or two shared checklist templates can cover most of them.

## Content Checklist Template

Use this template when adding a direct `## Important Checklist` to content
creation skills:

- [ ] Classify the artifact: post, carousel, video, storyboard, product photo,
  landing page, deck, document, or campaign bundle.
- [ ] State the intended output and handoff path before execution.
- [ ] Use [research:competitor](../../skills/research/SKILL.md#researchcompetitor)
  or [research:parity](../../skills/research/SKILL.md#researchparity) when the
  content needs examples, market, platform, source-asset, current-model, or
  peer-pattern grounding.
- [ ] Use [plan](../../skills/plan/SKILL.md) when choosing among channels,
  narrative angles, visual carriers, model families, or scope cuts.
- [ ] Write a compact plan with artifact structure, asset list, prompt/script
  plan, proof checks, and publish boundaries.
- [ ] Execute through the owning domain layer: `image-generation`,
  `video-generation`, `remotion`, `remotion-render`, `frontend-craft`, or the
  relevant plugin skill.
- [ ] Save prompts, inputs, result JSON, generated files, and notes in the
  workspace when external generation is involved.
- [ ] Follow the [execute](../../skills/execute/SKILL.md) proof and writeback
  loop before claiming final quality.
- [ ] Do not publish, post, spend, or run external compute unless that boundary
  is explicit for the task.

## Rollout Plan

### Phase 1: Registry And First Content Checklists

Add frontmatter metadata, generate a dedicated skill package registry, and add
missing first-load checklists for the content creation cluster:

- `video-production`
- `product-photography`
- `social-content`
- `remotion`
- `remotion-render`

Expected proof:

- package inventory rows for every local skill
- generated registry rows match skill frontmatter and local skill count
- Tier 3 groups appear in generated registry rows
- Markdown links in each new checklist resolve locally
- no content skill requires nested router traversal to know its first step

### Phase 2: Frontend And Coding Support Checklists

Add missing direct checklists to frontend, backend, testing, and coding-support
skills that are called often but lack checklists:

- `frontend-craft`
- `functional-ui`
- `visual-design`
- `frontend-design`
- `web-design-guidelines`
- `agent-browser`
- `qa`
- `demo`
- `prd`
- `pr-runtime`
- `codexter-invocation`

Expected proof:

- Tier 3 skills link the Tier 2 interface they implement
- proof, writeback, and visual QA obligations appear as linked checklist items
- support skills stay support skills instead of becoming hidden routers

### Phase 3: Consolidation Decisions

After the registry exposes dependencies, make hard migrations where the merge
is clearly one owner with method addresses. The first validated migration is
the social-content cluster:

- `ai-social-media-content` -> `social-content:cross-platform`
- `social-media-carousel` -> `social-content:carousel`
- `linkedin-content` -> `social-content:linkedin`
- `twitter-thread-creation` -> `social-content:twitter-thread`

Keep copied upstream references under `skills/social-content/references/` so
platform-specific examples are not lost. Keep media execution layers separate:
`image-generation`, `video-generation`, `remotion`, and `remotion-render` are
tool/proof surfaces, not social-content subtype wrappers.

Next consolidation candidates:

- Next ticket: `TASK-0151` should consider `video-production:marketing`, `video-production:explainer`,
  `video-production:storyboard`, `video-production:talking-head`, and
  `video-production:ad-spec`.
- Treat `social-content:linkedin`, `social-content:twitter-thread`,
  `social-content:carousel`, and `social-content:cross-platform` as the proven
  method-address pattern.
- Keep `documentation` and `external-patterns` as separate Tier 2 skills for
  now. They are reference-grounding-adjacent helper surfaces with distinct tool
  and codebase-search behavior, not obvious Tier 3 sibling wrappers. Revisit
  only if call sites become mostly `research:official-docs` or
  `research:code-patterns`.
- Keep `image-generation` and `video-generation` as shared execution layers.
  They are not generic Tier 2 interfaces because their model maps, spend gates,
  and asset bundles are domain-specific.

Expected proof:

- `rg` finds no stale Markdown links to removed skill directories after a hard
  migration
- all updated dependencies point to the owning `skill:method` address
- removed skill directories have no live references outside archive/research

## Pushback

Do not load every Tier 1 primitive into every `SKILL.md` body. That creates
prompt bloat and makes updates hard to keep consistent. The better pattern is:

- global/system policy states the tier model once
- Tier 1 and Tier 2 checklists import the primitive or method obligations
  they own
- Tier 3 skills link their Tier 2 interface or method surface, and the Tier 2
  surface carries the Tier 1 defaults

That keeps the hierarchy explicit without turning every skill into a copied
mini-system prompt.
