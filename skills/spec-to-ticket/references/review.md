# Spec-To-Ticket Review

Run this review before handing off the ticket set.
If any answer is weak, tighten the tickets first.

## Must Pass

- Is each ticket small enough for one build loop by default?
- Is overflow scope split into follow-up tickets instead of hidden in prose?
- Are dependencies explicit and ordered cleanly?
- If a ticket uses a library, package, service, or tool, is that dependency named where relevant?
- Do acceptance criteria explain the minimum necessary change clearly?
- For UI-bearing tickets, do `Agent Contract` and `Evidence checklist` make QA realistic?
- Does each non-trivial ticket declare a usable `Test hook`, not just vague “verify manually” language?
- If delegation is expected, does `Delegate with` point to the exact ticket path/section and write-back target?
- For UI-bearing tickets, is the intended layout or screen structure clear enough to review later without guessing?

## Ask If Relevant

- Are we trying to do too much in one ticket?
- Did we include the minimum amount of code or interface detail needed to explain the change?
- Are the tickets convincing enough for approval without becoming bloated?
- Are we saying too much, or too little, for an agent to execute reliably?
- Did we call out any instrumentation work needed for difficult UI or runtime verification?
- Are we defining proof in the cheapest deterministic way, for example a CLI check, seed path, debug route, or sanity script?
- For UI work, is the design intent readable for a human reviewer rather than only executable by an agent?
- Are we reusing existing shared UI patterns/libraries where possible instead of silently inventing another one?

## Fail If

- one ticket clearly hides multiple build loops
- dependency order is implied instead of stated
- a UI ticket says "verify in browser" without access/stabilization details
- a non-trivial ticket needs deterministic setup but has no usable `Test hook`
- acceptance criteria are generic, fluffy, or not observable
- important dependencies or packages are assumed but never named
- delegated work is described only in prose without an exact ticket reference
