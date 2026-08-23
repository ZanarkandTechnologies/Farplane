---
name: setup-advisor
version: 0.1.0
description: "Turn a project and desired external services into an operated setup, a human-gate wizard when needed, and a verified setup receipt."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.4.0"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Write, Glob, Grep, Bash, web_search
---

# Setup Advisor

## Context

Use this skill to provision, configure, migrate, or connect external services
for an existing project while minimizing operator work. The agent should
perform every safe, authorized, automatable step itself. Generate an interactive
wizard only for irreducible human gates such as login, MFA, secret revelation,
legal acceptance, payment, or an approval-gated cutover.

Keep `init-advisor` responsible for Farplane project substrate and stack
scaffolding. Keep `automation-advisor` responsible for recurring Codex
automations. This skill owns the verified setup receipt for service setup; it
does not own later service operation.

## Skill Signature

```text
setup_advisor(project_root, services?, target_state?, secret_store?, ci_target?, execution_mode?)
  -> setup_receipt + human_gate_wizard_or_spec? + verification_evidence
state: reads(repo config, env examples, CI references, provider config, local tool/auth readiness, current official docs); writes authorized setup/config changes, an ephemeral wizard by default, and a redacted receipt
owns: one verified setup receipt for the requested service set
gates: current_journey_grounded; automate_before_handoff; secret_destination_safe; external_side_effect_authorized; every_service_status_verified
routes: init-advisor | automation-advisor | research:official-docs | direct-action
fails: asks the operator to do automatable work; invents dashboard steps; exposes or tracks secrets; claims setup complete with unverified or blocked services
```

`execution_mode := operate | guide | plan`. Default to `operate` when the
request authorizes setup. Use `guide` when only a human can operate the target
environment, and `plan` when the user asked for analysis only.

## Phase Boundary

Inspect official provider documentation inline for a single ordinary service.
Use `research:official-docs` only when several providers, conflicting docs, or
a migration need a separate evidence artifact. Use independent review for
material cutovers or credential-routing changes; do not externalize routine
setup planning.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Route and preflight the setup request.
  - [ ] Read the first-load Todo List guardrails before execution.
  - [ ] Route Farplane substrate creation to `init-advisor` and recurring Codex
        automation activation to `automation-advisor`; retain external-service
        provisioning here. For a mixed request, return the explicit owner
        sequence: initialize the project first, run service setup against that
        state second, then activate automations that consume the bindings.
  - [ ] Resolve `project_root`, desired end state, execution mode, service set,
        secret store, CI target, available tools, and side-effect authority from
        the request and local state before asking a question.
- [ ] 2. Discover the real setup contract.
  - [ ] Inspect README files, package manifests, `.env*` examples, compose and
        deployment files, provider configs, and every CI `secrets.*` / `vars.*`
        reference; never print existing values.
  - [ ] Check local CLI installation and authentication redactedly, then read
        current official docs for each command or dashboard journey that will
        be prescribed. Record each inspected source by provider, page title,
        and URL; when current docs could not be inspected, say so and avoid
        asserting an exact UI journey or undocumented authenticated command.
        A URL found in a fixture or recalled from memory is not inspection.
        Never claim a source was inspected “today” or “this run” unless an
        actual web/browser open is present in this invocation's evidence. In a
        read-only fixture, isolated eval, or supplied-context-only plan, default
        every external source to `not_inspected`; describe provider commands as
        pending live-doc confirmation instead of presenting them as current.
  - [ ] Build a dependency-ordered map of prerequisites, exact current
        commands or probes, outputs, destinations, secret/public
        classification, reversibility, verification, and owner (`agent` or
        `human`). Distinguish provider-login credentials from application
        runtime values and name the safe destination for both. Preserve every
        discovered configuration key exactly and map `source value -> exact
        destination store + key`; categories such as “runtime secrets” are not
        a sufficient destination.
  - [ ] Account for every discovered dependency and safety step in the map;
        mark each `agent`, `human`, or `blocked` rather than silently dropping
        inconvenient items such as TTL preparation, rollback snapshots, or
        preflight probes.
