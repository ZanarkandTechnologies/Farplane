---
name: setup-advisor
description: "Use for \"set up this project\", \"start a new project\", \"set up the client deployment\" or \"wire up secrets\": a Farplane substrate, split charter with honest KPIs, wired services and a verified setup receipt."
source: local
department: delivery
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Write, Glob, Grep, Bash, web_search
---

# Setup Advisor

## Context

Use this to set up a project or client deployment end to end: scaffold a new
Farplane project, upgrade an existing one, turn a business or project idea into
its charter, metric objectives and starter tickets, or provision and connect
external services and secrets. The agent runs every safe, authorized step
itself; the operator only clears login, MFA, OAuth, payment, legal or CAPTCHA
gates. It does not own recurring automations (`automation-advisor`), feature
specs (`prd`), ticket plans (`impl-plan`) or Goal execution (`goal-advisor`).

## Skill Signature

```text
setup_advisor(target, mode?: init | charter | deploy | migrate, services?, human_intake?, force?)
  -> setup_receipt
reads: repo files, farplane/*, docs/bootstrap-brief.md, .env examples, CI refs,
       provider config, CLI auth state, current official provider docs
does: scaffolds or upgrades the substrate, drafts the split charter, files
      starter issues, operates safe service setup, wizards only human gates
writes: Farplane scaffold, farplane/{harness,metrics,bindings}.yaml deltas,
        GitHub issues, provider config, an ephemeral wizard, a redacted receipt
returns: per-surface status + evidence + human gates + readiness gaps + next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the target and pick the mode.**
  `request + repo state -> mode sequence + project_root + authority | blocked`

  Rule: No `farplane/` yet is `init`; an old `farplane/manifest.json` version
  is `migrate`; an idea, thesis, KPI or "operating model" ask is `charter`;
  services, secrets, CI, DNS or a client deployment is `deploy`. A mixed ask
  runs in that order (substrate, then charter, then services, then
  `automation-advisor` for jobs) with one receipt. Inspect README, AGENTS,
  docs, package files and existing tickets before writing or asking.

  Example: "start a new project and hook up Stripe" -> `init` -> `charter` ->
  `deploy`, one receipt.

  Assert:
  - One ordered mode sequence and named authority, or the missing input.
- [ ] **N2 — init / migrate: lay down or upgrade the substrate.**
  `project_root + profile + force? -> scaffold + bootstrap brief | collisions`

  Rule: Run `scripts/bootstrap.sh <project>`; it never overwrites without
  `--force`, which is only for an explicit scaffold replacement. To upgrade an
  existing project, apply [FRAMEWORK_CHANGELOG](references/FRAMEWORK_CHANGELOG.md)
  entries in order and run `scripts/migrate_framework.py --project-root <p>
  --force`, the only safe force path: never hand-force over project files.
  Pick the profile from [project-profiles](references/project-profiles.md); for
  an app scaffold load [CODE_SCAFFOLD_RECIPES](references/CODE_SCAFFOLD_RECIPES.md)
  and stop at cloud login, billing or deploy. Load
  [migration](references/migration.md) for the inventory and finish checklist.

  Assert:
  - Every pre-existing file is byte-identical or named as an approved overwrite.
  - Hooks stay disabled; no live automation or thread is created.
- [ ] **N3 — charter: draft the split charter with honest metrics.**
  `idea + values + constraints -> harness/metrics/bindings delta | readiness gap`

  Rule: The charter is split: `farplane/harness.yaml` (thesis, non-tradeoffs,
  authority, planning areas, capability and metric refs), `metrics.yaml`
  (meaning, direction, freshness, guards, refresh) and `bindings.yaml`
  (non-secret provider coordinates), from the HARNESS/METRICS/BINDINGS
  templates. Reuse `docs/skills/registry.jsonl`, root and `.agents/skills/`
  workflows before proposing a local skill. Missing thesis, non-goals or
  authority is one question or a gap in `docs/bootstrap-brief.md`
  ([phase-boundary](references/phase-boundary.md)).

  Assert:
  - Every live KPI names an honest provider binding; with none, it is marked
    not live with the credential, export, API or instrumentation that unblocks
    it. No number is invented.
- [ ] **N4 — charter: file starter tickets and hand off.**
  `approved charter + milestone -> GitHub issues + next owner`

  Rule: Starter and unblock tickets are GitHub issues in the project's own repo
  (search first, `gh issue create --body-file`); bootstrap's `TASK-0001..0003`
  foundation files are body drafts for find customer -> deliver value ->
  collect revenue. Client and business issues go to private repos only. Use
  [goal-advisor handoff](templates/goal-advisor-handoff.md) once a ticket,
  metric provider, stop rule and proof boundary are known; route owner
  placement to `harness` place mode, new workflows to `harness` create mode.

  Assert:
  - Each access, setup or approval blocker is its own unblock issue.
  - No controller, extra heartbeat or native Goal is created here.
- [ ] **N5 — deploy: map the real setup contract and operate safe steps.**
  `repo config + CI refs + docs -> dependency map + configured steps | gate`

  Rule: Read `.env*` examples, compose/deploy files, provider config and every
  CI `secrets.*`/`vars.*` ref; check CLI auth redactedly; open current official
  docs before prescribing a command or UI journey (otherwise mark it
  `not_inspected`). Map each value `source -> exact store + key`. Secrets go to
  Doppler for Farplane projects and to the named CI store; check them with
  `doppler secrets --only-names`, never `--plain`, and never write one to a
  tracked file.

  Assert:
  - Every discovered key, TTL, snapshot and probe is `agent`, `human` or
    `blocked`; none is silently dropped.
- [ ] **N6 — deploy: wizard only the human gates.**
  `remaining gates -> ephemeral wizard | stage spec`

  Rule: Copy [setup-wizard.sh](templates/setup-wizard.sh) to ignored scratch
  only for login, OAuth, payment, legal, MFA, secret reveal or CAPTCHA; every
  install, config, link or probe stays with the agent. One stage per gate with
  URL, captured value, destination and confirmation; read-only runs return the
  stage spec. Pause before DNS, cutover, deploy or destructive steps.

  Assert:
  - `bash -n` passes and each captured value traces to its destination.
- [ ] **N7 — Verify and return the setup receipt.**
  `mode outputs + probes -> receipt | escalation`

  Rule: Run the narrowest proof per mode: `bootstrap.sh`/migration output,
  `python3 bin/validators/check_farplane_project_files.py` where present,
  non-secret health and name probes, pre- and post-change probes for a cutover.
  Report a plain status: "Ready", "Filesystem ready, operating model still
  missing", "Services human_required" or "Blocked".

  Assert:
  - Each service is `configured | human_required | blocked | failed`; a human
    or blocked item is never reported as complete.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- File existence is not readiness: placeholder `harness.yaml` means the
  operating model is still missing.
- `bootstrap.sh --force` is not an upgrade; it replaces whole files.
- A link list is not a setup: operate the safe steps, wizard only the gates.
- A successful command is not end-to-end proof; check the consumer sees it.
- The charter worksheet is evidence, never the charter; do not create a
  Markdown charter.
- Do not invent thesis, authority, spend, publishing, contact or credentials.
- Keep project-specific capabilities in `.agents/skills/` until repeated
  cross-project proof.

## Reference Map

- [reference-map](references/reference-map.md) - every template, its target,
  and which mode loads it.
- [migration](references/migration.md) - bootstrap inventory, brownfield
  upgrade, Wiki regeneration, finish checklist.
- [phase-boundary](references/phase-boundary.md) - `human_intake`, readiness
  states, split-file ownership.
- [CODE_SCAFFOLD_RECIPES](references/CODE_SCAFFOLD_RECIPES.md) - stack recipes
  (Convex, Next.js, Clerk, shadcn, quality tooling).
- [project-harness worksheet](templates/project-harness.md),
  [capability map](templates/capability-map.md),
  [missing primitive plan](templates/missing-primitive-plan.md) - charter mode.
- [AGENTS.md](AGENTS.md) - bootstrap invariants for the generated project.
- [evals](evals/evals.json) - routing, secrets, foundation and KPI honesty.

## Output

```text
Mode: init | migrate | charter | deploy (sequence)
Status: Ready | Filesystem ready, operating model still missing | Services human_required | Blocked
Substrate: written | preserved | collisions <paths> | migrated <from -> to>
Charter: harness/metrics/bindings deltas | KPI -> provider | not-live KPIs + unblock
Issues: starter and unblock issue links | foundation drafts
Setup status: service | configured|human_required|blocked|failed | evidence
Grounding: provider | inspected + page + URL | not_inspected + limit
Value map: source value | secret/public/login | exact store | exact key
Human gates: stage | human-only action | URL | agent action unlocked | wizard cmd
Verification / rollback: probe | expected observation | recovery action
Next owner: automation-advisor | prd | impl-plan | goal-advisor | none
```
