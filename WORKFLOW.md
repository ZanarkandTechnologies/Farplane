---
workflow:
  name: codexter-invocation
  version: 1

board:
  adapter: filesystem
  source: tickets/
  active_phases: ["planning", "building", "documenting"]
  terminal_statuses: ["done", "failed"]

compute:
  default: local_shared
  allowed: ["local_shared", "local_worktree"]
  ticket_override_field: compute_target

routing:
  planning: impl-plan
  building: impl
  qa: qa
  review: review
  documenting: close-ticket

quality:
  requires_ticket_evidence: true
  requires_review: true
  requires_qa_from_ticket: true
  writes_proof_packet: true
---

# Codexter Invocation Workflow

Use this file as the repo-local invocation policy for Codexter-equipped Codex.
Do not duplicate detailed skill contracts here. A run should load one
`CodexterRunEnvelope`, normalize one work item, select allowed compute, route to
the existing phase skill, and write the requested `ProofPacket`.

Codexter is normal Codex with this repository's installed skills, hooks,
templates, and proof conventions. This workflow is not a daemon and not a
standalone `codexter run` CLI.
