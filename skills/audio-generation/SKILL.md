---
name: audio-generation
description: "Turn approved voice, music, or SFX briefs into provider-resolved generation packets, audio artifacts, and sanitized execution receipts."
tier: 3
group: content-audio
source: local
template_uses:
  skill-template: "0.3.8"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["audio-advisor", "content-impl-plan"]
allowed-tools: Read, Grep, Glob, Bash
---

# Audio Generation

## Context

Use this skill after voice, music, or sound-effect direction is approved and a
caller needs a provider-ready packet or generated audio. Methods are
`audio-generation:voice`, `audio-generation:music`, and
`audio-generation:sfx`.

This skill owns capability routing, provider parameters, artifact paths,
generation metadata, and sanitized receipts. `audio-advisor` owns creative
direction, cue timing, rights, voice consent, and mix notes; `remotion` owns
timeline placement and render proof. Upstream provider skills and docs are
implementation references, not required live dependencies.

## Skill Signature

```text
audio_generation(kind, brief, profile?, provider?, output_owner?)
  -> generation_packet | execution_receipt | blocked_report

state:
  reads(config.toml, approved audio brief, voice consent/rights evidence,
        selected provider reference, qa_checklist.md, runtime secret readiness?)
  writes(generation packet, optional generated audio artifact, sanitized receipt)

gates:
  kind_supported; provider_capability_matches; brief_approved;
  voice_consent_resolved_when_relevant; output_owner_resolved;
  explicit_external_execution_authority; runtime_secret_ready_for_execution;
  receipt_contains_no_secret

routes:
  audio-advisor | audio-generation:voice | audio-generation:music |
  audio-generation:sfx | remotion | review

fails:
  unsupported_provider_kind_pair; implicit_spend_or_upload; secret_in_config;
  voice_without_consent; provider_call_without_runtime_secret;
  receipt_leaks_credential_or_raw_request_headers
```

Config precedence is `invocation > config.toml > explicit fallback in this
file`. Config selects safe defaults only. Credentials resolve separately from
the runtime environment, normally through `farplane run -- <command>` or
`doppler run -- <command>`; never write credential values into a packet,
artifact, receipt, or tracked file.

## Phase Boundary

Packet or dry-run planning is the default and has no external side effects.
Execute a provider call only when the current request explicitly authorizes the
upload, spend, and generation. A prior direction approval does not itself grant
provider-execution authority.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load safe defaults and bind the request.
  - [ ] Read `config.toml` before choosing a provider, model, format, or output
    path; invocation values override config values.
  - [ ] Bind `kind`, approved brief, optional profile/provider, output owner,
    desired duration/timing, and whether provider execution is explicitly
    authorized.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Validate the creative and rights handoff.
  - [ ] Require an approved voice/music/SFX brief with the timing and acceptance
    checks needed by the downstream cue sheet.
  - [ ] For voice, require a rights-safe library voice or explicit consent for
    a cloned, designed, reference, or real-person voice before execution.
- [ ] 3. Resolve capability and provider detail.
  - [ ] Use the capability matrix: Fish -> voice; ElevenLabs -> voice, music,
    SFX. Return `blocked_report` for every other provider/kind pair.
  - [ ] Read `references/fish-audio.md` only for Fish voice, or
    `references/elevenlabs.md` only for an ElevenLabs route.
- [ ] 4. Build the generation packet.
  - [ ] Include kind, provider, model/format parameters, prompt or script,
    voice/profile handle when rights-safe, duration/timing, output path,
    execution mode, acceptance checks, and downstream cue binding.
  - [ ] Store personal/private voice IDs only in the invocation or private
    runtime context; do not promote them into tracked config or examples.
- [ ] 5. Stop at dry run unless execution is authorized.
  - [ ] Without explicit upload/spend/generation authority, return the packet
    with `execution_mode: dry_run` and make no provider call.
  - [ ] For authorized execution, confirm the provider environment variable is
    present without printing it; if absent, return a missing-secret blocker.
