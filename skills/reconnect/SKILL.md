---
name: reconnect
description: "Use for \"reconnect my threads\", \"put my threads on my phone\" or \"turn on Remote Control everywhere\": every live Claude app thread on Remote Control, with a connected / not connected / excluded receipt."
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.9"
allowed-tools: Read, Bash
---

# Reconnect

## Context

Use this when Kenji is about to leave the Mac (travel, a meeting, the laptop
closing) or after the app restarted, and he wants to follow and steer his
threads from the Claude phone app or claude.ai/code. It turns on Remote Control
for every thread that can take it and says plainly which ones could not and
why. It only flips the Remote Control switch: it never sends a thread a
message, never archives, renames or moves threads (sidebar layout is
`goal-sections`), and never turns Remote Control off.

## Skill Signature

```text
reconnect(request, include_idle_wake?: false) -> remote-control receipt
reads: thread list (ccd_session_mgmt), the "connect new sessions" app setting (ccd_settings)
does: turns Remote Control on for every eligible thread, then re-reads the list
writes: each thread's Remote Control switch; the auto-connect setting only on Kenji's yes
returns: counts from the re-read list, threads not connected with the reason, what Kenji must do
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — List the threads and sort them by what the switch allows.**
  `list_sessions -> already on | to turn on | excluded`

  Rule: Load in one ToolSearch call:
  `select:mcp__ccd_session_mgmt__list_sessions,mcp__ccd_session_mgmt__set_remote_control,mcp__ccd_settings__get_settings,mcp__ccd_settings__set_setting`.
  Call `list_sessions` with `limit` 150; drop archived rows. `remoteControlActive:
  true` is already on. Exclude, without calling the tool, the scheduled and
  unattended runs (titles of scheduled tasks such as `Farplane · Thread
  Sweeper`, `Farplane · Morning`, `Burn before reset`): the app refuses them.
  Everything else with `remoteControlActive: false` goes to "to turn on", this
  thread included (`session_id: "self"`).

  Example: 31 threads -> 24 already on, 3 to turn on, 4 scheduled runs excluded.

  Assert:
  - Every non-archived thread is in exactly one of the three groups.

- [ ] **N2 — Turn the switch on, one call per thread.**
  `to turn on -> on | connecting | unavailable | refused`

  Rule: Call `set_remote_control` with `enabled: true` for each thread in
  "to turn on", newest first, and record the state it returns. "on" and
  "connecting" count as connected. A refusal is final for this pass: do not
  retry it and never send the thread a message to wake it. "Remote Control
  requires an active session. Send a message first." means the thread's process
  is not running (idle since the last app restart); once the newest idle threads
  get it, older idle ones will too, so list them under the same reason instead
  of calling each. Other refusals: started from another device, never ran a turn.

  Assert:
  - Each call's returned state is recorded; no call ever passes `enabled: false`.

- [ ] **N3 — Offer the wake-up for idle threads instead of doing it.**
  `unavailable threads -> listed with their risk | woken on Kenji's yes`

  Rule: An idle thread connects once it runs a turn, but any message makes it
  act on its own task. List each such thread with what its next action would
  touch (a robot run, a paid pod, a post, a push). Wake one only when Kenji
  says yes in chat, and then with a message that says only "Remote Control
  check: reply 'ok' and do nothing else."

  Example: `"Lehome robot cloth folding"` idle 5 days -> listed as "could restart
  robot work", left alone.

  Assert:
  - No thread was messaged without a yes from Kenji in this conversation.

- [ ] **N4 — Check the auto-connect setting.**
  `get_settings -> on | off -> offer`

  Rule: Read `connect_new_sessions_to_remote_control` from `get_settings`. When
  it is true, say so in one line. When it is false, offer to turn it on with
  `set_setting` (the app asks Kenji to approve), because new threads would
  otherwise start off-phone.

  Assert:
  - The receipt states the setting's value as read, not as assumed.

- [ ] **N5 — Re-read the list and report from it.**
  `list_sessions again -> receipt`

  Rule: Report the counts from the second `list_sessions` call, not the counts
  planned. Lead with the overall state and the one thing Kenji must do; link
  each thread named as `[title](#local_<id>)`.

  Assert:
  - The connected count equals the threads with `remoteControlActive: true` in the re-read.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Sending "continue" to idle threads so they connect also restarts their work:
  a robot run, a paid GPU pod or a post can start while Kenji is away.
- Calling the switch on a scheduled run just returns a refusal; it does not
  mean Remote Control is broken.
- Counting a thread as connected from the tool's "on" alone can be wrong after a
  restart; the re-read list is the proof.

## Output

One line with the overall state (for example "28 of 32 threads are on your
phone"), then three short lists: connected now (new ones named), not connected
with the reason and what would fix it, excluded scheduled runs. End with the
auto-connect setting's value and the undo path: the Remote Control switch in
each thread's toolbar.
