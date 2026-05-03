# Autoresearch Exec Architecture

`autoresearch-exec` owns the measured experiment loop.

Inputs:

- `autoresearch.md`
- `autoresearch.sh`
- optional `autoresearch.checks.sh`
- `autoresearch.jsonl`
- editable scope and git history

Outputs:

- experiment commits for kept changes
- revert commits for discarded changes when possible
- appended JSONL run entries
- updated session memory when learnings matter

This skill is intentionally local and artifact-driven. It does not own tickets,
worker lanes, dashboards, recurring automation, or hidden runtime dispatch.