- [ ] 6. Execute and record when authorized.
  - [ ] Run the provider route through the managed runtime environment, save the
    audio under the resolved output owner, and record observed duration/format.
  - [ ] For Fish voice packets, use
    `scripts/execute_fish_audio.py <packet.json> --receipt <receipt.json>`
    through `farplane run --`; keep any configured voice ID in private runtime
    context and require the executor to verify that it is a public trained voice.
  - [ ] For ElevenLabs voice or SFX packets, use
    `scripts/execute_elevenlabs.py <packet.json> --receipt <receipt.json>`
    through `farplane run --`; use `--dry-run` before the first paid call.
  - [ ] Write a sanitized receipt containing provider, capability, model,
    artifact path, request/trace ID when safe, metering metadata when returned,
    and acceptance result—never credentials or raw authorization headers.
- [ ] 7. Verify and hand off.
  - [ ] Reapply `qa_checklist.md`; validate JSON packets/receipts with
    `scripts/validate_audio_packet.py`, confirm the file opens, and confirm
    observed duration/format match the packet.
  - [ ] Route timing, ducking, captions, waveform treatment, and final mix to
    `remotion`; use independent review for material production runs.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```text
audio_generation_packet:
  kind: voice | music | sfx
  provider:
  capability:
  execution_mode: dry_run | authorized_execution
  brief_ref:
  prompt_or_script:
  profile_ref:
  parameters: {}
  timing: {duration_seconds, cue_ref}
  output: {owner, path, format}
  rights_and_consent:
  acceptance_checks: []
  secret_source: runtime_environment_only

blocked_report:
  result: blocked_report
  code: unsupported_provider_kind_pair | missing_runtime_secret |
    unresolved_voice_consent | missing_execution_authority |
    brief_not_approved | artifact_verification_failed
  kind: voice | music | sfx
  provider: fish | elevenlabs
  requested_capability: voice | music | sfx
  execution_mode: dry_run | authorized_execution
  brief_ref:
  reason:
  silent_provider_switch: false
  next_action:
  external_call_made: false | true (artifact_verification_failed only)
```

Unsupported-pair blockers require an unsupported provider/kind pair. Safety
blockers such as missing runtime secret or unresolved voice consent require a
supported pair and retain `external_call_made: false`. Artifact-verification
failure is the only blocker code that may follow a provider call; its receipt
must still be sanitized and report the observed side effect honestly.

For a complete positive fixture, read
`examples/explainer-audio-packet/example.md` only when shaping or reviewing a
packet that combines voice, music, and SFX.

## Gotchas

- A provider's upstream skill is an implementation aid, not a reason to bypass
  this skill's consent, spend, artifact, or receipt gates.
- A voice ID can be non-secret but still private or rights-sensitive; do not
  commit it merely because an API accepts it as a parameter.
- Do not call a music endpoint for a short transition hit when the SFX route
  better matches the cue, duration, and metering model.

## Reference Map

- `config.toml` - always read before provider/default selection; it contains
  non-secret shared defaults only.
- `qa_checklist.md` - read before execution and reapply before handoff.
- `references/fish-audio.md` - load only for Fish voice packet or execution.
- `references/elevenlabs.md` - load only for ElevenLabs voice, music, or SFX.
- `examples/explainer-audio-packet/example.md` - load only for a combined
  explainer-audio packet example or output-shape review.
- `scripts/validate_audio_packet.py` - validate provider/capability pairing,
  packet/blocker shape, runtime-only secret markers, and credential redaction.
- `scripts/execute_fish_audio.py` - execute one validated authorized Fish voice
  packet using a private-context public catalog voice, save the artifact, probe
  it, and write a sanitized receipt with no voice ID or credential.
- `scripts/execute_elevenlabs.py` - execute one validated authorized
  ElevenLabs voice or SFX packet, save the artifact, probe it, and write a
  sanitized hash-bearing receipt; run through the managed environment.
- [Audio Advisor](../audio-advisor/SKILL.md) - use when the creative direction,
  cue timing, rights, or mix plan is not approved.
- [Remotion](../remotion/SKILL.md) - use after generation for deterministic
  placement, captions, ducking, and render proof.

## Output

- `generation_packet`: dry-run-safe provider route and artifact contract.
- `execution_receipt`: generated artifact metadata plus sanitized provider and
  acceptance evidence.
- `blocked_report`: unsupported capability, unapproved brief, unresolved
  voice rights, missing execution authority, missing runtime secret, or failed
  artifact verification.
