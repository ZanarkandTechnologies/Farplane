---
name: commit-message
version: 0.1.0
description: "Compact commit-subject skill. Use when writing a commit message from staged changes or recent diffs. Follows the repo style: type(scope): lower-case imperative summary."
allowed-tools: Read, Glob, Grep
---

# Commit Message

Use when the user asks for a commit message, commit title, or to infer the repo's commit style from history.

<!-- MEM-0009 decision: commit subjects should default to compact Conventional-style form: type(scope): lower-case imperative summary; output one best subject first, then short alternates only if ambiguity remains. -->

## First-Load Contract

### Trigger Conditions

- user asks for a commit message
- user asks to infer or follow the repo's commit standard
- staged diff or recent changes need a concise subject line

### Workflow (6 Steps)

1. **Read signal**: inspect staged diff, changed files, or recent commit history.
2. **Find main delta**: choose the single highest-signal change, not the changelog.
3. **Pick type**: use the smallest truthful type.
4. **Pick scope**: use a short scope when obvious; omit only if the diff is cross-cutting and no short scope fits.
5. **Write subject**: `type(scope): summary` in lower-case imperative style.
6. **Trim**: remove filler, stacked clauses, and redundant detail.

### Core Decision Branches

- **Single clear area changed** -> include scope.
- **Cross-cutting repo change** -> omit scope or use the tightest shared scope.
- **Docs-only / rules-only** -> prefer `docs(...)`.
- **Structural rewrite without net-new behavior** -> prefer `refactor(...)`.

### Top 3 Gotchas

1. Listing everything the diff touched instead of the main delta.
2. Writing title case, sentence case, or trailing punctuation.
3. Using vague verbs like "update", "improve", or "change" when a sharper verb exists.

### Outcome Contract

When this skill is used, return:

1. `Best:` one primary commit subject
2. `Why:` one short line naming the chosen main delta
3. `Alt:` up to 2 alternates only if the diff is genuinely ambiguous

## Style Rules

- Shape: `type(scope): summary`
- Case: lowercase
- Mood: imperative
- Length: compact; target one line
- Focus: one change theme
- No trailing period

Default types:

- `feat`
- `fix`
- `refactor`
- `docs`
- `chore`
- `test`
- `perf`
- `build`
- `ci`
- `init`

## References

- [references/style.md](references/style.md)
