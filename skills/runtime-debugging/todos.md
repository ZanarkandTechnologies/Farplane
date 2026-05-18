# Todos

- [ ] Capture the exact symptom, repro path, scope, and success criteria before proposing a fix.
- [ ] Map the relevant codepath, side-effects, and current observability surface.
- [ ] State a small set of falsifiable hypotheses and what evidence would separate them.
- [ ] Add the minimum instrumentation or repro harness needed to learn something real.
- [ ] Reproduce and collect runtime evidence before patching.
- [ ] If the issue is really browser-first or visual, stop and hand off to the
  visual QA owner rather than forcing runtime debugging.
- [ ] Apply the smallest fix that matches the observed root cause.
- [ ] Re-run the repro and report exact proof that the fix worked.
- [ ] Note whether another skill such as `testing` or `visual-qa` should take over next.
