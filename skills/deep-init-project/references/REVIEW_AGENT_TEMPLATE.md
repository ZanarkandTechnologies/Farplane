---
title: Codex Review Agent Loop
status: active
owner: project
updated: YYYY-MM-DD
---

# Codex Review Agent Loop

This repo uses deterministic checks first and a Codex SDK reviewer second. The
reviewer is a second pair of eyes for maintainability drift, modularity,
cross-commit consolidation, risky commits, and missed proof. It runs during
local pre-push by default as an advisory check.

## Relationship To Farplane Reviewers

- Reusable local diff-review contract:
  `~/.codex/skills/code-review/SKILL.md`.
- Canonical material review: installed Farplane reviewer lane at
  `~/.codex/agents/reviewer.toml` plus `~/.codex/skills/review/SKILL.md`.
- Local pre-push review: `scripts/codex_review_agent.ts`, which reviews check
  logs and git diff using the `code-review` skill. It is lighter-weight and
  does not issue TAS verdicts.
- `install.sh` from the Farplane repo links skills, canonical reviewer agents,
  and review rubrics into `~/.codex`; keep those installed before relying on
  this loop.

## Commands

- `bash scripts/pre_push_check.sh`: runs deterministic gates, then advisory
  Codex agent review.
- `bash scripts/collect_review_context.sh .farplane/reviews/latest/context.md`:
  writes a review packet.
- `bash scripts/run_pre_push_review.sh`: runs the pre-push reviewer directly.

If this project uses `package.json`, add these scripts:

```json
{
  "scripts": {
    "review:agent": "tsx scripts/codex_review_agent.ts",
    "review:prepush": "bash scripts/run_pre_push_review.sh"
  },
  "devDependencies": {
    "@openai/codex-sdk": "latest",
    "tsx": "latest"
  }
}
```

For non-Node projects, either keep the script skipped until a JS toolchain is
available or replace `CODEX_REVIEW_CMD` in `scripts/pre_push_check.sh` with a
project-native wrapper.

## Environment

- `FARPLANE_SKIP_AGENT_REVIEW=1`: skip advisory agent review during pre-push.
- `STRICT_AGENT_REVIEW=1`: make agent review required during pre-push.
- `CODEX_REVIEW_MODEL=<model>`: override the Codex SDK model.
- `CODEX_REVIEW_TIMEOUT_MS=<ms>`: abort the review turn after a timeout.
- `CODEX_REVIEW_SKILL_FILE=<path>`: override the code-review skill file.
- `CODEX_REVIEW_REACT_GUIDE_FILE=<path>`: override the React/frontend
  guideline skill file. Defaults to
  `~/.codex/skills/vercel-react-best-practices/SKILL.md`.
- `FARPLANE_REVIEW_DIFF_LINES=<n>`: change the diff line cap in review context.
- `FARPLANE_REVIEW_UNTRACKED_LINES=<n>`: change the per-file cap for untracked
  text files in review context.
- `FARPLANE_REVIEW_INCLUDE_UNTRACKED=1`: include untracked text file contents in
  the review prompt. Leave this off unless those files are intentional review
  inputs.
- `FARPLANE_PRE_PUSH_REVIEW_DIR=<path>`: write pre-push artifacts under a custom
  path. The path must resolve under `.farplane/reviews/`.

## Output

Pre-push writes artifacts to `.farplane/reviews/pre-push-latest/`:

- `context.md`: deterministic checks, changed files, commits, and truncated diffs.
- `context.md` also includes project maintainability standards and nearby
  module README/AGENTS files for changed paths when available.
- `review.prompt.md`: exact prompt sent to Codex.
- `review.json`: structured review output.
- `review.md`: human-readable summary.

`.farplane/reviews/` is ignored because it can contain local diffs, private
paths, and check logs. Untracked file names are listed, but untracked file
contents are omitted unless explicitly enabled.

The reviewer process uses an allowlisted environment instead of inheriting the
full shell environment.
