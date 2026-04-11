# Demo Realism Architecture

## Purpose

`demo-realism` exists because believable MVP demos fail before final design when
the agent never models how the client plausibly operates, which workflows matter
most, or what realistic data/state would make the result feel presentable.

## Core Decisions

- **Aggressive inference is allowed**
  - The goal is pitch-worthy potential, not an exact carbon copy of the client's
    current operation.
- **Realism sits upstream of design/build**
  - This skill owns believable operating context, not final UI execution or implementation.
- **The output is hierarchical**
  - app slice -> workflow -> screen/state -> data pack
- **Believability beats generic completeness**
  - A smaller, credible MVP slice is better than a broad but obviously fake demo.

## Boundaries

- not factual client research
- not final visual design
- not implementation planning by default
- not a review-only skill

## Why Not Extend Existing Skills

- `functional-ui` focuses on user stories, comparable apps, and workflow choice
  after the product shape is already the main question
- `review` judges work after it exists; it does not generate believable examples
- `demo-realism` fills the missing synthesis layer between vague product idea and
  downstream workflow/design/build work
