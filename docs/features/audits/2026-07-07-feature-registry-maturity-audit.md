---
title: Feature Registry Maturity Audit
status: complete
owner: feature-registry
created_at: 2026-07-07
refs:
  - docs/features/README.md
  - docs/features/TEMPLATE.md
  - docs/features/registry.jsonl
  - docs/systems/registry.jsonl
---

# Feature Registry Maturity Audit

This audit checks whether each current `FEAT-*` doc still earns a feature page, whether
it should be stable or experimental, and whether it should be merged, split, or
superseded later.

```text
feature_maturity_audit(feature_doc)
  -> keep_stable | keep_experimental | merge_candidate | retire_candidate
```

## Decision

Farplane feature docs may include experimental features when they describe a real
operator or agent UX contract. The feature registry is not a patch ledger: tiny fixes,
single-run experiments, and implementation details stay in tickets, product-loop
progress, reports, audits, or skill-local docs.

`experimental: true` means the capability is real enough to dogfood but not accepted as
globally stable. `superseded_by` marks the successor `FEAT-*` handle when the active
contract moved to a clearer feature.

## Summary

- Stable active feature docs kept: 16
- Experimental active feature docs kept: 5
- Retired or superseded feature handles kept for historical refs: 8
- Immediate delete candidates: 0
- Merge-watch candidates: 0
- New successor feature docs added for the current dogfood set:
  - `FEAT-0066` Product-scoped Pulse loops
  - `FEAT-0067` Daily interval review reports
  - `FEAT-0068` Goal-backed ticket execution
  - `FEAT-0069` Taste Loop human-feedback optimization
  - `FEAT-0070` Experimental feature evaluation reports

## Audit Table

