# Workflows

## Spec Research

1. Write the prompt and command metadata under `.farplane/external-cli/runs/<run-id>`.
2. Name one first-write planning artifact.
3. Mount `landing-page`, `best-of-worlds`, `brainstorm`, and visual/review
   support skills.
4. Forbid `qa/**`, prior session JSONL, screenshots, videos, and frame folders
   unless the phase is visual review.
5. Require a concise handoff before optional deep dives.

## Implementation

1. Validate the approved spec locally before delegation.
2. Name owned source files and the first-write target.
3. Mount frontend, media, QA, and review skills needed for the phase.
4. Run Pi/Kimi with the prompt file.
5. Read the handoff and decide keep, repair, or reject.
6. Run Farplane-owned verification before any completion claim.

## Visual Review

1. Provide the URL or local HTML path and expected UI spec.
2. Permit reading screenshots and QA artifacts.
3. Require findings, screenshots, browser/debug outputs, and recommended repair
   prompt.
# Delegate Frontend Workflows

## Ready Frontend Ticket

1. Read the ticket.
2. Confirm UX and visual direction are explicit.
3. Run `delegate-cli` with `frontend-pi-kimi`.
4. Attach artifacts.
5. Run QA, visual QA, and review.

## Unclear Frontend Ticket

Use `frontend-craft`, `functional-ui`, `visual-design`, or `landing-page`
before delegating implementation.
