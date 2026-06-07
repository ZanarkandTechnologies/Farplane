# Demo Realism Rubric

Use this rubric before handing off the realism pack downstream.

## Dimensions

### 1. Operational Plausibility

- `1`: feels fictional and detached from real work
- `3`: plausible at a high level, but still generic
- `5`: strongly feels like a believable operational workflow

### 2. Workflow Believability

- `1`: workflows are abstract or product-marketing-shaped
- `3`: workflows are coherent but still thin on day-to-day detail
- `5`: workflows feel like they come from a real operator's routine

### 3. Data Realism

- `1`: generic placeholder rows or labels
- `3`: data is shaped correctly but still emotionally fake
- `5`: records, statuses, timelines, and edge cases feel presentable to a real client

### 4. Source Provenance

- `1`: realism-critical artifacts are synthetic, unattributed, or masquerading
  as real
- `3`: provenance is stated, but real public/user-provided sourcing was thin or
  synthetic fallback still carries the demo
- `5`: source-critical artifacts are real public, user-provided, or local
  supplied where possible, with clear URLs/access notes and fallback labels

### 5. Presentation-Worthiness

- `1`: would undermine trust in the product
- `3`: safe enough to discuss, but not strong enough to pitch confidently
- `5`: strong enough to support a credible client demo or MVP walkthrough

### 6. Client-Fit Inference Quality

- `1`: inference ignores likely industry context
- `3`: inference is directionally right but still broad
- `5`: inference feels appropriately targeted to the client type without claiming verified truth

## Pass Rule

The realism pack is ready for downstream handoff only when:

- no dimension is below `3`
- `presentation-worthiness` is at least `4`
- `data realism` is at least `4`
- `source provenance` is at least `4` when the demo depends on concrete
  documents, media, forms, records, blueprints, logs, invoices, regulations, or
  other real-world source artifacts

## Reviewer Questions

- Would a real client immediately dismiss this as fake?
- Do the workflows imply a believable day-to-day operating loop?
- Do the records, statuses, and edge cases feel like they came from operations rather than lorem ipsum?
- Were source-critical artifacts real public, user-provided, or locally
  supplied before synthetic fallback was used?
- Are all synthetic artifacts clearly labeled as fallback rather than treated
  as proof?
- Does the pack show a strong future-state pitch without pretending to be exact current-state truth?
