---
name: research
description: "Use for \"research X\", \"how do others do this\", \"who are the competitors\" or \"find the paper\": pick the source branch, verify claims at the source, return a ranked evidence note."
source: local
department: intelligence
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash, web_search, documentation-searcher
---

# Research

## Context

Use this when a decision needs outside evidence the agent does not already
hold: who competes for a customer job (`market`), how maintained code solves a
local feature (`code`), which research-backed approach deserves an experiment
(`papers`), or which features to take from several sources (`synthesis`). One
pass answers one decision with one evidence note.

A caller that only needs one claim grounded does not need this skill: follow
the global contract's `Grounding:` rule inline and stop. Research one person
or account with `customer-research`, turn one external source into Farplane
features with `harness-scout`, and run an accepted experiment with
`ml-autoresearch` or the experiment owner.

## Skill Signature

```text
research(question, branch?: market | code | papers | synthesis, local_target?, budget?)
  -> evidence_note { claims + source class + opened? + verdict or ranking } + next_owner
reads: local baseline, official sites and docs, repos, issues, papers, reviews, community threads, demos
does: binds the decision, finds candidates, qualifies them at the source, deep-dives finalists, decides
writes: none, unless the caller supplies an artifact owner
returns: the evidence note, rejection ledger, recommendation and its downside, next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the decision and pick one branch.**
  `question + local baseline -> decision contract + branch | inline grounding | blocked`

  Rule: Name the decision the evidence must move, the local baseline, the
  freshness bar, and the observation that would change the answer. Infer the
  branch: a market, product, or "who else does this" question is `market`; a
  feature against local code is `code`; a technique, benchmark, or "find the
  paper" is `papers`; several named sources to combine is `synthesis`. For
  `code`, read the local seam (entrypoint, owners, state flow, tests, failure
  path) before searching.

  Example: `"how do others do resumable uploads?" + upload.ts -> code branch;
  local seam read first, so the search names multipart symbols, not tutorials`

  Assert:
  - Hypotheses are written as questions evidence can confirm or reject.
  - A one-claim question is answered with a `Grounding:` line, not a brief.
- [ ] **N2 — Build a reproducible candidate pool.**
  `decision contract -> query ledger + candidate pool | thin-evidence branch`

  Rule: Record every query, filter, date, and empty result. `market` searches
  official sites, reviews, Reddit, X, YouTube, and switching or pricing terms;
  `code` searches literal symbols, imports, config keys, and exact error
  strings, never tutorial phrasing; `papers` traces citations backward and
  forward, then authors, labs, repos, and replications. Do not stop at the
  first plausible hit. Load the branch reference below.

  Assert:
  - Discovery covers more than one source class and more than one hit.
  - An unavailable modality is reported as unsearched, never as searched.
- [ ] **N3 — Qualify each candidate at the source.**
  `candidate pool -> finalists + rejection ledger | evidence-gap branch`

  Rule: A snippet, title, or metadata record discovers a candidate; it never
  proves a qualification field. Open the official site, repo, or paper and
  record dated observations. Copies of one complaint, and a founder's paper
  plus their demo, are one source lineage. `market` threat claims need the
  four gates in [market](references/market.md); `code` promotes only
  maintained patterns with tests and a compatible lifecycle; `papers` needs
  artifacts and a comparable protocol. Top-k is a ceiling, never a quota.

  Example: `search snippet says the vendor is local + one backordered SKU ->
  unverified or supplier in the rejection ledger, not a direct threat`

  Assert:
  - Every rejected or unverified candidate keeps its failed or unknown field.
  - No blank field is scored as a pass.
- [ ] **N4 — Deep-dive finalists in independent lanes.**
  `finalists -> dossiers with supporting and contrary evidence | parallel-lane branch`

  Rule: With two or more finalists and bounded delegation available, run one
  lane per finalist. Each lane returns observed behaviour, contrary evidence,
  source-specific assumptions, and unknowns. A contradiction updates the
  hypothesis and picks the next discriminating query; a dead end backtracks to
  the best unresolved sibling instead of repeating the query.

  Assert:
  - Each dossier cites exact URLs or files with dates or versions.
  - Anecdotes are not reported as prevalence.
- [ ] **N5 — Decide in the branch's terms.**
  `dossiers + local baseline -> verdict or ranking + downside`

  Rule:
  1. `market`: separate table stakes, differentiation, recurring pain, and
     outliers; recommend one opportunity the local product can act on.
  2. `code`: adopt, adapt, trial, reject, or defer each pattern; recommend the
     smallest local change and the proof that could falsify it.
  3. `papers`: rank experiments by learning value and reproducibility; pick
     the smallest one that separates the live hypotheses, with a falsifier and
     stop condition. Incomparable benchmarks get no numeric ranking.
  4. `synthesis`: cluster overlapping features first, then score and decide
     each per [synthesis](references/synthesis.md); no "maybe".

  Assert:
  - One recommendation, its downside, and what evidence would reverse it.
- [ ] **N6 — Return the evidence note and the next owner.**
  `decision + ledgers -> evidence note + next_owner`

  Rule: Tag every claim with its source class and whether it was opened.
  Route the result: an accepted build to `impl-plan`, a product scope to `prd`,
  an experiment to `ml-autoresearch`, a fuzzy metric to `metric-advisor`.

  Assert:
  - Source fact, synthesis, and recommendation are distinguishable.
  - Unsearched branches and unavailable sources are listed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Citing a source that was only searched, not opened.
- Feature-count matrices hide the customer job; compare outcomes and failure
  modes first.
- A popular repo is not automatically compatible with the local lifecycle, and
  a detached snippet hides setup, cleanup, and failure behaviour.
- Citation count, author fame, and polished demos are discovery signals, not
  validation.
- One impressive source outweighing several that converge on a simpler pattern.

## Reference Map

- [market](references/market.md) - load in N2-N3 for `market`: platform
  query families and the qualification ledger.
- [code](references/code.md) - load in N2-N4 for `code`: literal queries and
  finalist file maps.
- [papers](references/papers.md) - load in N2-N4 for `papers`: researcher
  trails and result normalization.
- [synthesis](references/synthesis.md) - load in N5 for `synthesis`: scoring
  dimensions and the decision table.

## Output

```yaml
branch: market | code | papers | synthesis
decision: <what the evidence must move>
query_ledger: <queries, filters, dates, empty results, unsearched sources>
candidates: <finalists + rejection ledger with failed or unknown fields>
evidence: <claim -> source URL or file, source class, opened yes/no, date>
verdict: <opportunity | local delta + decisions | ranked experiments | decision table>
downside: <what this costs or risks, and what would reverse it>
next_owner: impl-plan | prd | ml-autoresearch | metric-advisor | none
```
