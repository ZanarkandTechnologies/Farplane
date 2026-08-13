# Architecture

`functional-ui` owns the functional shape of UI:

- users and jobs,
- current UI diagnosis,
- comparable workflow patterns,
- interaction model,
- screen/state map,
- planning handoff and optional low-fi wireflow.

It feeds `impl-plan`, which resolves any remaining visual or asset context. It
does not own final visual taste, ticket composition, or code implementation.
