---
title: Phone Chaser QA Checklist
owner: phone-chaser
status: active
kind: qa-checklist
---

# Phone Chaser QA Checklist

Use before dispatching a call and again before reporting completion.

```text
phone_chaser_check(request, payload, env_state) -> pass | block | dry_run_only
```

## Checklist

- [ ] The user explicitly asked for a phone call/chaser/test call, or Work
  Pulse supplied an operator-approved structured escalation receipt with the
  due threshold, active-hours pass, prior Telegram count, repeat interval, and
  remaining cap.
- [ ] The recipient is Kenji, a named internal organization recipient, or an
  explicitly approved test number with a legitimate reminder/escalation purpose;
  do not call prospects, customers, public numbers, unknown recipients, or
  guessed contacts.
- [ ] The message is short, non-sensitive, and asks for one concrete action.
- [ ] Artifact review calls include bounded context from the ticket, Review or
  Done block, and relevant artifact/evidence summaries so the recipient can
  answer without reconstructing the work from memory.
- [ ] Any spoken review callback uses only a gateway-minted one-review
  `review_id`/capability and never exposes Codex app-server credentials,
  arbitrary thread ids, publish/outreach/account/spend/deploy authority, or
  broad tools to the phone runtime.
- [ ] The payload and response shown in chat omit secrets, SIP credentials, API
  keys, and live phone numbers unless the user already wrote the same number in
  the current public context and it is necessary for debugging.
- [ ] If the review webhook is unavailable, Telegram reply routing remains the
  fallback path; do not widen the phone agent's authority to compensate.
- [ ] The finish report says whether dispatch was created, skipped, or blocked,
  and includes a sanitized dispatch id/room when available.
