# Demo Realism Gotchas

## High-Risk Failure Modes

- **Generic mock-data theater**
  - Swapping in slightly better names or labels is not enough if the workflows,
    statuses, and timelines still feel fake.
- **Synthetic source substitution**
  - When public or user-provided source artifacts would make the demo real,
    inventing a similar-looking document, blueprint, policy, log, or dataset is
    a realism failure, not harmless scaffolding.
- **Design-first drift**
  - Jumping into polished UI language before the operating model is believable
    creates prettier but still fake demos.
- **Client-truth overclaim**
  - The output may be plausible without being verified. Do not present inferred
    context as established fact.
- **Flat decomposition**
  - Going straight to screens without a strong workflow ladder usually produces
    shallow states and weak data.
- **Data without operations**
  - A data pack that is not tied to operator actions, transitions, and edge
    cases will still feel synthetic.

## Recovery Moves

- If the app feels fake, step back from screens to workflow.
- If the workflow feels fake, step back from workflow to operator context.
- If the data feels fake, trace each entity back to a real operational event.
- If a source artifact feels fake, search for public or user-provided material,
  record provenance, and only then use a clearly labeled synthetic fallback.
