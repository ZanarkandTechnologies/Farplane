---
name: notion-task-field-fill
description: "Turn incomplete Notion Tasks into field proposals, safe high-confidence patches, and Telegram review requests."
tier: 3
group: back-office
source: local
capability:
  kind: integration
methods:
  - id: notion-task-field-fill:proposal
    class: artifact
    output: notion-task-field-proposal
  - id: notion-task-field-fill:apply
    class: integration
    output: notion-task-field-write-receipt
template_uses:
  skill-template: "0.3.7"
allowed-tools: Read, Glob, Grep, Bash
---

# Notion Task Field Fill

Use this skill when Kenji asks to fill missing Notion Task fields, run a task
hygiene automation, review newly created unfilled tasks, or prepare a weekly
strategy `Task Hygiene` preflight.

This is a proposal-first workflow. It reads private Notion handles and compact
query recipes from `/Users/kenjipcx/.codex/private/docs/notion.md`, queries
Notion through the official `ntn` CLI, writes a local proposal artifact, and only applies live
Notion property updates from typed high-confidence proposals.

Low-level helper scripts in this skill that need direct Notion credentials must
load a single key through `scripts/notion_config.py`: `NOTION_TOKEN` from the
process environment, preferably via `farplane run -- <command>` or
`doppler run -- <command>`. Local TOML is not a credential source. Do not read
`NOTION_API_KEY`, `notion_api_key`, or Codex MCP config from skill scripts.
When launching `ntn`, bridge `NOTION_TOKEN` to `NOTION_API_TOKEN` only at the
subprocess boundary.

## Skill Signature

```text
notion_task_field_fill(run_envelope, private_context?, ntn_cli?)
  -> proposal_artifacts + optional_typed_writes + readback_receipts

state:
  reads(/Users/kenjipcx/.codex/private/TOOLS.md,
        /Users/kenjipcx/.codex/private/docs/notion.md,
        ntn Tasks/Projects/Goals rows?, NOTION_TOKEN for helper
        scripts?, Telegram config?)
  writes(.farplane/state/notion-task-field-fill/runs/<run-id>/*,
         optional high-confidence Notion field updates,
         optional Telegram review request)

gates:
  private_handles_loaded; compact_query_contract_honored;
  rows_normalized_before_reasoning; no_raw_private_ids_in_artifacts;
  high_confidence_only_live_writes; readback_verified_for_live_writes

routes:
  telegram-message | review

fails:
  uses Notion MCP as the normal path; uses a separate Notion wrapper skill;
  broad Notion page dump; semantic-search task discovery; raw public API helper
  fallback outside `ntn`; reads NOTION_API_KEY/notion_api_key; writes
  medium/low-confidence fields; stores private URLs, IDs, or tokens in tracked
  artifacts
```

## Phase Boundary

This skill follows Tier 0 phases inline. Call `review` only when changing this
skill, adding a live-write path, or judging a material proof bundle. Do not call
a separate Notion wrapper skill at runtime; the private Notion doc plus `ntn`
are the dependency boundary.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind inputs.
      Resolve `mode`, run window, target fields, candidate statuses, artifact
      directory, and live-write allowance before fetching Notion rows.
- [ ] 2. Load private context.
      Read `/Users/kenjipcx/.codex/private/TOOLS.md` and
      `/Users/kenjipcx/.codex/private/docs/notion.md`; use named handles only
      in tracked artifacts. If a low-level helper script needs a credential,
      load only `NOTION_TOKEN` via `scripts/notion_config.py`.
- [ ] 3. Discover candidates.
      Run one compact `ntn` Tasks query with bounded page size,
      `filter_properties`, no repeated equivalent query, and no raw page dump.
- [ ] 4. Normalize or stop.
      Normalize and filter candidate rows before reasoning; record
      `private_context_missing`, `unexpected_task_properties`,
      `compact_query_failed`, or `connector_unavailable` when the source path
      is unsafe.
- [ ] 5. Enrich only as needed.
      Fetch Plan Week, pinned pages, Projects, Goals, and area mappings through
      compact `ntn` queries only when candidates need that context.
- [ ] 6. Decide fields independently.
      Produce per-field decisions for `Act Time`, `Project`, `Areas`,
      `Attention Required`, and `Tags`; abstain on conflicting evidence.
- [ ] 7. Escalate or write safely.
      Queue Telegram/local review for low-confidence or conflicted fields; in
      live mode write only high-confidence typed patches and verify readback.
- [ ] 8. Finish with proof.
      Write proposal artifacts, query ledger, source gaps, Telegram fallback,
      live receipts, and any blocker before claiming the run is complete.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Modes And Detailed Workflow

Default to `dry-run`. Use `notify` for proposal plus review messages,
`live-high-confidence` only after its typed write/readback path is reviewed,
`weekly-preflight` for weekly evidence, and `fixture` for local tests.

After candidates exist, load [workflow detail](references/workflow.md) for the
run envelope, compact-query budgets, proposal rules, artifacts, Telegram path,
write gates, and completion contract. Load [model](references/model.md) and
[confidence](references/confidence.md) only when deciding fields.

## Output

Return artifact paths, candidate and proposal counts, per-field confidence,
source gaps, Telegram fallback, applied patch/readback receipts, and blockers.
Provider effects must be `none` outside reviewed `live-high-confidence` mode.
