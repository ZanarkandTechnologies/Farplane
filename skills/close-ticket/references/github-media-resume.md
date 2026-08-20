---
title: Authenticated GitHub media resume
consumer_scope: close-ticket
---

# Authenticated GitHub Media Resume

Use this only after `farplane ticket finalize TASK-XXXX --media ...` creates or resumes the issue and returns a missing-media blocker with its URL.

For each missing original file:

1. Compute its lowercase SHA-256 and use exactly `<!-- farplane-ticket-media:TASK-XXXX:<sha256> -->`.
2. Read current comments with `gh issue view`. One exact marker means reuse that comment; more than one blocks; zero means upload once.
3. Open Core's exact issue URL in the operator's authenticated GitHub browser session. Confirm the configured repository and a signed-in comment composer.
4. Use the semantic attachment control to upload the file. Wait until the composer contains a real `https://github.com/user-attachments/...` URL.
5. Add a short `Demo` or `Screenshot` label plus the exact digest marker without replacing the attachment Markdown, then submit once.
6. Re-read comments with `gh` and require one marker, one attachment URL, and one canonical comment URL. Open that fragment and require the image or playable video to render.
7. Repeat only for the next missing digest, then rerun the identical finalize command.

If the browser is signed out or upload fails, leave the issue open and packet intact. Return the issue URL and next missing digest. Never create/close the issue, post a local path, commit the binary, create a Release, call a guessed upload API, or expose browser credentials/state.
