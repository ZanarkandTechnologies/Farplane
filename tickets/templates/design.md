---
template_id: ticket-design-template
template_version: "0.1.0"
ticket_id: TASK-XXXX
title: UI/design proof baseline
status: draft
owner: ticket-workflow
created_at: 2026-06-22
updated_at: 2026-06-22
refs:
  - tickets/TASK-XXXX/ticket.md
---

# TASK-XXXX Design Baseline

Use this file only when layout, interaction, visual design, UI state, canvas
rendering, or taste are part of the ticket proof. Keep it compact enough for QA
and `visual-qa` to compare expected state against captured screenshots.

## Screens / States

| Screen or state | Route / trigger | Expected evidence |
| --- | --- | --- |
|  |  | screenshot, snapshot, trace, or clip |

## Layout Assertions

```json
[
  {
    "element": "primaryCta",
    "expected_bbox_pct": {
      "x": [0, 100],
      "y": [0, 100],
      "w": [1, 100],
      "h": [1, 100]
    },
    "tolerance_pct": 2
  }
]
```

## Interaction Assertions

- Primary action:
- Loading / empty / error state:
- Keyboard / focus:
- Responsive:

## Visual Intent

- Design language:
- Visual hierarchy:
- Spacing / typography:
- Color / contrast:
- Motion / reduced motion:

## Evidence Contract

- `qa-tester` captures:
  - screenshots:
  - snapshot:
  - logs:
- `visual-qa` judges:
  - screens/states:
  - geometry assertions:
  - best evidence image:
- Final response must include:
  - Markdown image link to best screenshot, or blocker reason if absent
  - QA report link
  - visual-qa report link when UI judgment is in scope
