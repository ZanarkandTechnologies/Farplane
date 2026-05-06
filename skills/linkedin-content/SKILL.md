---
name: linkedin-content
version: 1.0.0
description: Plan and write LinkedIn content, thought-leadership posts, B2B posts, professional carousels, hooks, comments, and personal-brand content. Use for LinkedIn posts, LinkedIn strategy, professional content, B2B content, founder posts, hiring posts, and LinkedIn carousel planning. Routes writing through domain guidance, carousels through `social-media-carousel`, visuals through `imagegen` or `image-generation`, and campaign bundles through `frontend-craft`.
allowed-tools: Read, Grep, Glob, Bash
---

# LinkedIn Content

Domain entrypoint for LinkedIn writing and professional social content.

## Steps

1. Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
2. Load the [upstream LinkedIn guide](references/upstream.md) for hook formulas, post anatomy, formatting rules, and engagement patterns.
3. Decide the artifact: text-only post, thought-leadership post, founder story, B2B announcement, carousel outline, comment, or cross-post variant.
4. If visuals or carousel slides are needed, route to `social-media-carousel`, `imagegen`, or `image-generation`.
5. Draft content first; do not publish or cross-post unless the user explicitly asks to publish.

Use the shared production workflow for saved drafts, asset bundles, upstream-reference safety, and campaign QA.
