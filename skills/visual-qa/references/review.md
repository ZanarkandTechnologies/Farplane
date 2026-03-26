# Visual QA Review

Run this review before handing off the QA verdict.
If any answer is weak, tighten the report first.

## Must Pass

- Did we follow the project's star rating guide or equivalent taste standard when relevant?
- Did we check the intended layouts and screen structure, not just route completion?
- Did we remove or call out visual artifacts that should not be present in the UI?
- Does the screen look clean, tidy, and intentional?
- Does the screen feel minimal and readable for a human, not bulky or overloaded?
- Are there unexpected UI elements on the board or screen?
- Is extra explanatory information shown inline when it should probably live in a tooltip or lighter affordance?
- Are we using the right components for the job, instead of generic or mismatched ones?
- If a shared UI library or existing pattern should have been used, did we call out where the implementation drifted?
- Did the report call out both visual diffs and behavior diffs where relevant?

## Ask If Relevant

- Does spacing feel dense and deliberate rather than bulky or empty?
- Are there default-styled remnants, placeholder artifacts, or debug leftovers?
- Is any panel, card, or label heavier than it needs to be?
- Is the UI trying to explain too much directly instead of using progressive disclosure?
- Are there duplicated patterns or component variants that should probably collapse into one shared treatment?
- If the screen was planned from an explicit layout sketch or strong reference, did the output preserve that structure?
- Does the final evidence actually show the most important user-facing surface?

## Fail If

- the QA report does not judge against declared screens/states
- layout quality is hand-waved instead of checked
- visible artifacts, clutter, or wrong components are ignored
- bulky, plain, or default-looking UI is accepted without comment
- the report says "looks good" without concrete evidence
- the output would not help implementation fix the problem quickly
