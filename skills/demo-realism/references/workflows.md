# Demo Realism Workflow

## Primary Workflow

1. **Identify the operator and context**
   - Who uses the product?
   - In what business setting?
   - What day-to-day loop are they already living inside?
2. **Infer the adjacent-tool baseline**
   - What are they plausibly using today?
   - What spreadsheets, dashboards, inboxes, or systems likely surround the workflow?
3. **Choose the pitch-worthy MVP slice**
   - Which narrow slice best shows future-state value in a believable way?
4. **Run the source-artifact ladder when realism depends on concrete inputs**
   - Prefer user-provided or local source files.
   - Search for public, non-password-protected artifacts before inventing
     replacements.
   - Record stable URLs, access notes, artifact type, and whether each artifact
     is `real-public`, `user-provided`, `local-supplied`, or
     `synthetic-fallback`.
   - Use synthetic artifacts only after real sources fail, are sensitive, are
     explicitly out of scope, or are requested by the user.
5. **Build the workflow ladder**
   - Start from the whole story
   - Break into concrete workflows/features
6. **Build the screen/state ladder**
   - For each workflow, list the screens, states, and operational transitions that matter
7. **Build the demo-data pack**
   - entities
   - realistic records
   - timelines
   - statuses
   - edge cases
   - failure/empty states
8. **Score the pack with the realism rubric**
9. **Recommend the next handoff**

## Output Shape

```text
Client operating hypothesis
Pitch-worthy MVP slice
Workflow ladder
Screen/state ladder
Demo-data pack
Source provenance
Realism rubric score
Assumption ledger
Recommended handoff
```

## Example Prompts

### Warehouse Ops

What would a believable warehouse-ops MVP demo look like for a regional
director, assuming the current operation still relies on spreadsheets,
exception inboxes, and one legacy WMS?

### Recruiting CRM

What would a believable recruiting CRM demo look like for hiring managers and
recruiters if the current workflow is still split across email, ATS notes, and
ad hoc spreadsheets?

## Handoff Rules

- use `functional-ui` when the realism pack is strong but the actual workflow
  interaction model still needs product/UI planning
- use `visual-design` when the workflow and data feel believable and visual
  direction should start
- use `frontend-craft` when the workflow and data feel believable and
  implementation should start
- use `impl-plan` when the realism pack should turn into a scoped build plan
- use `impl` only when a ticket already exists and the realism pack is good
  enough to build directly
