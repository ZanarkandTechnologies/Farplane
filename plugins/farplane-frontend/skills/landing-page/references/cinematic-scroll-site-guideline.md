# Cinematic Scroll Site Guideline

This file is kept as a stable compatibility pointer for older references.

For new cinematic or Terminal-style landing work, use the JSON registry records:

- `landing-recipes.json` -> `industrial-mission-control`
- `taste-profiles.json` -> `terminal-palantir`
- `effect-stacks.json` -> `cinematic-frame-sequence`
- `registry-format.md` -> JSON field contract and authoring rules

## Routing

1. Use `industrial-mission-control` when the page is an enterprise, industrial,
   logistics, infrastructure, operations, or AI-control landing page where one
   physical world becomes a command layer.
2. Pair it with `terminal-palantir` when the look should feel dark, precise,
   proof-heavy, operational, and mission-control rather than generic SaaS.
3. Pair it with `cinematic-frame-sequence` when the hero is a generated or
   rendered video converted into scroll-scrubbed frames with GSAP and HTML
   overlays.

Keep GSAP API details source-fresh through official GreenSock docs or installed
GreenSock skills. Keep generated image or video asset production in the
appropriate asset-generation workflow, then bring the resulting files back into
the effect stack's asset and QA contract.
