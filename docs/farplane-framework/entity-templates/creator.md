---
template_id: creator-page
template_version: "0.1.0"
feature_refs:
  - FEAT-0075
  - FEAT-0079
kind: entity-page
consumer_scope: wiki
applies_to:
  - .farplane/entities/*.md (pages with roles [creator])
---

# Creator page template

A creator's Wiki page reads like a short wiki article, not a log: a lede, their
top ideas grouped under fixed themes, and their real stories. It is a cache of
what they repeat most, capped at 100 claims and 50 stories (the YouTube bridge
merges each video in and evicts the least-cited lines); every video's full
detail stays in its dossier.

Rules:

- Use the themes below, in this order, and only the ones with lines; a page may
  add at most two niche themes under `## Claims` when the creator needs them.
- Every line is one idea ending in its `[video@m:ss](url)` citations. A repeated
  point gains a citation on its line; a new specific rewrites the line; only a
  genuinely new point adds a line.
- The theme comments name the skills an idea there would level up; they are a
  guide, not a rule.

```markdown
---
id: {{id}}
kind: person
name: {{name}}
roles:
  - creator
---

# {{name}}

{{lede: 3–5 sentences on who they are and what they keep coming back to}}

## Claims

### Audience and content
<!-- social-content, storyboard, copywriting-advisor -->

### Offers and sales
<!-- review-offer, copywriting-advisor, personalized-offer -->

### Outreach and relationships
<!-- first-value-outreach, review-leads, customer-research -->

### Strategy and money
<!-- review-model, feasible-roadmap, advise -->

### Fundraising and deals

### Running a company
<!-- hiring, operations, pm -->

### Mindset

## Stories

### Background

### Their business
<!-- milestones, numbers, products: their own business over time -->

### People they work with

### Case studies
<!-- one line each: who · before → after · what changed · citation -->

## Videos covered
```