- [ ] 3. Operate everything the agent can safely complete.
  - [ ] Use available CLI, API, and browser capabilities for reversible,
        authorized steps; reuse existing configuration and make reruns safe.
        Keep install, local configuration, linking, and non-secret probes in an
        agent-preparation block; never bundle them into a human wizard stage.
  - [ ] Pause only for login/MFA, secret reveal, legal or payment acceptance,
        missing authority, destructive changes, deploys, DNS/cutovers, or
        another action whose consequence requires the operator.
  - [ ] Store Farplane-project secrets in Doppler by default and CI secrets in
        the named CI store. Never write a secret to a tracked file; use a local
        ignored env file only when the project contract and operator explicitly
        select it. When the request proposes repo storage, state this opt-in
        boundary explicitly rather than presenting an ignored env file as a
        fallback. Verify secret presence by names or consumer readiness only:
        for Doppler use `doppler secrets --only-names`, never `secrets get
        --plain`, and for CI use the provider's secret-name listing.
- [ ] 4. Generate a wizard only for remaining human gates.
  - [ ] Copy `templates/setup-wizard.sh` to an ignored project-local scratch
        path when available, otherwise an OS temp directory. Commit a wizard
        under `scripts/` only when the operator requests a repeatable setup path.
        In a read-only or plan-only environment, return the complete ordered
        wizard stage specification plus the exact agent-preparation commands,
        probes, and intended evidence paths instead of omitting them.
  - [ ] Author one focused stage per human task with the exact URL, current UI
        journey, captured value, safe destination, confirmation gate, and
        dependency order. A stage may name the agent action it unlocks, but must
        not ask the human to perform that automatable action. Use only helpers
        already present in the template.
  - [ ] Run `bash -n`, run `shellcheck` when available, make the copy executable,
        and statically trace every captured value to its declared destination.
- [ ] 5. Verify and return the setup receipt.
  - [ ] Give every requested service exactly one status: `configured`,
        `human_required`, `blocked`, or `failed`; run non-secret health probes
        and config-name checks wherever the provider supports them. For a
        cutover, name distinct pre-change and post-change probes, including
        consumer-visible routing/delivery checks rather than only rollback
        tripwires. Also account explicitly for current TTL, TTL preparation,
        config snapshots, exact mutation boundary, and rollback destination;
        in read-only mode, label authenticated provider commands as unavailable
        unless current docs were actually opened.
  - [ ] Record changed surfaces, redacted evidence, wizard path and run command,
        remaining human gates, rollback notes, and the next smallest action.
  - [ ] Apply the first-load Todo List guardrails again. Never collapse `human_required` or
        `blocked` into “setup complete.”
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Setup wizard template](templates/setup-wizard.sh) — copy only when Todo 4
  finds at least one irreducible human gate; never edit the library section in
  the generated copy.

Every operated, guide, or plan response uses this compact receipt shape; write
`none` rather than omitting a section:

```text
Setup status: service | configured|human_required|blocked|failed | evidence/blocker
Grounding: provider | inspected_this_run + page + URL | not_inspected + resulting limit
Current -> target: surface | exact current state | exact target state
Agent preparation: dependency order | exact command/action | proof | evidence path
Human gates: stage | exact human-only action | current URL | agent action unlocked
Value map: source value | secret/public/login | exact store | exact key
Local env policy: not selected | explicitly selected by project + operator
Verification / rollback: pre|post | probe | expected observation | recovery action
```

Positive example: “Set up Stripe and Vercel” leads the agent to inspect the
repo and CI, install a missing CLI before its login gate, configure authenticated
paths itself, and create a wizard only for login/key revelation. Each provider
login credential and application value has an explicit safe destination; the
receipt names configured and human-gated services without displaying values.

## Gotchas

- A link list is not a setup: operate the safe steps and make each human step
  precise enough for a stranger to complete.
- A successful command is not end-to-end proof: verify the consumer can see the
  expected non-secret configuration or readiness state.
- Do not create provider recipes before repeated evidence shows a stable,
  reusable journey; current official docs remain the source of truth.

## Reference Map

- the first-load Todo List guardrails — read before every setup and apply
  again before returning the receipt.
- [Behavioral eval suite](evals/evals.json) — use when changing routing,
  automation-first behavior, secret handling, or completion claims.

## Output

Return one redacted setup receipt containing scope, service-status table,
automated actions, human gates, exact source-to-destination key map, changed
surfaces, verification evidence, rollback notes, and the exact wizard command
when a wizard exists.
