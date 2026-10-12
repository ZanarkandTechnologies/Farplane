# Reference Overrides

Use this before copying commands from upstream reference files.

## Known Stale App IDs

| Upstream app ID | Status | What to do |
| --- | --- | --- |
| `infsh/hunyuanvideo-foley` | `belt app get infsh/hunyuanvideo-foley` returns app-not-found on belt v1.9.9 | Do not run directly. Search live with `belt app search foley` and `belt app search sound`; inspect candidates with `belt app get <app>`. If only audio-only sound effects are available, record that limitation before substituting. |

## Reference Rule

Copied upstream files are usage references, not local truth. The active `SKILL.md`, [providers](providers.md), this override file, and live `catalog_get` or `belt app get` checks win over stale examples inside copied references.

The files under `tools/` describe the inference.sh (`belt`) route. That route is a fallback: the default paid route is treg (see [providers](providers.md)). Use `belt` only when treg has no listing for the needed model or the listing fails, and say so in the receipt.
