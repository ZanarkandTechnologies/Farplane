---
name: notify
description: "Use for \"message me\", \"ping me on Telegram\", \"send this for review\" or \"call me about this\": one phone-readable Telegram message or a bounded reminder call to Kenji, with a delivery receipt."
source: local
department: operations
capability:
  kind: integration
template_uses:
  skill-template: "0.6.6"
  skill-eval-task: "0.2.0"
allowed-tools: Bash, Read
---

# Notify

## Context

Use this when a workflow needs Kenji's attention away from the desk: a feedback
request, an automation status, a blocker, an artifact ready for review, or a
reminder call. Callers (the `goal-advisor` human-feedback preset, `ads`, `pm`
hygiene, `commit` PR watch) write the request; this skill delivers it on one
channel and returns a receipt.

Channels: `telegram` (default) sends through the bunker's Telegram gateway,
which stores a reply route so Kenji's answer returns to the source thread.
`call` dispatches the LiveKit phone agent whose worker lives in
`/Users/kenjipcx/Zanarkand Technologies/projects/Farplane-UI-v2/apps/phone-chaser`
(resolved through `farplane ui link`).

Recipients are Kenji, or for calls an approved internal or explicit test
number. Never prospects, customers, public channels, or unknown recipients.
Notifying Kenji grants no authority to publish, spend, deploy, or message
anyone else. Never write tokens, phone numbers, or SIP credentials into a file,
log, or chat.

## Skill Signature

```text
notify(intent: feedback_request | automation_status | blocker | artifact_ready | review_request | reminder,
       channel?: telegram | call, body?, original_source_url?, media_paths?, thread_id?, policy_receipt?)
  -> sent_message | dispatch_receipt | fallback_report
reads: caller artifact, CODEX_THREAD_ID or caller thread id, runtime env or private config
does: writes a phone-readable body or a short call script, sends through the gateway or LiveKit
writes: nothing tracked; the gateway persists the reply route
returns: message id + delivery kind + route, or dispatch id + room, or the exact fallback reason
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind channel, recipient, and what Kenji can see on a phone.**
  `request -> channel + recipient + view_mode | fallback_report`

  Rule: `channel := call` only on an explicit call request or a policy receipt;
  otherwise `telegram`. `view_mode := inline_summary | phone_openable_link |
  fallback_only`. Every Telegram message carries a labeled phone-openable
  original (task, brief, or source page); a local filesystem path alone is not
  reviewable, so include the deciding excerpt or report a fallback.

  Assert:
  - Recipient is Kenji or an approved internal/test number with a reason.
- [ ] **N2 — telegram: write a body Kenji can decide from inside Telegram.**
  `request + artifacts -> body + attachments + one reply action`

  Rule: Lead with the plain-language product, decision, result, or blocker;
  a ticket id never carries the context. For a decision, describe each real
  option as a concrete workflow, say what is at stake, and give one honest
  recommendation. For a blocker or reminder: stakes, exact blocker, why his
  judgment is needed, action, deadline, and what happens if it passes; no
  forced A/B for open judgment. A visual review (storyboard, design, frame)
  attaches a PNG/JPEG; prose or a link never replaces it. End with
  `*Original:* <url>` and one reply action answerable in one message.
  Calibrate with [templates](references/telegram-templates.md).

  Example: `"TASK-0412 ready"` -> `"*Review the redesigned onboarding flow* ...
  {attach_photo} ... *Original:* <url> ... *Reply with:* approve, or revise + what felt unclear."`

  Assert:
  - No giant report dump, no mechanical approval/deploy boilerplate, no secrets.
- [ ] **N3 — telegram: send through the gateway and claim only a receipt.**
  `body + thread_id -> sent_message | fallback_report`

  Rule: Resolve `thread_id := caller thread || CODEX_THREAD_ID`; with no route
  target, do not send a replyable message. Send with
  `scripts/send_message.py` (gateway by default, so the route row persists);
  `--photo` for visuals, `--parse-mode Markdown` for simple controlled text,
  `none` for raw excerpts. Say `sent` or `delivered` only after the gateway
  returns a message id and delivery kind. Missing credentials: see
  [configuration](references/telegram-configuration.md), keep the local
  artifact, and report the fallback.

  Assert:
  - A drafted body, named file, or intended command is never reported as sent.
- [ ] **N4 — call: check the policy, then dispatch one bounded call.**
  `call request -> dispatch_receipt | dry-run payload | blocked_report`

  Rule: Require explicit call intent or a policy receipt (ticket, Review block,
  due threshold, active hours, prior Telegram reminders, repeat interval,
  remaining cap). Keep the script short: who, one reason, one action. Run
  `scripts/dispatch_call.py --message ...` (`--dry-run` to validate; pass
  `--phone-number` only for an approved override). Review callbacks use a
  gateway-minted scoped `review_id` bound to one source thread and review
  cycle; never Codex app-server credentials or arbitrary thread choice. Setup,
  trunks, review-call compile, and deployment: [call setup](references/call-setup.md).

  Example: `"Kenji. This is Farplane. The ad campaign packet is waiting. Your one
  action is approve, revise, or reject. Say it now or reply in Telegram."`

  Assert:
  - No repeated test calls without spacing and a clear label.
- [ ] **N5 — Return the receipt.**
  `send or dispatch result -> receipt`

  Rule: Report sent, skipped, or blocked and why. Include message id and
  delivery kind, or dispatch id and room; never phone numbers, keys, or SIP
  credentials. When a call or webhook fails, the Telegram reply route is the
  fallback rather than broader phone authority.

  Assert:
  - The receipt matches what the gateway or LiveKit actually returned.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- `tickets/TASK-0240/artifacts/foo.md` is not phone-viewable.
- Telegram Markdown is not GitHub Markdown: `*bold*`, `_italic_`, short bullets.
  Code, JSON, dense paths, or underscore-heavy text go with `--parse-mode none`.
- Never bypass the gateway with raw Telegram API sends for replyable messages:
  without a route row, Kenji's reply cannot reach the source thread.
- The LiveKit-rented number can be inbound-only; outbound needs the SIP trunk.
- A review queue or stale ticket is not a policy receipt for a call.
- This is not a robocall or outreach tool.

## Reference Map

- [telegram templates](references/telegram-templates.md) - N2/N3: decision,
  artifact-ready, and blocker calibration plus send commands.
- [telegram configuration](references/telegram-configuration.md) - N3 when
  credentials are missing.
- [call setup](references/call-setup.md) - N4 for setup, providers, deployment,
  and review-call compile and gateway binding.

## Output

```yaml
channel: telegram | call
result: sent_message | dispatch_receipt | fallback_report
receipt: <message id + delivery kind + reply route> | <dispatch id + room + agent> | none
reason: <why sent, skipped, or blocked>
```
