# Landing Registry Format

Use the JSON registries when a landing-page request needs repeatable examples,
taste routing, or effect-stack selection.

## Files

- `landing-recipes.json` - page formulas and section structure.
- `taste-profiles.json` - visual register and taste constraints.
- `effect-stacks.json` - implementation mechanics, assets, debug hooks, and QA.

Each file uses:

```json
{
  "schema_version": "1.0.0",
  "kind": "landing-recipes",
  "records_key": "recipes",
  "recipes": []
}
```

## Routing

1. Select one recipe from `landing-recipes.json`.
2. Select one compatible taste profile from `taste-profiles.json`.
3. Select one compatible effect stack from `effect-stacks.json`.
4. Produce a landing brief that names all three selected IDs.
5. Load the detailed record only when it is relevant to the request.

Compatibility is advisory, not a hard parser rule. A request can intentionally
mix records when the reason is explicit.

## Authoring Rules

- Keep records short enough to scan but complete enough to build from.
- Use arrays of concrete strings instead of paragraph blobs.
- Put URLs and private repo refs in `reference_examples`.
- Keep copy, CTA, proof, assets, fallbacks, and QA expectations explicit.
- Keep implementation library details in `effect-stacks.json`, not recipes.
- Keep visual taste in `taste-profiles.json`, not effect stacks.
- Keep app UI profiles out of these landing registries; app UI stays with
  `functional-ui` and `visual-design`.

## New Record Checklist

- `id` is stable kebab-case.
- `title` is human-readable.
- `use_when` and `avoid_when` are specific enough to route.
- Examples include 2-3 high-signal references when available.
- Compatible record IDs point to existing records or clearly planned follow-ups.
- The record avoids vague mood-board language unless it also names structure,
  assets, proof, and QA.

Validate JSON with:

```bash
python3 -m json.tool skills/landing-page/references/landing-recipes.json >/dev/null
python3 -m json.tool skills/landing-page/references/taste-profiles.json >/dev/null
python3 -m json.tool skills/landing-page/references/effect-stacks.json >/dev/null
```
