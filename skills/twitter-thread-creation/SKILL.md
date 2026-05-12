---
name: twitter-thread-creation
version: 1.0.0
description: Plan and write Twitter/X threads, tweet storms, hook tweets, X posts, reply chains, media-supported threads, and engagement-optimized social writing. Covers thread structure, character limits, hooks, summaries, CTAs, and media attachments. Routes visuals through `imagegen` or `image-generation`, social campaigns through `ai-social-media-content`, and frontend/campaign bundles through `frontend-craft`.
allowed-tools: Read, Grep, Glob, Bash
---

# Twitter/X Thread Creation

Domain entrypoint for Twitter/X threads and posts.

## Steps

1. Load the shared [image/social production workflow](../image-generation/references/domain-production.md).
2. Load the [upstream Twitter/X guide](references/upstream.md) for thread structures, hooks, character limits, formatting, and examples.
3. Decide the artifact: single post, hook tweet, thread, reply chain, media-supported thread, or cross-platform variant.
4. Draft the thread with standalone tweet logic and any needed visual prompts.
5. Do not post through `belt` or any social API unless the user explicitly asks to publish.

Use the shared production workflow for saved drafts, media assets, upstream-reference safety, and campaign QA.
