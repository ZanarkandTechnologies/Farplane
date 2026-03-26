# Codex Harness PRD

## Goal

Turn this live `~/.codex` directory into a safe, portable Git-backed harness repo for reusable Codex configuration.

## In Scope

- version reusable skills, agents, rules, scripts, and repo operating docs
- document the safe bootstrap flow for cloning directly into `~/.codex` or installing from another path
- keep secrets and machine-local state out of Git by default

## Out of Scope

- committing auth/session/log/sqlite state
- auto-generating per-machine `config.toml` values
- creating or pushing a remote repository without a user-provided remote URL
