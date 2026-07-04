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

- [ ] The user explicitly asked for a phone call, chaser, reminder call, or
  test call in this turn or the active task context.
- [ ] The recipient is Kenji or an explicitly approved test number; do not call
  third parties, customers, public numbers, or guessed contacts.
- [ ] The message is short, non-sensitive, and asks for one concrete action.
- [ ] The payload and response shown in chat omit secrets, SIP credentials, API
  keys, and live phone numbers unless the user already wrote the same number in
  the current public context and it is necessary for debugging.
- [ ] The finish report says whether dispatch was created, skipped, or blocked,
  and includes a sanitized dispatch id/room when available.
