# Close Ticket

## Purpose

Provide the operator-facing contract for Farplane's canonical closeout surface:
`$close-ticket`. It turns a proven ticket into one glanceable issue in the
project repository from `integrations.github.repo`, places the reviewed feature
demo first for material feature work, verifies every attachment, closes the
issue, then lets Core mine, index, and delete the exact local packet.

## Public API / Entrypoints

- `SKILL.md`: main close-ticket workflow and guardrails
- `SKILL.md` Todo List: ordered parent-skill todo list
- `README.md`: module summary and test checklist
- `AGENTS.md`: maintenance notes

## Minimal Example

1. Start the prompt with `$close-ticket TASK-00XX`.
2. Update ticket/docs evidence and pass QA plus independent review.
3. For material feature work, run `$demo` and select its reviewed `final.mp4`
   first; select supporting screenshots only when useful.
4. Render the concise `Before`, `After`, `Example`, `Key decisions`, and
   `Proof` issue in the configured project repository.
5. Use `gh` for issue creation, body updates, reads, and completed close state;
   treat browser sign-in as a separate gate from `gh auth`.
6. Upload one marked attachment comment per selected media file through
   GitHub's authenticated web composer, demo first. Wait for the real
   `github.com/user-attachments` URL; `gh issue comment --body-file` cannot
   upload a local binary.
7. Verify each marker and attachment URL with `gh`, open the comment fragment
   to prove GitHub renders the image/video, and link the first demo comment from
   the issue's `Proof` section.
8. Close as completed, then run `farplane ticket close` so Core verifies,
   mines, indexes, and deletes safely.

## How to Test

- Run `python3 -m unittest bin.tests.test_farplane_ticket_close`.
- Confirm material feature work blocks before GitHub mutation without a passing
  reviewed demo, while maintenance-only work does not invent one.
- Confirm Core rejects marker-only media comments and retains the local packet.
- Confirm a signed-out composer preserves the open issue, packet, and next
  digest; after sign-in the retry resumes that issue and uploads once.
- Confirm `gh` is never presented as a binary attachment uploader and no
  repository commit, Release, or private upload endpoint is used as fallback.
- Confirm exact configured-repository identity, no Releases or secondary repo,
  concise issue headings, attachment verification, and retry-safe cleanup.
