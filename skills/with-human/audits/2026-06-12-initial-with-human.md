---
date: 2026-06-12
change: initial-with-human
skill: with-human
---

# Initial With Human Audit

## Reason

Human feedback is a provider for Goal loops, not a standalone autoresearch
runtime. The previous session-shaped feedback name made the ownership boundary
less clear after native Goal mode became the continuation engine.

## After

`with-human` owns feedback requests, feedback schema, and notification handoff.
Native Goal mode owns continuation, and the Goal Packet owns durable state.
