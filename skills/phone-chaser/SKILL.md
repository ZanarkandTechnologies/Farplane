---
name: phone-chaser
description: "Turn an explicit reminder or escalation request into a bounded LiveKit phone call for Kenji or an approved internal/test recipient."
tier: 3
group: notifications
source: local
template_uses:
  skill-template: "0.3.7"
qa_checklist: qa_checklist.md
allowed-tools: Bash, Read
---

# Phone Chaser

## Context

Use this skill when the operator explicitly asks for a phone reminder, phone
chaser, call escalation, or test call through the Farplane LiveKit agent.

This skill owns the harness workflow and dispatch guardrails. The deployable
LiveKit worker lives at `../../farplane/phone-chaser/` and should stay there
unless the runtime is being changed.

Phone calls are external side effects. The default recipient is Kenji's
configured reminder number, but the operator may provide a recipient override
for a named internal organization recipient or explicit test number. Do not
place calls to prospects, customers, public numbers, unknown recipients, or any
recipient where the legitimate reminder relationship is unclear. Default
recipient and caller values must come from runtime env or private config; never
write live phone numbers, keys, or SIP credentials into tracked files.

## Skill Signature

```text
phone_chaser(call_request, state?) -> dispatch_receipt | blocked_report
state: reads(qa_checklist.md, references/setup.md when setup or deployment is
      needed, ../../farplane/phone-chaser/README.md for runtime details,
      runtime env/private config through scripts/dispatch_call.py)
      writes(no tracked files by default)
gates: explicit_user_call_intent; allowed_recipient; no_secrets; message_bound;
       livekit_cli_available; dispatch_created_or_blocker_recorded
routes: phone-chaser -> telegram-message only when phone call is blocked and a
        Telegram fallback was explicitly useful
fails: accidental repeated calls; unapproved external call; secret exposure;
       local-only path masquerading as phone proof
```

## Phase Boundary

Dispatch requests execute inline. Runtime setup, trunk repair, provider
selection, or deployment changes are material work and should be planned or
ticketed before editing the deployable agent.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the call request.
  - [ ] Confirm the request explicitly asks for a phone call, chaser, reminder
    call, or test call.
  - [ ] Resolve `phone_number`, `message`, `urgency`, and `agent_name` from
    user input, runtime env, or private config.
  - [ ] Confirm any `phone_number` override targets a named internal recipient
    or explicit test number with a legitimate reminder/escalation purpose.
  - [ ] Keep the reminder short enough for a phone call.
- [ ] 2. Read guardrails.
  - [ ] Read `qa_checklist.md` before dispatch.
  - [ ] Read `references/setup.md` only when setup, deployment, trunks, model
    choices, or credentials are in scope.
- [ ] 3. Decide the branch.
  - [ ] 1. Dispatch branch: call an allowed recipient through the existing
    deployed agent.
  - [ ] 2. Dry-run branch: validate the metadata payload without placing a
    call.
  - [ ] 3. Setup/repair branch: update private config, LiveKit/Telnyx/Fish
    setup, or the deployable runtime.
- [ ] 4. Execute the selected branch.
  - [ ] For dispatch, run `scripts/dispatch_call.py --message ...` and pass
    `--phone-number` only when the user supplied or approved an override.
  - [ ] For dry-run, run the same script with `--dry-run`.
  - [ ] For setup/repair, keep tracked runtime edits in
    `../../farplane/phone-chaser/` and private values in local config/env.
- [ ] 5. Finish gate.
  - [ ] Apply `qa_checklist.md` again.
  - [ ] Report whether a LiveKit dispatch was created, skipped, or blocked.
  - [ ] Include dispatch id/room when available; do not include phone numbers,
    keys, SIP credentials, or provider secrets.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Short reminder shape:

```text
{Recipient}. This is Farplane for Kenji. {one concrete reason}. Your one action
is {approve/revise/reject/open Codex/reply received}. Say it now or reply in
Codex.
```

Dispatch command:

```bash
python3 skills/phone-chaser/scripts/dispatch_call.py \
  --message "Kenji. Review the waiting Farplane decision. Reply approve, revise, or reject." \
  --urgency high
```

Dry run:

```bash
python3 skills/phone-chaser/scripts/dispatch_call.py \
  --message "Kenji. Dry-run reminder." \
  --dry-run
```

## Gotchas

- The LiveKit-rented phone number can be inbound-only; outbound calls require
  the configured SIP trunk and allowed caller number.
- Do not use this skill as a general robocall or cold outreach tool. Its scope
  is bounded reminder/escalation calls to Kenji, named internal recipients, and
  explicit test numbers.
- Fish Audio is only the voice. Talkback also depends on LiveKit STT/LLM
  configuration inside the deployed runtime.
- Repeated dispatch tests can ring the phone multiple times. Space tests out
  and name them clearly in the message.

## Reference Map

- `references/setup.md` - read when changing LiveKit, Telnyx, Fish Audio,
  deployment, model choices, or local/private configuration.

## Output

- `dispatch_receipt`: LiveKit dispatch id, room, agent name, urgency, and
  sanitized message summary.
- `blocked_report`: exact missing setup, safety gate, or command failure.
