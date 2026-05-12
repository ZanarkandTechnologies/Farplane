# Board Adapter Conformance

Status: Draft v1

Purpose: Define the smallest proof a filesystem, Linear, Notion, GitHub, or
custom board adapter must provide before Codexter treats it as a real work-item
source.

## Core Rule

Board adapters store and normalize work. They do not decide that Codexter should
start work.

Execution starts only after an explicit invocation produces a
`CodexterRunEnvelope`. The adapter then reads one selected item, returns a
normalized `WorkItem`, and writes evidence only through explicit, traceable
writeback behavior.

## Non-Goals

- No polling loop.
- No webhook listener.
- No external board client in this conformance scaffold.
- No automatic transition from board state to agent execution.
- No silent evidence or state writeback.
- No credentials in prompts, fixtures, or ticket frontmatter.

## Adapter Contract

Every adapter must provide these behaviors:

```ts
type BoardAdapter = {
  kind: "filesystem" | "linear" | "notion" | "github" | string;
  listCandidates(filter: CandidateFilter): WorkItemSummary[];
  readWorkItem(selector: WorkItemSelector): WorkItem;
  writeEvidence(item: WorkItemRef, evidence: EvidencePatch): WriteResult;
  transitionState?(item: WorkItemRef, transition: StateTransition): WriteResult;
  normalize(raw: unknown): WorkItem;
};
```

The live Python v1 surface is intentionally smaller:

- `bin/codexter_boards.py / FileTicketAdapter.list_candidates(...)`
- `bin/codexter_boards.py / FileTicketAdapter.read_work_item(...)`
- `bin/codexter_boards.py / FileTicketAdapter.write_evidence(...)`
- `bin/codexter_boards.py / normalize_ticket(...)`

Future adapters may use different transport code, but they must return the same
normalized shape and preserve the same invocation boundary.

## Normalized Work Item

Conformance focuses on the fields that downstream routing and proof rely on:

```ts
type WorkItem = {
  source: string;
  id: string;
  identifier: string;
  title: string;
  description: string;
  state: string;
  phase: string;
  status: string;
  priority: string | number;
  labels: string[];
  blockedBy: string[];
  dependsOn: string[];
  ready: boolean;
  approvalRequired: boolean;
  requiresQa: boolean;
  requiresDemo: boolean;
  computeTarget?: "local_shared" | "local_worktree" | "symphony" | "codex_cloud";
  localTicketPath?: string;
  artifactsPath?: string;
  url?: string;
  metadata: Record<string, unknown>;
};
```

Required semantics:

- `ready` means eligible after invocation, not "run now."
- `approvalRequired` blocks non-planning phases until cleared.
- `blockedBy` and `dependsOn` must be normalized into stable references.
- `computeTarget` is an admission request, not a launcher.
- `source`, `identifier`, and `url` or `localTicketPath` must be enough for
  proof and logs to point back to the original work item.

## Conformance Case Shape

Each adapter should have at least one fixture like this:

```ts
type AdapterConformanceCase = {
  source: "filesystem" | "linear" | "notion" | "github";
  rawFixture: string | Record<string, unknown>;
  expectedWorkItem: {
    source: string;
    identifier: string;
    title: string;
    status: string;
    phase: string;
    ready: boolean;
    approvalRequired: boolean;
    blockedBy: string[];
    dependsOn: string[];
    computeTarget?: string;
  };
  writeExpectation: "manual" | "traceable_write" | "unsupported";
};
```

The fixture should prove:

1. The adapter rejects selectors outside its configured source.
2. The adapter returns a `WorkItem` with the fields above.
3. The adapter preserves blockers, dependencies, approval, and readiness.
4. The adapter never treats readiness or status as an invocation trigger.
5. Evidence writeback either returns a traceable `WriteResult` or an explicit
   manual/unsupported result.

## Filesystem Baseline

The filesystem adapter is the reference implementation today:

- Source: `tickets/TASK-*/ticket.md`
- Adapter: `FileTicketAdapter`
- Conformance test: `bin/test_codexter_boards.py`
- Evidence writeback: manual in v1

Expected filesystem behavior:

- A ticket path must point to `ticket.md`.
- A ticket path must stay under the configured board source.
- `ticket_id` must match `TASK-####`.
- `compute_target` must be one of the supported compute targets.
- `write_evidence(...)` must not silently mutate the ticket in v1; it returns a
  manual writeback result.

## Future Adapter Checklist

Before making a new adapter discoverable:

- [ ] Add one raw fixture with realistic source payload shape.
- [ ] Add one conformance test that produces the expected `WorkItem`.
- [ ] Prove selectors cannot escape the configured source or project scope.
- [ ] Prove `ready`, status, labels, blockers, dependencies, approval, QA, and
  demo flags normalize predictably.
- [ ] Prove `computeTarget` remains an admission request and does not launch
  external compute.
- [ ] Prove evidence writeback returns a `WriteResult` with a path or URL a
  reviewer can inspect.
- [ ] Document credential handling and keep tokens out of prompts, fixtures,
  logs, and ticket metadata.
- [ ] Document which explicit trigger source creates the
  `CodexterRunEnvelope`.

## AI Misread Risks

Agents implementing adapters are likely to misunderstand these points:

- A board item becoming `ready` is not an invocation.
- A ticket comment such as `@codexter implement` is not handled by Codexter
  unless an external caller converts it into an envelope.
- `writeEvidence` is not permission to edit arbitrary ticket fields.
- `transitionState` is optional and must not become hidden orchestration.
- `symphony` and `codex_cloud` compute targets are blocked locally until real
  adapters exist.
- Linear, Notion, and GitHub fixtures must not include real tokens or private
  payloads.

When in doubt, keep the adapter read-only and return a manual writeback result.

## Verification

Current core checks:

```bash
python3 -m unittest bin/test_codexter_boards.py
python3 -m unittest bin/test_codexter_invocation.py
python3 -m unittest bin/test_codexter_compute.py
```

Future adapter checks should add adapter-specific tests beside the adapter and
still run the conformance assertions against the returned `WorkItem`.
