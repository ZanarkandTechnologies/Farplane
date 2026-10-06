# Repo structure audit — 2026-10-07

Read-only sweep of the Farplane checkout's top level. Each finding names what is there,
why it's questionable, who reads it, and the proposed change. Nothing here is applied yet.

**Rule used:** one home per job. Shared sources at the root, generated output only under
ignored `.farplane/`, each runtime's adapter under `runtimes/<name>/`, and a file that one
skill owns lives in that skill.

## Target shape

```text
Farplane/
  AGENTS.md  ARCHITECTURE.md  README.md      # one rules file, not two
  agents/  hooks/  rules/  skills/  bin/  docs/   # shared sources (unchanged)
  farplane/        # this project's config only: harness, metrics, bindings, automations/
  runtimes/
    claude/        # renders shared sources for Claude Code (exists)
    codex/         # renders them for Codex: hooks.json, global AGENTS.md, config example
  tickets/         # GitHub-issue templates and the frozen legacy archive only
  .farplane/       # every generated file, including tmp/ and tool output
```

Gone from the root: `output/`, `tmp/`, `meshy_output/`, `qa/`, `tests/`, `templates/`,
`PROJECT_RULES.md`, `hooks.json`, `config.toml.example`.

## Findings

### Generated output outside `.farplane/`

| Path | What's there | Writer | Proposal |
|---|---|---|---|
| `meshy_output/` (132 MB, ignored) | 3D models from one 1 Oct run | `meshy-3d-generation` writes to `$PWD/meshy_output` | The skill writes to `.farplane/meshy/`; move the run there |
| `output/` (30 MB, ignored) | One 28 Jul video-production proof | No current writer | Move to `.farplane/` or trash; drop the folder |
| `tmp/` (1.7 MB, ignored) | Jul–Sep social dry runs and blocked-login JSON | Ad-hoc agent scratch | Trash. Scratch goes to the session scratchpad or `.farplane/tmp/` (which `plan_wave_guard` already uses) |
| `.tmp-validation.*/` (empty) | Leftover validator temp dirs | A validator that doesn't clean up | Delete them; make the validator remove its temp dir |

### Stale or duplicate rules

- **`PROJECT_RULES.md`** still calls the repo a "Codex Harness" and says active work lives in
  Multica. Its folder map repeats `AGENTS.md` and `README.md`. The validator requires it
  (`required_paths`). **Proposal:** fold anything unique into `AGENTS.md`, delete the file, and
  remove it from `required_paths` and the init templates.

### `tickets/`: legacy, and 898 MB on disk

- Tracked: the task-record rules (`README.md`), templates (`ticket.md` is required by the
  validator; `goal-loop/` is used by `impl-plan` and `goal-advisor`), the metadata check
  script, and the legacy archive (about 3 MB, 12 tickets).
- Ignored: 51 local `TASK-*` proof folders, about 650 MB. The largest are `TASK-0416`
  (383 MB) and `TASK-0429` (94 MB). Active work is GitHub Issues, so these are proof of
  closed Multica-era work.
- **Proposal:**
  1. Keep `tickets/` for the GitHub-issue body templates and the frozen archive only.
  2. Check that no open issue links a local `TASK-*` folder, then trash those folders.
  3. Move the task-record rules from `tickets/README.md` into `docs/`, so `tickets/` holds
     templates only.

### Runtimes are uneven: `claude/` exists, `codex/` doesn't

Codex is the native layout: root `hooks.json`, `agents/*.toml`, `templates/global/AGENTS.md`
and `config.toml.example` are written for `~/.codex`, and `install.sh` copies them. Claude
gets a rendered adapter in `runtimes/claude/`. That's why only one runtime folder exists.
**Proposal:** add `runtimes/codex/` and move the Codex-only files into it: `hooks.json`
(currently a source that the Claude render rewrites), the global `AGENTS.md`, and
`config.toml.example`. Each runtime folder then owns how the shared sources render for it,
and that's also where the automation renderer from the 6 Oct catalog goes. This changes
`install.sh`, `farplane_claude_install.py` and the Claude install test.

### Four homes for templates

| Home | Holds | Proposal |
|---|---|---|
| `templates/global/AGENTS.md` | the install-time global contract | `runtimes/codex/` and the Claude render read it from there |
| `templates/external-cli/` | Pi/Kimi delegate profiles | `skills/delegate-cli/templates/`, its only user |
| `docs/templates/` | doc templates and the template registry | keep |
| `tickets/templates/` | issue body templates | keep |

The root `templates/` folder then disappears.

### One-skill folders at the root

- **`qa/`** (8 docs: the QA guide and cookbook) belongs to `skills/qa`, `agents/qa-tester` and
  `proof-advisor`. **Proposal:** move it to `skills/qa/references/` and fold `qa/AGENTS.md`
  into the skill.
- **`tests/`** (4 fixture files) is read only by `bin/validators/check_skill_capabilities.py`.
  **Proposal:** move it to `bin/validators/fixtures/`. Then tests live in two places, both by
  rule: `bin/tests` for core code and `skills/<name>/scripts/test_*` for skill scripts.

### `farplane/` should be config only

- **`farplane/phone-chaser/`** is a whole LiveKit voice-agent app (Dockerfile, `uv.lock`, a
  206 MB `.venv`) inside the project's config folder. **Proposal:** give it its own repo, or
  an `apps/phone-chaser/` folder outside `farplane/`. It can't live under the `phone-chaser`
  skill, because skills are installed into `~/.claude/skills` and `~/.codex/skills`, and the
  venv would be copied with them.
- **`farplane/strategy/`** is ignored private strategy inside a public repo's config folder.
  **Proposal:** move it to `~/.farplane/`, where the private notes and company files already
  live, so a bad ignore rule can never publish it.

### Smaller things

- **`.agent-office/`** (the bunker's runtime state for this checkout) is ignored through
  `.git/info/exclude`, not `.gitignore`, so a fresh clone would show it as untracked.
  **Proposal:** add it to `.gitignore`, or have the bunker write under `.farplane/`.
- **`.agents/skills/`** holds five project-local skills next to the 123 product skills in
  `skills/`. This follows the Codex project-skill convention, so keep it, and say so in
  `ARCHITECTURE.md`.
- **`docs/doc-audit/2026-09-30-automations-v2-plan.md`** has become the live automation
  catalog. **Proposal:** move the catalog table to
  `docs/farplane-framework/automations.md`, and leave the dated plan as history.
- **`assets/`** (3 README images) is fine as is.

## Suggested order

Each step is one commit, ordered by safety:

1. Generated output: Meshy path, then trash `output/`, `tmp/` and `.tmp-validation.*`.
2. `qa/` → `skills/qa/`, `tests/` → `bin/validators/fixtures/`, `templates/external-cli/` →
   `delegate-cli`.
3. Fold `PROJECT_RULES.md` into `AGENTS.md`.
4. Ticket cleanup: check open issues, trash local `TASK-*` proof, move the rules to `docs/`.
5. Move `farplane/strategy/` to `~/.farplane/`; move `phone-chaser` out of `farplane/`.
6. `runtimes/codex/` and the move of `templates/global/` (touches install, so last).
