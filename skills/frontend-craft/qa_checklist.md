---
title: Frontend Craft QA Checklist
owner: frontend-craft
status: active
kind: qa-checklist
created_at: 2026-06-15
updated_at: 2026-06-15
applies_to:
  - frontend
  - ui
  - app-screens
---

# Frontend Craft QA Checklist

Use this after material frontend implementation, UI copy changes, or visual QA
repairs before claiming the surface is ready. Run each check against the actual
rendered UI evidence and the changed source files. Record violations, then fix
or explicitly defer them with a reason.

```text
frontend_qa_checklist(changed_files, rendered_evidence, audience, surface?)
  -> checklist_verdicts + fixes_or_deferrals + evidence_note
```

## Checks

1. `audience-copy-fit`
   - Question: Does visible UI copy speak to the real audience and task on this
     screen?
   - Violation: The UI explains implementation details, environment variables,
     local commands, framework plumbing, or feature rationale to a user who is
     trying to operate the product.

2. `no-developer-explainer-paragraphs`
   - Question: Are long explanatory paragraphs absent from normal app chrome,
     dashboards, toolbars, cards, and HUDs unless the screen is explicitly a
     docs, settings, onboarding, or developer-console surface?
   - Violation: The UI contains prose such as "requires X env vars", "uses the
     local bridge", "this feature routes to...", or command setup text in the
     main workflow instead of the right help surface.

3. `help-affordance-routing`
   - Question: If extra explanation is useful, is it routed to the right
     affordance: tooltip, info popover, docs link, inline validation message,
     empty-state action, copyable command block, or setup panel?
   - Violation: Background explanation is permanently visible where a concise
     label, status, icon button, tooltip, or "learn more" affordance would
     preserve workflow focus.

4. `tooltip-accessibility`
   - Question: Tooltips or popovers have a visible trigger, work by keyboard or
     focus where relevant, are not the only place for essential instructions,
     and use accessible names/descriptions.
   - Violation: Help only appears on hover, hides required setup information
     from keyboard/touch users, or uses an unlabeled icon.

5. `copy-density`
   - Question: The screen can be scanned quickly, with labels and status text
     doing most of the work.
   - Violation: UI copy reads like README prose, release notes, implementation
     notes, or a developer handoff.

6. `surface-exception-explicit`
   - Question: Technical copy that remains visible belongs to an explicit
     technical surface, such as settings, diagnostics, setup, logs, or a
     developer console.
   - Violation: Technical setup text appears in a primary product view without
     a surface-level reason.

7. `rendered-copy-checked`
   - Question: QA inspected rendered screenshots or DOM text, not just source
     diffs.
   - Violation: The check relies only on code review and misses text assembled
     at runtime.

8. `source-copy-search`
   - Question: Source search covered likely explainer terms when this risk is
     in scope.
   - Violation: No targeted search was run for terms such as `requires`,
     `configured`, `gateway`, `env`, `npm run`, `local bridge`, `thread id`,
     `routes to`, or product-internal feature explanations.

## Acceptable Exceptions

- Developer/operator settings pages can show commands, env vars, local service
  status, and setup requirements when that is the job of the screen.
- Empty states can explain what is missing when the explanation immediately
  helps the user take the next action.
- Diagnostics and logs can expose technical details, but should still separate
  summary, action, and details.
- A tooltip is not enough for essential setup or destructive-action context;
  those need visible labels, validation, confirmation copy, or a setup panel.

## Evidence Note Template

```text
frontend_copy_qa:
  audience:
  surfaces_checked:
  rendered_evidence:
  source_search:
  violations:
  fixes_or_deferrals:
```

## Subagent QA Prompt

Use this prompt when a QA lane checks frontend copy and help affordances:

```text
Review the changed UI against skills/frontend-craft/qa_checklist.md.

Focus on whether visible UI copy is audience-facing, whether developer-facing
implementation prose leaked into normal product screens, and whether optional
explanations are routed to tooltips, popovers, docs links, setup panels, or
validation messages.

Return one row per checklist item:
- verdict: pass | violation | not_applicable
- evidence: screenshot/DOM/source path plus short quote or selector
- fix: smallest product-facing change, or "none"

Do not judge visual taste except where copy density or help placement harms the
workflow.
```
