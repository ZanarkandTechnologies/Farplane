# Architecture

`desloppify` has one public skill surface and two execution modes:

- `main-agent mode`: the coordinator decides whether cleanup is appropriate,
  checks obvious excludes, and spawns one bounded worker.
- `worker mode`: the delegated worker installs or updates the CLI, runs the
  scan/next/resolve loop, and reports blockers back without recursive
  delegation.

The package stays intentionally small so the first-load contract in
[SKILL.md](../SKILL.md) is enough for normal use.
