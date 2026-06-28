# Stage Matrix

Use this when you need the stage defaults quickly.

| Stage | Default command shape | Best use | Notes |
| --- | --- | --- | --- |
| `pre-commit` | `coderabbit review --plain --type uncommitted` | risky local changes before commit | opt-in only; not the normal default |
| `pre-push` | `coderabbit review --plain --type committed --base <default-branch>` | heavy gate before push | preferred default |
| `pr` | `coderabbit review --plain --type committed --base <default-branch>` | final PR-ready review pass | same technical shape as `pre-push`, different intent |
| agent loop | `coderabbit review --agent --type committed --base <default-branch>` | Codex reads findings and fixes them | use raw CLI or pass `--output agent` to the helper |

## Guidance

- If the branch is still noisy, clean the scope before running the heavy pass.
- If the review is timing out in practice, shrink the diff before inventing more
  automation.
- If you need exact branch defaults, the repo helper auto-detects the default
  base branch when possible and falls back to `main`.
