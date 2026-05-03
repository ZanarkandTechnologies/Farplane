# Autoresearch Plan Architecture

`autoresearch-plan` owns session setup only.

Inputs:

- user goal
- repo context
- editable scope
- metric and verify candidates
- optional guard and iteration limit

Outputs:

- `autoresearch.md`
- `autoresearch.sh`
- optional `autoresearch.checks.sh`
- `autoresearch.jsonl` config header
- optional `autoresearch.ideas.md`

Execution belongs to `autoresearch-exec`. Ticketed implementation belongs to
`impl-plan` and `$impl`. Short same-session retry loops belong to `$loop`.

