---
name: close-ticket
description: "Turn a completed ticket into a glanceable GitHub issue, demo-first feature proof, safe Core cleanup, and durable closeout."
tier: 3
group: operations
source: local
template_uses:
  skill-eval-task: "0.2.0"
---

# Close Ticket

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

1. Resolve one active ticket and assert implementation, proof, and required review are complete.
2. Read the first-load Todo List guardrails before any remote mutation.
3. Update ticket evidence, durable docs, handoff, next action, and latest verification.
4. Run `farplane ticket check <ticket.md> --phase complete` with an explicit changed-path boundary.
5. Refresh independent review when closeout changes made the prior receipt stale.
6. Derive a compact repo-style commit subject from the intended slice, commit only that slice, and push only when explicitly authorized.
7. Select media explicitly. Material features require the passing reviewed `$demo` `final.mp4` first; maintenance tickets invent no demo.
8. Run `farplane ticket finalize TASK-XXXX` with one `--media <path>` per selected file.
9. If Core pauses on missing media, upload only those marked comments through the authenticated GitHub composer, then rerun the same command.
10. Assert Core verified and closed the issue as completed, mined and indexed it, and deleted the exact local packet.
11. Reapply the first-load Todo List guardrails and return the issue URL, media comment URLs, receipt outcome, and packet state.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when one coding ticket is genuinely complete and only durable closeout remains.

## Skill Signature

```text
close_ticket(ticket_id, selected_media[], browser_profile?)
  -> verified_closed_issue + media_comment_urls[] + local_close_receipt

reads:
  tickets/TASK-XXXX/**
  farplane/bindings.yaml#integrations.github.repo
does:
  validate final local truth
  call Core to render, create or resume, verify, close, mine, index, and delete
  upload missing selected media through the authenticated browser when required
writes:
  one Core-owned marked GitHub issue
  zero or one marked comment per selected media digest
  Core-owned locator, closure receipt, mining output, and packet deletion
returns:
  close_ticket_complete | continue_impl | blocked
```

## Contract

- Keep the ticket packet as the retry surface until Core reports `local_packet_deleted: true`.
- Core owns issue identity, rendering, create/resume, exact open-issue refresh, verification, completed close state, mining, indexing, and deletion.
- Never pass an issue URL to Core. Never create, edit, or close the issue outside Core.
- The only skill-owned remote mutation is authenticated upload of explicitly selected media after Core returns the open issue URL.
- Retry by ticket marker, media SHA-256 markers, receipt, and locator identity. Never create a replacement issue or manually delete/move the packet.
- A material feature cannot close without its passing reviewed demo MP4. A maintenance ticket may close without media.
- Do not push unless the user or owning workflow explicitly authorizes publication.

## Workflow

### 1. Prove local readiness

Read the ticket, program/progress when present, and linked evidence. Unchecked required work, stale material review, failed validation, or a missing required demo returns `continue_impl` or `blocked`.

Update durable docs only where final behavior changed. Run the phase-aware ticket validator with an explicit base/path boundary. Commit the intended slice before terminal cleanup so the ticket still exists if commit or validation fails.

### 2. Select media

Use only explicit original files. For feature work, the first item must be the independently reviewed `$demo` `final.mp4`; optional screenshots follow. Check current GitHub attachment limits and file digests before Core creates the issue.

### 3. Invoke Core

```text
farplane ticket finalize TASK-XXXX \
  --media <selected-path-1> \
  --media <selected-path-2>
```

Omit `--media` when none were selected. Core derives the repository from `integrations.github.repo`, exhaustively searches issue bodies for the literal ticket marker, and:

- creates one issue when no marker exists
- resumes and refreshes one stale open issue when exactly one marker exists
- blocks on duplicate markers or stale closed content
- leaves the issue open and returns its URL when selected media markers are missing
- verifies all body/media markers before closing with reason `completed`
- mines, writes the compact locator and receipt, then deletes only `tickets/TASK-XXXX`

### 4. Resume missing media

Follow [Authenticated media resume](references/github-media-resume.md). Upload one comment per missing digest through GitHub's authenticated web composer. A valid comment contains the exact marker and a real `github.com/user-attachments/...` URL. Rerun the identical finalize command; do not supply the issue URL.

### 5. Verify completion

Require the Core receipt to agree on ticket ID, issue URL/number, comment URLs, `remote_state: closed`, mining success, locator path, and `local_packet_deleted: true`. Any failure retains the packet and returns one exact resume point.

## Output

Report commit/push state, issue and media-comment URLs, Core receipt path and mining result, packet state, and the exact blocker/resume point when incomplete.

End with exactly:

`EXECUTION_RESULT: status=<close_ticket_complete|continue_impl|blocked> next=<done|documenting|none> reason=<optional>`
