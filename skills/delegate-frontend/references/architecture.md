# Delegate Frontend Architecture

`delegate-frontend` is a profile entrypoint over `delegate-cli`.

It does not own a separate launcher or artifact contract. It selects
`frontend-pi-kimi` and keeps frontend-specific readiness checks close to the
frontend skill topology.
