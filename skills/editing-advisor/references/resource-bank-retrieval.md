---
title: Editing Creative Pattern Retrieval
owner: editing-advisor
status: active
---

# Editing Creative Pattern Retrieval

Load this reference when the advisor must discover reusable creative patterns, prove
their source, or distinguish Resource Bank records from Brand Kit snapshots and
skill findings.

## Source precedence

1. Explicit caller constraints and approved Brand Kit policy govern the run.
2. Resource Bank CreativeElements with `kind: editing` are the canonical
   cross-project creative-pattern corpus.
3. A Brand Kit editing element is an approved project/brand snapshot; it may
   approve, constrain, or pin a Resource Bank pattern but does not replace
   the corpus.
4. A caller-supplied complete editing element is valid for the current run.
5. Skill findings describe proposed harness/skill improvements. Never use them
   as production conditioning recipes.

Deduplicate by stable element ID when available; otherwise use normalized title
plus provenance. Preserve conflicts instead of silently merging them.

## Current Farplane UI adapter

From the Farplane UI project, direct retrieval is the normal path when the
brief already names an editing need:

```bash
corepack pnpm exec convex run modules/resourceBank/creativeElements:listCreativeElements \
  '{"query":"exact state handoff tactile pacing captions","kind":"editing","projectId":"farplane-ui","limit":8}'
```

Use a Tasty Pack when the request needs broader reference discovery and
cross-kind inspiration while keeping the editing filter explicit:

```bash
corepack pnpm exec convex run modules/resourceBank/retrieval:createTastyPack \
  '{"idea":"35-second evidence-led explainer with tactile editorial motion","kinds":["editing"],"projectId":"farplane-ui","limit":8}'
```

Load the approved production snapshot through the Resource Bank Brand Kit
adapter when a Brand Kit ID is known. The current query owner is
`brandKits:getBrandKitForProduction`; inspect its local signature before calling
because identifiers are project/runtime state.

## Acceptance

For each selected pattern, resolve:

```text
element_id? + provenance + title + description + whyItWorks
+ goldenExample + goldenRecipe + anchor? + tags[]
```

If the adapter is unavailable, state the exact missing project/runtime input
and continue only with complete caller-supplied packets. If a selected record
lacks its golden example or recipe, mark it `block` and stop before renderer
handoff. Do not reconstruct the missing recipe from the title or from model
memory.
