---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-intel-digest
name: Farplane Intel Digest
kind: cron
status: active
runtime: claude
runtime_task: farplane-intel-digest
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: Asia/Kuala_Lumpur
  time: "23:15"
---
Run Farplane's **Intel Digest** automation on Claude Code: first the bookmarks, then Feed Scout.

Work in `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`. Run the two records below in order, following each body exactly; the front matter is metadata. If the first part is blocked, still run the second.

**Part 1: Bookmarks.** Run `farplane/automations/steps/bookmark-recovery.md`: its sources, ledger, validator, person matches against open Wiki problems, write policy and final response.
- **X is read in the browser only, never through the X API.** Use Claude in Chrome (the operator's logged-in Chrome): x.com → Bookmarks, read-only.
- Never like, repost, reply, bookmark or follow, and never change an X setting.
- If Chrome isn't connected or X asks to sign in, report that as this part's blocker. Never type credentials.

**Part 2: Feed Scout.** Run `farplane/automations/steps/feed-scout.md`, with this boundary:
- Use public and direct sources and the browser only. **No Apify or any other paid scraping.** A source that needs one is a source gap.
- **Never create, comment on or label GitHub issues.** Report recovery candidates in the report only.
- Write its dated report and `latest.json` under `.farplane/reports/feed-scout/` as the record says. The office's Intel panel reads them.

Claude runtime notes:
- A skill written `$name` in a record is the Claude skill `name` (e.g. `bookmark-recovery`, `feed-scout`, `intelligest`); invoke it with the Skill tool.
- Credentialed commands go through `farplane run -- <command>`; never print secrets.
- Never send messages, publish, spend, or change settings.

End with both records' final responses: the bookmarks read, who each could help and the inbox path; then Feed Scout's summary, candidates and report path.
