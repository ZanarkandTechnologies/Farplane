---
title: Functional UI QA Checklist
owner: functional-ui
status: active
kind: qa-checklist
created_at: 2026-07-02
updated_at: 2026-07-02
applies_to:
  - functional-ui
  - app-screens
  - dashboards
  - workflow-ux
---

# Functional UI QA Checklist

Use this before and after material functional-UI planning for app screens,
panels, dashboards, forms, and control surfaces. Check the planned workflow,
wireframe, screenshot, or implementation handoff. Record violations, then fix
or explicitly defer them with the reason and owner.

```text
functional_ui_qa_checklist(surface, users, workflow_artifact, evidence?)
  -> checklist_verdicts + fixes_or_deferrals + evidence_note
```

## Checks

0. `comparable-evidence-route`
   - Question: For a material, unsettled, current, or SOTA workflow, were 2-4
     comparables or direct products operated with browser evidence covering
     URLs, job/query, sequence, states, access limits, evidence refs, and
     `adopt | adapt | reject` decisions? For a tiny same-pattern fix, settled
     model, or pure visual task, is the skip reason explicit?
   - Violation: The recommendation relies on memory, snippets, vibes, isolated
     screenshots, or Pinterest/gallery taste as functional proof; hidden states
     behind login walls are invented; or a tiny correction is delayed by an
     unnecessary broad research pass.

1. `primary-workspace-priority`
   - Question: Does the main panel or primary workspace take most of the usable
     screen area for the user's core job?
   - Violation: Headers, sidebars, footers, banners, empty decoration, or
     secondary panels dominate the viewport while the actual work area feels
     cramped.

2. `compact-chrome-controls`
   - Question: Are headers, footers, filters, and control bars compact while
     still discoverable and usable?
   - Violation: Navigation, branding, status text, or controls consume space
     needed for the task, repeat the same actions, or push primary content
     below the first viewport without a workflow reason.

3. `balanced-spacing-rhythm`
   - Question: Do panels, sections, cards, lists, forms, and control groups use
     even-looking padding and gaps that make the layout breathe without wasting
     primary workspace?
   - Violation: Padding looks lopsided, cramped, or random; adjacent elements
     use inconsistent spacing without hierarchy; content touches container
     edges; or added padding bloats headers, footers, and controls more than
     the main working area.

4. `readable-information-hierarchy`
   - Question: Can the user quickly identify the current object, state,
     priority, next action, and any blocking condition?
   - Violation: Important labels, values, status, errors, or actions blend
     together; dense data lacks grouping, sorting, filtering, summaries, or
     progressive detail.

5. `responsive-overflow-proof`
   - Question: Does the plan define how long labels, names, table cells,
     numbers, translations, errors, and empty/loading states fit on mobile and
     desktop without text overflow or incoherent overlap?
   - Violation: Text is expected to fit by luck, truncation hides critical
     meaning, controls resize unpredictably, or no wrap/truncate/tooltip/detail
     behavior is specified for realistic content.

6. `honest-and-reversible-actions`
   - Question: Are defaults, labels, destructive actions, subscriptions,
     consent, opt-outs, confirmations, undo paths, and retry/failure states
     honest and reversible where the risk warrants it?
   - Violation: The workflow uses dark patterns, hidden costs, preselected
     consent, confusing cancellation, fake scarcity, misleading hierarchy,
     shame copy, irreversible one-click actions, or disguised ads/promotions.

7. `accessible-input-and-feedback`
   - Question: Can keyboard, touch, screen-reader, and low-vision users
     understand and operate the core workflow with visible focus, labels,
     target sizes, validation, and status feedback?
   - Violation: Essential controls are hover-only, icon-only without labels or
     accessible names, too small for touch, focus order is unclear, errors are
     color-only, or progress/failure feedback is missing.

8. `state-and-edge-case-coverage`
   - Question: Are empty, loading, partial, error, permission, offline,
     unsaved-change, success, and high-volume states included when they can
     affect the user's job?
   - Violation: The happy path is planned but realistic states would break the
     layout, hide the next step, lose data, or strand the user.
   - Required handoff vocabulary: name applicable `empty`,
     `loading/in-progress`, `partial`, `success/return`, `error`, and
     `retry/recovery` behavior rather than relying on a generic "states"
     promise.

9. `workflow-efficiency`
   - Question: Does the interaction model minimize repeated work for common
     tasks through sensible defaults, bulk actions, keyboard/touch shortcuts,
     persistence, and clear return paths?
   - Violation: Users must re-enter known data, navigate through avoidable
     screens, repeat filters, hunt for common actions, or recover context after
     every operation.

## Evidence Note Template

```text
functional_ui_qa:
  surface:
  users:
  workflow_artifact:
  evidence_checked:
  violations:
  fixes_or_deferrals:
```

## Reviewer Prompt

```text
Review the functional UI plan, screenshot, wireframe, or implementation
handoff against skills/functional-ui/qa_checklist.md.

Return one row per checklist item:
- verdict: pass | violation | not_applicable
- evidence: artifact path, screenshot reference, or short UI detail
- fix: smallest required change, or "none"

Focus on workflow usefulness, spatial priority, readability, overflow,
ethical interaction patterns, accessibility, state coverage, and efficiency.
Do not judge visual taste except where it affects functional clarity. Verify
the comparable-evidence route or its explicit skip reason before passing a
material workflow recommendation.
```
