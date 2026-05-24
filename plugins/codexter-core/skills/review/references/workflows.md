# Workflows

## Standard Review

1. Read the active ticket.
2. Open `review-rubric-index.md`.
3. Choose rubric families.
4. Load matching family references.
5. Inspect changed files, evidence, and relevant neighboring surfaces.
6. Score on the anchored `1.0`-to-`5.0` scale.
7. Write the review artifact and link it from ticket evidence.

## Frontend Review

1. Include `ui-quality` for visible product quality.
2. Include `frontend-guidelines` when UI source files changed.
3. Run `web-design-guidelines` on the changed UI files.
4. Include `visual-qa` evidence when rendered UI proof is in scope.
5. Compare `ui-quality` and `frontend-guidelines` scores for alignment.

## Completion Review

1. Verify evidence and integration readiness first.
2. Apply user-intent satisfaction when the ticket expresses a user-facing ask.
3. Return pass only when required rubrics meet threshold and hard gates pass.
