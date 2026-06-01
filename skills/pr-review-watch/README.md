# PR Review Watch

Explicit PR watcher workflow for already-open GitHub pull requests.

## Entry Points

- `SKILL.md`: operational workflow, guardrails, and outcome contract.
- `todos.md`: first-load checklist source.
- `templates/pr-review-pipeline.md`: project-local review memory template.
- `templates/codex-automation-prompt.md`: visible heartbeat prompt template.
- `fixtures/*.json`: deterministic PR state samples for the helper tests.

## Minimal Example

```bash
python3 bin/pr_review_watch.py classify \
  --fixture skills/pr-review-watch/fixtures/clean-pass.json \
  --config skills/pr-review-watch/fixtures/pipeline-config.md \
  --json
```

## Test

```bash
python3 bin/test_pr_review_watch.py
```