| Feature | Current maturity | Decision | Rationale | Follow-up |
| --- | --- | --- | --- | --- |
| `FEAT-0007` Ticket as durable task memory | stable | keep_stable | Core Work Loop UX with durable owner surfaces and broad reuse. | None. |
| `FEAT-0008` Artifact-first QA and completion proof | stable | keep_stable | Core proof UX with review/report behavior across Farplane. | None. |
| `FEAT-0011` Harness scout source ingestion | stable | keep_stable | Source-ingestion capability with durable skill/docs surfaces. | None. |
| `FEAT-0014` Frontend skill parity upgrade | retired | retire_feature | Generic frontend skill-family work, not a Farplane-specific product capability. | Keep current truth in Domain Skill Families and frontend skills. |
| `FEAT-0015` Retired Symphony-compatible invocation contract | retired | retire_feature | Dead pre-Farplane/Symphony framing. | Preserve only while old refs exist; move any useful truth to Invocation Runtime history. |
| `FEAT-0022` Skill tier leverage classes | stable | keep_stable | Core Skill System classification and maintenance language. | None. |
| `FEAT-0025` Retired video-to-skill source reconstruction | retired | retire_feature | Generic source/media skill workflow, not a Farplane product capability. | Keep current truth in media/source-ingestion skills. |
| `FEAT-0029` Retired Goal Packet architecture | retired | superseded_by `FEAT-0032` | Goal Packet files are implementation surfaces; Goal Advisor is the feature UX. | Keep as historical handle until active refs are cleaned. |
| `FEAT-0030` On-demand skill plugin packaging | stable | keep_stable | Distinct packaging/install capability. | None. |
| `FEAT-0031` Agent behavior test workflow | stable | keep_stable | Distinct proof workflow with artifacts and logs. | None. |
| `FEAT-0032` Goal Advisor execution loop | stable | keep_stable | Core Horizon execution UX that includes Goal Packet setup and prompt compilation. | None. |
| `FEAT-0034` Adversarial agent QA test skill | stable | keep_stable | Distinct QA orchestration capability. | None. |
| `FEAT-0039` Farplane evals | stable | keep_stable | Consolidated eval capability for hardcases, prompt evals, and skill-local eval tasks. | Owns former `FEAT-0043` and `FEAT-0054` behavior. |
| `FEAT-0042` Retired lean global agent operating kernel | retired | retire_feature | Agent Kernel is a system/policy surface, not a distinct feature doc. | Keep truth in Agent Kernel system and templates. |
| `FEAT-0043` Retired project-level system prompt eval suite | retired | superseded_by `FEAT-0039` | Prompt evals are part of consolidated Farplane evals. | Keep eval files as surfaces. |
| `FEAT-0054` Retired modular skill-local eval tasks | retired | superseded_by `FEAT-0039` | Skill-local eval tasks are part of consolidated Farplane evals. | Keep eval files as surfaces. |
| `FEAT-0056` Tasty Pack inspiration vault | stable | keep_stable | Completed source-memory/Tasty Pack capability. | Track retrieval quality through source/product evidence, not experimental maturity. |
| `FEAT-0057` Skill-local QA checklist artifacts | stable | keep_stable | Distinct QA/checklist artifact contract; current dirty worktree edits preserve this as active. | None. |
| `FEAT-0060` Registry-backed documentation OS | stable | keep_stable | Owns the registry/schema/doc lifecycle itself. | None. |
| `FEAT-0061` Farplane adoption tracker CLI | stable | keep_stable | Real CLI/report capability for adoption and maintenance visibility. | None. |
| `FEAT-0062` Capped skill surface budget | stable | keep_stable | Distinct Skill System guardrail with validator/eval behavior. | None. |
| `FEAT-0063` Metric advisor cards | stable | keep_stable | Distinct metric-choice UX for self-improvement. | None. |
| `FEAT-0064` Skill signals | stable | keep_stable | Distinct signal language; Taste Loop feedback optimization now references it rather than hiding inside it. | None. |
| `FEAT-0065` Pulse and interval automation | retired | superseded_by `FEAT-0066`, `FEAT-0067` | Older umbrella handle is superseded by Product-scoped Pulse and Daily interval review reports. | Keep while active refs exist; successor features own active dogfood tracking. |
| `FEAT-0066` Product-scoped Pulse loops | experimental | keep_experimental | New product-loop ticket-supply UX currently being dogfooded. | Dogfood review should decide cap/adjust/graduate. |
| `FEAT-0067` Daily interval review reports | experimental | keep_experimental | New daily report/dogfood composition UX. | Dogfood review should decide whether report shape is useful. |
| `FEAT-0068` Goal-backed ticket execution | experimental | keep_experimental | Names the ticket-executor UX without inventing a daemon or new skill. | Track until execution quality is stable enough to mark non-experimental or fold into `FEAT-0007`/`FEAT-0032`. |
| `FEAT-0069` Taste Loop human-feedback optimization | experimental | keep_experimental | Unique recurring self-improvement UX using Taste Loop plus optimize-with-human. | Track feedback burden, artifact quality, and graduation decision. |
| `FEAT-0070` Experimental feature evaluation reports | experimental | keep_experimental | First-class harness-maintenance report for deciding whether experimental features graduate, adjust, split, merge, or retire. | Track report usefulness and whether it reduces operator review burden. |

## Supersession Notes

- `FEAT-0065` is now retired and marked as superseded by `FEAT-0066` and
  `FEAT-0067` for the newer product-scoped Pulse and daily interval report
  contracts. It is not deleted because active automation, skill, and docs
  references still use the umbrella handle.
- The old global Pulse ticket-supply behavior has no separate feature doc; its
  replacement is represented by `FEAT-0066`.
- `FEAT-0068` intentionally avoids creating a `ticket-executor` skill. The feature
  handle is for dogfood review of the ticket execution UX across existing Work Loop
  surfaces.
- `FEAT-0039` now owns consolidated Farplane evals. `FEAT-0043` and `FEAT-0054`
  are retired historical handles superseded by `FEAT-0039`.
- `FEAT-0070` owns the dogfood report UX for evaluating experimental feature
  maturity against `farplane/harness.md#Feature Policy`.

## Dogfood Review Feed

Dogfood review should include:

- any feature or system with a non-empty `track` prompt;
- any feature with `experimental: true` when the caller asks for the experimental
  feature feed;
- evidence from tickets, Pulse reports, interval reports, product-loop progress,
  audits, evals, and report directories.

The report decision vocabulary should allow `continue`, `adjust`, `cap`, `pause`,
`rollback`, `graduate`, `split_feature`, `merge`, and `source_gap`.

## Follow-Up Checks

- Run `python3 docs/features/validate_features.py --write`.
- Run `python3 docs/features/validate_features.py`.
- Run `python3 bin/validators/check_doc_refs.py`.
- Revisit merge-watch candidates after the next dogfood cycle.
