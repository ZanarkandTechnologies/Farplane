# Bootstrap and Migration

Load for `init` or `migrate` mode: what bootstrap writes, how to upgrade an
existing Farplane project, and the finish checklist. The version-to-version
deltas live in [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md).

## Greenfield bootstrap

```bash
bash ~/.codex/skills/setup-advisor/scripts/bootstrap.sh [--force] <project>
```

Bootstrap copies the templates in this folder (inventory:
[reference-map.md](reference-map.md)) and never overwrites an existing file
unless `--force` is passed for an explicit scaffold replacement. It writes:

- `AGENTS.md`, `ARCHITECTURE.md`, `docs/{prd,HISTORY,MEMORY,TASTE,bootstrap-brief,code_review,review-agent}.md`;
- tracked `farplane/{README.md,manifest.json,harness.yaml,metrics.yaml,bindings.yaml,pm.json}`
  plus an empty `farplane/automations/` (jobs come from `automation-advisor`);
- `.agents/skills/README.md` for project-local capability skills;
- ignored `.farplane/README.md` and `.farplane/views.yaml` (`views: {}`); other
  `.farplane/` folders appear when their writers first run;
- `tickets/README.md`, `tickets/templates/ticket.md` and three foundation
  drafts `tickets/TASK-0001..0003` (find customer -> deliver value -> collect
  revenue, each depending on the previous). File them as GitHub issues when
  the project has a repo; existing paths are preserved one by one and each
  collision is reported;
- opt-in `.githooks/` and `scripts/pre_{commit,push}_check.sh` plus the Codex
  SDK diff-review helpers; hooks are never enabled automatically;
- the [GITIGNORE_TEMPLATE](GITIGNORE_TEMPLATE) block in `.gitignore`.

The intake answers (local hooks vs CI/deploy gate, advisory or strict diff
review, one app-only run path, one QA/evidence run path, required services,
ports and env names, UI theme plan) go in `docs/bootstrap-brief.md` and the
generated `AGENTS.md` Build & Run / Agent QA sections.

Optional local hooks after bootstrap:

```bash
git config core.hooksPath .githooks && chmod +x .githooks/pre-push
npm install --save-dev @openai/codex-sdk tsx   # Node projects: diff reviewer
```

Add package scripts `review:agent` (`tsx scripts/codex_review_agent.ts`) and
`review:prepush` (`bash scripts/run_pre_push_review.sh`). Prefer `pre-push`;
leave `pre-commit` off unless the project wants the heavier gate.

## Brownfield migration

1. Read `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework`, then apply each newer
   [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md) entry in order.
2. Add missing scaffold files with `bootstrap.sh` (no `--force`).
3. Upgrade framework fields with the only safe force path:

   ```bash
   python3 ~/.codex/skills/setup-advisor/scripts/migrate_framework.py --project-root . --force
   ```

   It updates versioned fields and deterministic metric `kind -> type`
   mappings while preserving the human charter, metric definitions, refresh
   prompts, bindings, docs and tickets. Never use `bootstrap.sh --force` as an
   upgrade.
4. When a migration changes Wiki or entity schemas, update consumers first,
   then regenerate (never hand-migrate generated files):

   ```bash
   farplane wiki doctor --project-root . --json
   farplane wiki rebuild --project-root . --no-write --json
   farplane wiki rebuild --project-root .
   ```

5. Regenerate read models and validate:

   ```bash
   farplane metrics primitives --project-root . --date <YYYY-MM-DD> --json
   farplane project snapshot --project-root . --date <YYYY-MM-DD> --json
   python3 bin/validators/check_farplane_project_files.py --root .
   ```

Remove retired controllers, registries and detached review/evidence stores
only after their active readers move. Keep no compatibility aliases unless an
external contract requires one.

Keep the first migration slice small: one PRD or spec, one real GitHub issue,
one `impl-plan -> goal-advisor` cycle. Do not convert the whole backlog, start
parallel ticket farms or cloud lanes before one clean ticket run.

## Finish checklist

- [ ] Manifest compared with the changelog; each newer migration applied.
- [ ] `docs/bootstrap-brief.md` records stack, topology, local-gate, CI/deploy
      gate, diff-review policy, run paths, services, ports and env names.
- [ ] `AGENTS.md` names the app-only and QA/evidence launch commands.
- [ ] `farplane/harness.yaml` holds real intent, or a readiness gap is recorded.
- [ ] `farplane/metrics.yaml` defines every objective and guard metric with one
      `refresh` or `refresh_ref`; a metric without a provider is marked not live.
- [ ] `farplane/bindings.yaml` holds non-secret IDs, URLs and aliases only.
- [ ] `farplane/automations/` holds only live routines, one file each.
- [ ] Wiki schema changes passed `wiki doctor` and a `--no-write` rebuild.
- [ ] `check_farplane_project_files.py` passes where the validator exists.
- [ ] Foundation drafts exist or were filed as issues; collisions reported.
