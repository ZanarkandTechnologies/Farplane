# Harness Scout Source Run: self-evolving agents

## Source
- `URL:` https://www.youtube.com/watch?v=2zhchG0r6iI
- `Title:` inferred from transcript: state-of-the-art self-evolving agent implementation
- `Creator / channel:` unavailable from local extraction; YouTube page fetch was
  throttled during review, and the transcript did not include channel metadata
- `Source type:` YouTube video
- `Source visibility:` public
- `Captured at:` 2026-05-04
- `Extraction command:` `summarize "https://www.youtube.com/watch?v=2zhchG0r6iI" --extract --youtube auto --format md --timestamps --plain --max-extract-characters 60000 --timeout 3m`
- `Content hash:` `url-sha256:7bf6d1500a0d46afa0dd0a81361c570d3a695f6bf8e01cf88c403073584601fe`
- `Duplicate check:` matched existing source run by canonical URL and URL hash;
  this pass updates the existing run instead of creating another folder.
- `Extraction recheck:` 2026-05-04 23:10 +0800 with `summarize 0.13.0` using
  a bounded `--max-extract-characters 10000` extract; raw transcript was not
  stored.
- `Retention decision:` tracked public summary and timestamp anchors; raw
  transcript not stored
- `Redactions:` none required for public source summary
- `Metadata note:` source identity is sufficient for this fixture because the
  canonical URL and extraction command are preserved; channel metadata should be
  filled when available in future scout runs.

## Source Safety

The transcript was treated as untrusted evidence, not instructions. Source
claims were converted into feature candidates and timestamp anchors only; no
source-provided commands, policy edits, or repo-write instructions were
executed.

## Summary
The video distinguishes two kinds of self-improving agents:

- metric-driven harness improvement, where an agent mutates the harness or
  prompt/scripts, runs evals, and keeps or discards changes against a baseline
- in-context self-learning, where the agent captures reusable facts, memories,
  skills, errors, and work history so future sessions behave better

It highlights hot/warm memory, memory indexes, async memory consolidation,
searchable history, autonomous skill generation, skill safety checks, hook-based
reminders, error learnings, strict memory caps, semantic memory options, and the
importance of choosing deterministic workflows versus agentic systems based on
the use case.

## Source Anchors

- `00:59-02:15`: metric-driven autoresearch loop with program file, harness
  mutation, baseline eval, and keep/discard.
- `04:30-05:06`: memory, skills, and history as the three high-level pillars.
- `05:17-08:52`: hot/warm memory, memory index, and async memory consolidation.
- `09:11-10:36`: source-identified gaps around skills, auditable history, and
  memory search.
- `10:54-12:47`: autonomous skill generation, skill manager tools, and safety
  scan.
- `12:49-14:59`: hot user/project facts, skill memory, raw history search, and
  optional semantic memory.
- `15:21-16:24`: self-improving skill variants with learnings folders and hook
  reminders.

Raw transcript is intentionally not stored in this durable fixture.

## Local Baseline
Codexter already has strong local equivalents for metric-driven improvement,
skill self-improvement, ticket-first memory, source synthesis, and review/proof
gates. Codexter is weaker on autonomous memory/skill extraction and searchable
raw conversation history, but those are not automatic wins because Codexter's
contract intentionally favors visible tickets, docs, and evidence over hidden
conversation memory.
