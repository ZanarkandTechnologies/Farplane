# Summarize

## Purpose

Guide agents to use the external `summarize` CLI for quick URL, file, and
YouTube summaries or transcript extraction.

## Public API / Entrypoints

- `SKILL.md`: main workflow contract
- `AGENTS.md`: maintenance rules

## Minimal Example

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto --extract-only
```

## How To Test

- confirm `SKILL.md` uses the `summarize` binary name consistently
- confirm URL/file/YouTube cases are all covered
- confirm transcript extraction is described as best-effort, not guaranteed
