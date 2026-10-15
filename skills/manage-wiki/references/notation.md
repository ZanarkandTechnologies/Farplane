# Wiki Authoring Notation

Read before staging or reviewing Wiki Markdown. This is the complete
compiler-significant notation; ordinary Markdown stays ordinary prose unless it
is listed here. Storage, search and projection behavior live in
[wiki-contract.md](wiki-contract.md).

## Notation Catalogue

| Scope | Notation | Meaning and rules |
| --- | --- | --- |
| Frontmatter | `---` YAML `---` | Required at the start of every article; it must parse as a mapping |
| Identity | `id: acme` | Required; lowercase letters, digits, hyphens, or underscores; must equal the filename stem and cannot start with `.` or `-` |
| Classification | `kind: company` | Required project-owned entity type; it scopes search and consumers but does not create a folder |
| Display | `name: Acme` | Required canonical human-readable name |
| Lookup | `aliases: [Acme Corp]` | Optional alternate labels used by exact and hybrid resolution |
| Identity refs | `company_ref`, `organization_ref` | Optional single IDs; validated lookup relationships, not graph edges |
| Identity refs | `entity_refs`, `person_refs`, `opportunity_refs`, `relationship_refs` | Optional ID lists; validated lookup relationships, not graph edges |
| Place | `location: Penang, Malaysia` | Optional display/filter label; no geocoding |
| Coordinates | `latitude`, `longitude` | Optional paired finite numbers within latitude `-90..90` and longitude `-180..180` |
| External refs | `links: [https://…]` | Optional durable profile/source URLs; they do not create entity edges |
| CRM | `funnel: {…}` | Optional non-empty mapping; includes this same entity in generated `crm.json` |
| Title/sections | `# Name`, `## Context` | Human article structure and nearest-section provenance; headings do not create entities or edges |
| Entity relation | `[Acme](entity:acme)` | Resolved body link; creates a paragraph-backed outgoing claim and Wiki graph association from this article |
| Source evidence | `[filing](https://…)` | HTTP(S) link in the same claim/timeline context; captured as source evidence, not an entity edge |
| Question ref | `[^q-20260819-01]` | Attaches one or more stable question IDs to the containing factual block |
| Question definition | `[^q-…]: Exact question?` | Required same-file definition for a used question ID |
| Session provenance | `[^q-…]: Question? \| session=<id>` | Optional local session provenance; the `q-*` ID remains question identity |
| Named view | `## View: AI Infrastructure` | Starts view-specific article context; matches a configured view ID or name |
| Current view state | `### Latest Status` | Freeform current interpretation under a named view |
| Status date | `_As of 2026-08-19_` | Optional latest-status date; `As of:` is also accepted |
| Status tags | `[role:compute-provider]` | Any `[key:value]` tags inside Latest Status are preserved as typed current context |
| Timeline | `### Timeline` | Only dated list items below this heading become timeline evidence |
| Timeline row | `- 2026-08-19 …` | `-`, `*`, or `+` list item followed by an ISO date; event identity is generated from semantic content |
| View route | `[view:ai-infrastructure]` | Routes a timeline item when its heading is insufficient |
| Event type | `[relation:investment]` or `[type:investment]` | Explicit event/relationship type; otherwise configured patterns may classify it |
| State | `[status:announced]` | View-defined lifecycle value |
| Confidence | `[confidence:primary]` | View-defined evidence-confidence value |
| Signal | `[signal:capacity-risk]` | Freeform typed signal preserved on the event |
| Resource observation | `[<configured-resource-tag>:2 USD-billion by 2028]` | Numeric value, unit, and optional `by` or `@` horizon interpreted by `.farplane/views.yaml` |
| Metric | `[<configured-metric-tag>:300 MW]` | Numeric value and unit interpreted by `.farplane/views.yaml` |
| Literal examples | inline code or fenced code | Entity links, question refs, and timeline metadata inside code are ignored |
| Retired notation | triple-backtick fence whose info string is `farplane` | Invalid; use headings, entity links, question footnotes, and inline tags |

An entity link is the only notation that creates a generic Wiki graph edge.
`*_ref` fields and `links` validate and support lookup but never create edges.

## File And Identity

Pages sit directly in `.farplane/entities/<id>.md`; nested folders are invalid
and the filename stem must equal `id`. The folder may symlink into the
local-only memory repo. Every page needs `id` (lowercase letters, digits, `-`,
`_`; not starting with `.` or `-`), `kind` (free classification, no folder) and
`name`. Optional fields are listed in the catalogue above plus `roles`,
`problems`, `resources` and `goals` below.

Keep view-specific metrics, statuses and relation vocabulary out of
frontmatter: put them inline under the view section and define them in
`.farplane/views.yaml`.

## Roles, Problems, Resources

Only people and companies own pages. `roles` says what the owner is to you
(`client`, `creator`, …). Problems and resources are items on the owner's page:

- `problems[]`: `id`, `text`, optional `since`, `ongoing` (bool), `size`,
  `status` `open` (default) | `solved` | `dropped`, `source`.
