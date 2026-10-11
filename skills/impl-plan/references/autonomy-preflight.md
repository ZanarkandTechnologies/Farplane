# Autonomy Preflight

Load this at Todo step 6, when filling the ticket's `Autonomy Preflight` so the
approved run can go unattended. The ticket template owns the section's shape;
this reference owns how the planner fills it.

## Probe, Do Not Assume

Fill the section from probes actually run:

- CLI auth: `gh auth status`, `farplane doctor`, `farplane run -- true`.
- Required secret names are present. Never print or request their values.
- Storage: free disk or volume space against the run's expected outputs
  (checkpoints, logs, media), so a long run cannot fail on save.
- A bounded dev server start: run it in the background, wait for the port with
  a timeout, then stop it.
- Each site the run touches, reached in the built-in browser, else the
  logged-in browser, else desktop control.

## Render All Seven Lines

Render exactly these seven labeled lines even when probes cannot run:
`Target and floor`, `Choose by`, `Will do myself`, `Checks I run`,
`Blockers (probed)`, `Needs you before AFK`, and `Interrupt only for`. When the
ticket cannot be written, render the same seven lines in the visible handoff.

- `Target and floor` names the deadline, the target, and the floor: the
  smallest result worth returning to if the target slips. The ticket's Done
  checks the floor, so a run never ends below it while a route remains.
- `Choose by` is fixed: expected value in money. Count the goal reached
  sooner, operator hours included, minus spend and expected loss (likelihood
  times cost of what could break). Below the cap, waiting to save a few
  dollars loses.

- `Blockers (probed)` always includes an `auth` row (`gh auth status`, the
  secret manager's login check), a `secrets` row naming each required secret
  and whether it is present (names only), a `dev server` row with its bounded start
  command, and a `browser` row listing built-in browser -> logged-in browser ->
  desktop control, each with its result or "not run: reason".
- Under `Blockers (probed)`, write one sub-bullet per dependency, never one
  combined line: `dependency -> probe command -> result or "not run: reason"
  -> fix or fallback`. The browser fallback is built-in browser -> logged-in
  browser -> desktop control; the browser row names each rung tried with its
  result. Fix a blocker now when allowed. A blocker the agent can clear itself
  (dependency install, server start, test-mode config) goes under `Will do
  myself`, not `Needs you before AFK`.
- List every QA check as one the agent runs itself.
- `Interrupt only for` is fixed: reputational harm, spend over the cap, or
  irreversible loss of the operator's data, meaning anything with no other
  copy; checkpoints, caches, and build artifacts are regenerable. A missing login or tool is a
  blocker to clear before AFK, not an interrupt.

## Permissions And Approval

Read standing permissions and the spend cap from the operator profile; never
copy the cap or credentials into the ticket. `Needs you before AFK` holds only
platform-limited or over-cap items: logins, account creation, CAPTCHAs, OAuth
grants, and over-cap spend. Plan approval and config the agent can find are
never `Needs you` items; never ask to confirm an action standing permissions
already allow. Call the plan `approval_ready` only when that list is empty and
no blocker is unresolved, or the operator accepted them in this conversation;
otherwise label it `approval: pending` and name what is open.
