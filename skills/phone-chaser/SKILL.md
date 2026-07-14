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
chaser, call escalation, or test call through the Farplane LiveKit agent, or
when Work Pulse selects a due review escalation from the operator-approved
structured chase policy in `farplane/bindings.yaml`.

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
      runtime env/private config through scripts/dispatch_call.py, ticket.md
      and artifacts through scripts/compile_review_call.py for review calls)
      writes(no tracked files by default)
gates: explicit_user_call_intent_or_policy_receipt; allowed_recipient; no_secrets; message_bound;
       scoped_review_callback_when_used; livekit_cli_available; dispatch_created_or_blocker_recorded
routes: phone-chaser -> telegram-message only when phone call is blocked and a
        Telegram fallback was explicitly useful; spoken review response ->
        Farplane-UI Telegram gateway review relay when a review_id capability
        was minted for exactly one source thread and review cycle
fails: accidental repeated calls; unapproved external call; secret exposure;
       local-only path masquerading as phone proof; app-server credentials or
       arbitrary thread ids reaching the phone runtime
```

## Phase Boundary

Dispatch requests execute inline. Runtime setup, trunk repair, provider
selection, or deployment changes are material work and should be planned or
ticketed before editing the deployable agent.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the call request.
  - [ ] Confirm either explicit user call intent or a Pulse policy receipt that
    identifies the ticket, Review block, due turn threshold, active-hours pass,
    prior Telegram reminders, repeat interval, and remaining call cap.
  - [ ] Resolve `phone_number`, `message`, `urgency`, and `agent_name` from
    user input, runtime env, or private config.
  - [ ] Confirm any `phone_number` override targets a named internal recipient
    or explicit test number with a legitimate reminder/escalation purpose.
  - [ ] Keep the reminder short enough for a phone call.
  - [ ] For artifact review calls, compile bounded context from `ticket.md`,
    the Review/Done block, and relevant artifact/evidence summaries: title,
    objective, produced artifact, why it matters, decision question, approve
    effect, revision examples, and limits.
  - [ ] For artifact review callbacks, use a gateway-minted opaque
    `review_id`/capability bound to one source thread and review cycle; never
    send Codex app-server credentials or arbitrary thread selection to the
    phone runtime.
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
  - [ ] For review calls, create the gateway binding, compile metadata with
    `scripts/compile_review_call.py`, then dispatch with
    `scripts/dispatch_call.py --metadata-file <metadata.json>`.
  - [ ] For setup/repair, keep tracked runtime edits in
    `../../farplane/phone-chaser/` and private values in local config/env.
- [ ] 5. Finish gate.
  - [ ] Apply `qa_checklist.md` again.
  - [ ] Report whether a LiveKit dispatch was created, skipped, or blocked.
  - [ ] Include dispatch id/room when available; do not include phone numbers,
    keys, SIP credentials, or provider secrets.
  - [ ] If webhook delivery is unavailable, confirm the existing Telegram reply
    route remains the fallback rather than broadening phone runtime authority.
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

Review-call metadata dry run:

```bash
python3 skills/phone-chaser/scripts/compile_review_call.py \
  --ticket tickets/TASK-0351/ticket.md \
  --artifact tickets/TASK-0351/artifacts/farplane-ui-activation-case-study.md \
  --dry-run
```

Gateway binding and relay shape:

```bash
# In Farplane-UI:
npm run cli -- gateway telegram review-bind --thread-id <source-thread-id> --title "TASK-0351 review"
npm run cli -- gateway telegram review-relay --port 8789
```

Temporary tunnel examples, without committing secrets or exposing Codex
app-server directly:

```bash
ngrok http http://127.0.0.1:8789
cloudflared tunnel --url http://127.0.0.1:8789
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
- A review queue or stale ticket is not a policy receipt. Calls require the
  exact configured per-review escalation threshold and cap.
- Review webhook callbacks belong to the Farplane-UI gateway. The phone runtime
  gets only the review-specific capability and relay URL; it does not get
  Codex app-server credentials or permission to choose a thread.

## Reference Map

- `references/setup.md` - read when changing LiveKit, Telnyx, Fish Audio,
  deployment, model choices, or local/private configuration.

## Output

- `dispatch_receipt`: LiveKit dispatch id, room, agent name, urgency, and
  sanitized message summary.
- `blocked_report`: exact missing setup, safety gate, or command failure.
