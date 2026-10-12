# Realism Pack

Load this in `prd` realism mode when a prototype or MVP demo feels fake and
needs a believable operating model, demo data, and a build-ready handoff. The
goal is pitch-worthy future-state potential, not a reconstruction of the
client's exact current tooling.

## Ladder

Work top-down; do not jump to screens while the workflow is still vague.

1. **Operator and context:** who uses it, in what business setting, inside
   which day-to-day loop.
2. **Adjacent-tool baseline:** the spreadsheets, inboxes, dashboards, or legacy
   systems that plausibly surround the workflow today.
3. **Pitch-worthy MVP slice:** the narrow slice that best shows future-state
   value believably. A smaller credible slice beats a broad, obviously fake one.
4. **Decision mechanism** (operational recommendation demos only): the one
   recurring decision, the retrieval, calculation, optimization, rule, or state
   transition that owns the result, and the ordinary, constrained, and
   changed-condition cases that should alter it. See the
   [Mine-To-Margin reference standard](../../approach/references/mine-to-margin-reference-standard.md).
5. **Source-artifact ladder** (documents, media, forms, records, blueprints,
   logs, invoices, regulations, or other concrete inputs):
   public non-password-protected artifacts with stable URLs first, then
   user-provided or local files, then synthetic only when real sources are
   unavailable, sensitive, out of scope, or explicitly requested. Label every
   artifact `real-public | user-provided | local-supplied | synthetic-fallback`
   and record URL, access note, and artifact type.
6. **Workflow ladder:** whole story -> concrete workflows/features.
7. **Screen/state ladder:** per workflow, the screens, states, and operational
   transitions that matter.
8. **Demo-data pack:** entities, realistic records, timelines, statuses, edge
   cases, empty and failure states, each traced to a real operational event.
9. **Score** with [realism-rubric.md](realism-rubric.md).

## Branches

- Thin context: infer aggressively from industry norms and adjacent tools; say
  it is inference, never verified client truth.
- Rich context: preserve supplied operator detail and fill only obvious gaps.
- Product shape still abstract: stay at app/workflow decomposition.
- Shape believable but data fake: stay on the data pack and rubric.

## Output Shape

```text
Client operating hypothesis
Pitch-worthy MVP slice
Workflow ladder
Screen/state ladder
Demo-data pack
Decision mechanism and responsive proof cases   (operational recommendation demos)
Source provenance
Realism rubric score
Assumption ledger
Recommended handoff
Expectation-check artifact required             (demo-bearing build or review)
```

## Expectation-Check Artifact

Every demo-bearing build or review handoff names this artifact; the downstream
worker fills it before Kenji Review instead of reporting bare success.

```text
Demo expectation check
Source realism pack:
Demo-bearing feature:
Realistic data exercised:   concrete records, scenarios, source artifacts, or a named demo pack
Workflow exercised:         an action sequence, not a screen list
Mechanism exercised:        the tool, rule, solver, retrieval, or state transition that produced the output
Expected demo value:
Observed result:            what actually happened
Mismatch notes:             gaps, or `none observed`; never omitted
Evidence:                   screenshots, logs, command or fixture output, artifacts, or a blocker report
Operator question:          does this observed result match the expected demo value? (name feature and workflow)
Provenance and limits:      provenance labels; synthetic data stays `synthetic-fallback`, never real-world proof
```

## Recovery Moves

- App feels fake: step back from screens to workflow.
- Workflow feels fake: step back to operator context.
- Data feels fake: trace each entity to a real operational event.
- Source artifact feels fake: search public or user-provided material, record
  provenance, and only then use a labelled synthetic fallback.
- Demo-bearing feature lacks an expectation check: create one from the shape
  above before asking for review.

## Example Prompts

- A warehouse-ops MVP demo for a regional director whose operation still runs
  on spreadsheets, exception inboxes, and one legacy WMS.
- A recruiting CRM demo for hiring managers whose workflow is split across
  email, ATS notes, and ad hoc spreadsheets.