- `resources[]`: `id`, `text`, `source`, and `helps[]` of
  `{problem: <owner-id>#<item-id>, impact: high|medium|low, status: suggested|confirmed}`.
  `status` defaults to `suggested`; every `problem` must resolve.

```yaml
# .farplane/entities/kenji-phang.md
resources:
  - id: agent-workflows
    text: Agent-built workflow automation
    helps:
      - {problem: hank-globex#leads, impact: high, status: suggested}
```

## Goals

A page may carry `goals[]`: `title`, optional `unit`, `target` (a number, or
unset until chosen), `deadline`, and `setups[]`. A setup has optional `for` (a
person or company), `owner`, `done_when`, `project` (the project floor it runs
on) and `steps[]` whose `status` is `todo` | `next` | `done` | `blocked`; the
steps form the critical path.

## CRM

CRM has no separate record. A non-empty `funnel` mapping, or `client` in
`roles`, puts the page in `crm.json`. Removing it removes the CRM entry but
keeps the page in the index and graph. Deals carry
`funnel.value: {amount, currency, per: month|project, note}`.

## Entity Links

Only a resolved `[label](entity:<id>)` in body prose makes a graph
association, kept with its sentence, nearest section, path, source URLs and
question refs. Associations are undirected; prose may state direction. Links
inside inline or fenced code are ignored; HTTP links are evidence. Self-links
are invalid. Never copy the sentence into the target to make a reverse edge.

## Questions

Put `[^q-YYYYMMDD-NN]` on the factual block and define
`[^q-…]: <exact question>` in the same file, optionally followed by
`| session=<id>` (never turn ids). The question id, not the session, is
identity. Reuse an id only for the same inquiry; repeated definitions across
files must match text. Questions are not graph nodes; provenance, storage paths
and link spelling are excluded from claim and edge keys, so adding provenance or
moving a file does not replace an unchanged relationship.

## View Sections

Under `## View: <id or name>`, `### Latest Status` is freeform current context
(`_As of YYYY-MM-DD_`, `[key:value]` tags kept). Only dated bullets under
`### Timeline` become events; event keys are generated, never authored. A row
counts for its page and every linked entity, so never duplicate it in the
counterparty's page.

A fenced block with info string `farplane` is retired and fails validation;
move its data to inline tags under the view section.

## View Configuration

`.farplane/views.yaml` (ignored, local) holds membership and vocabulary. Each
view needs a `name` and a non-empty, unique `entity_ids` list of resolvable ids
(canonical id syntax for view ids too). Duplicate YAML keys are invalid. No file
means no views; an empty scaffold is `views: {}`. Declared member order is kept;
views sort by id.

```yaml
views:
  ai-infrastructure:
    name: AI Infrastructure
    entity_ids:
      - nebius
      - nvidia
    relations:
      investment:
        patterns:
          - invested in
    resources:
      capital:
        name: Capital
        measure: flow
        base_unit: USD-billion
        units:
          USD-billion: 1
          USD-million: 0.001
    resource_tags:
      capital-demand:
        resource: capital
        direction: demand
        entity: source
    status_weights:
      announced: 0.5
    confidence_weights:
      primary: 1
```

A view may define `relations` (match patterns), `resources` (measure,
base_unit, unit conversions), `resource_tags` (resource, direction, entity,
optional transfer), `status_weights` and `confidence_weights`. Unknown
statuses, confidences, resources, units, transfers or selectors are compile
issues.

## Observations And Transfers

A resource tag records an observation (supply, demand, capacity, requirement),
not an exchange. Add `transfer: source-to-linked` or `linked-to-source` only
when the tag asserts something moved, and only with exactly one linked
counterparty. Never render untagged observations as money, power or compute
changing hands.

## Example

```markdown
---
id: nebius
kind: company
name: Nebius
aliases:
  - Nebius Group
location: Amsterdam, Netherlands
links:
  - https://nebius.com
funnel:
  pipeline: partnerships
  stage: researched
  status: active
  next_action: Verify infrastructure partnership fit
---

# Nebius

## Durable context

Cloud infrastructure company tracked for AI compute and power relationships.

## Relationships

Nebius received an investment from [NVIDIA](entity:nvidia). [^q-20260731-01]
Source: [company announcement](https://example.com/announcement).

## View: AI Infrastructure

### Latest Status

_As of 2026-07-31_

[role:compute-provider] Expanding AI infrastructure capacity while depending on
accelerator and power availability.

### Timeline

- 2026-03-11 [relation:investment] [status:announced] [confidence:primary]
  [capital-demand:2 USD-billion] Nebius announced an investment relationship
  with [NVIDIA](entity:nvidia).
  Source: [filing](https://example.com/filing).

## Question index

[^q-20260731-01]: Which companies connect AI capital, compute, and power supply?
```

The example contributes:

- one canonical entity record;
- one paragraph-backed Wiki graph association;
- one question-backed claim;
- one view-specific latest status;
- one dated typed-view event;
- one resource observation when `capital-demand` is declared in the view;
- one CRM entry because `funnel` is a non-empty mapping.
