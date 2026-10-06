---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-morning
name: Farplane Morning
kind: cron
status: active
runtime: claude
runtime_task: farplane-morning
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: "05:00"
---
Run Farplane's **Morning** chain on Claude Code: four records, run in this order in one session and each followed exactly, then one brief. The front matter is metadata; each record owns its steps and write policy.

Work in `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`.

1. **Fetch Context:** `farplane/automations/daily-collect.md`. Write today's run and its `_run.json` marker. Also copy each floor's whiteboard strategy doc found under `~/.farplane` into the run folder as `_strategy/<file>`, unchanged. That copy is the day's snapshot of the rolling strategy notes.
2. **Metrics Refresh:** `farplane/automations/metrics-refresh.md`.
3. **Knowledge Update:** `farplane/automations/knowledge-update.md`, on the run from step 1.
4. **Progress Updater:** `farplane/automations/daily-operating-update.md`, on the run from step 1 and the fresh metrics from step 2, including its pace check.

If a step fails or is blocked, record why in its receipt, then carry on with the later steps where they can still run. Steps 3, 4 and 5 need step 1's completion marker; without it, report them as blocked. Steps 1–4 are plumbing: don't narrate them.

5. **Morning brief.** This is the mancave's job: it serves Kenji's whole life, and each business is
   one floor of it. Read the Life Plan (game, money rules, tracks, guardrails, decision triggers)
   and the newest Plan Week fresh from Notion. Then read today's run: every call note (career and
   personal ones included), the Wiki changes from step 3, the metric changes from step 2, the
   project memory changes and overdue check-ins from step 4. Ask of each: what changed about a
   person, a company, a project or Kenji; what can be used as leverage; and what is it worth
   against the Life Plan? Write `.farplane/company-os/daily/briefs/<YYYY-MM-DD>.md` (local and
   private), then reply with that brief and nothing else.

Brief format:
0. **The call:** the one decision or move that matters most today, and why. Two lines.
1. **Entity updates:** people, companies, projects and Kenji. One line each: who → what's new →
   so what. Skip anything that didn't change.
2. **Leverage found:** each item tagged `[Intro]` `[Pain]` `[Asset]` `[Proof]` `[Capital]`
   `[Distribution]`, with its source and where it could be reused.
3. **Opportunities:** what · who benefits · value with the maths written out · assumptions ·
   confidence High/Med/Low · Life Plan triage: kill, park or test, with the cheapest test.
4. **Life:** how today's evidence moves the Life Plan's tracks or decision triggers (career, cash
   runway, focus). Give an opinionated recommendation, not a summary.
5. **Money and pace:** only what moved or is off pace, with numbers; otherwise "No movement."
6. **Today:** 1–3 moves, each with its why. Fold overdue check-ins into one line: the count, the
   oldest, and decide or kill.
7. **Questions for Kenji:** at most 3.

Brief style: insights, never a list of what each step did. A pipeline problem shows only as a
footer line, and only when it weakens a claim above (e.g. "Calls: 1 of 3 readable"). Every claim
names its source; inferences go in *italics*. Absolute dates. Never a value without its maths.
"None identified" rather than dropping a section. Under ~400 words, with the receipt path in the
footer.

Runtime notes (they don't change the records' rules):
- A skill written `$name` in a record is the Claude skill `name` (e.g. `progress-update`, `manage-wiki`); invoke it with the Skill tool.
- Tasks are GitHub Issues of each project's own repo; use the `gh` CLI. The only write allowed is a `gh issue comment` on an existing issue, through Progress Updater's allowlist. Public repos (Farplane, Farplane-UI, farplane-bunker) get engineering facts only. Multica is archived.
- Read Notion (the Plan Week and Life Plan adapter, and call notes) through the Notion connector, read-only.
- Credentialed commands go through `farplane run -- <command>`; never print secrets.
- Wiki: anything that is leverage for Kenji's life, career included. It stays local, outside every git repo. No health details.
- Never send messages, publish, spend, or change settings. Other people's actions and unclear ownership stay proposals.
