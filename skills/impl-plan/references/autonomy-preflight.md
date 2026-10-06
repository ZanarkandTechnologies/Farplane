# Autonomy Preflight

Load this at Todo step 6, when filling the ticket's `Autonomy Preflight` so the
approved run can go unattended. The ticket template owns the section's shape;
this reference owns how the planner fills it.

## Probe, Do Not Assume

Fill the section from probes actually run:

- CLI auth: `gh auth status`, `farplane doctor`, `farplane run -- true`.
- Required secret names are present. Never print or request their values.
- A bounded dev server start: run it in the background, wait for the port with
  a timeout, then stop it.
- Each site the run touches, reached in the built-in browser, else the
  logged-in browser, else desktop control.

## Render All Five Lines

Render the five lines even when probes cannot run: `Will do myself`,
`Checks I run`, `Blockers (probed)`, `Needs you before AFK`, and
`Interrupt only for`.

- Under `Blockers (probed)`, write one sub-bullet per dependency, never one
  combined line: `dependency -> probe command -> result or "not run: reason"
  -> fix or fallback`. The browser fallback is built-in browser -> logged-in
  browser -> desktop control. Fix a blocker now when allowed.
- List every QA check as one the agent runs itself.
- `Interrupt only for` is fixed: reputational harm, spend over the cap, or
  irreversible loss of the operator's data. A missing login or tool is a
  blocker to clear before AFK, not an interrupt.

## Permissions And Approval

Read standing permissions and the spend cap from the operator profile; never
copy the cap or credentials into the ticket. `Needs you before AFK` holds only
platform-limited or over-cap items. `approval_ready` requires that list empty
or explicitly accepted.
