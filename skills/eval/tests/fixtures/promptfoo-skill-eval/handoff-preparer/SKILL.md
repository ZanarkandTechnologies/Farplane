---
name: handoff-preparer
description: Prepare a concise project handoff from a local brief when the user asks for a handoff or status-transfer artifact.
---

# Handoff Preparer

Read the named local brief before drafting the handoff.

Create `handoff.txt` in the working directory with exactly these five lines:

1. `Status: ready`
2. `Marker: <the marker from the brief>`
3. `Owner: <the owner from the brief>`
4. `Next: <the next action from the brief>`
5. `Protocol: QUARTZ-LANTERN`

In the final response, include one line containing `HANDOFF_READY:`, the marker,
the path `handoff.txt`, and the protocol token `QUARTZ-LANTERN`. Do not add a
skill-specific heading or explanation; higher-priority harness framing may
remain around the line.
