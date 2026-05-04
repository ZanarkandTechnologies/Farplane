# Delegate CLI Skill Rules

- Keep `delegate-cli` generic; profile-specific taste or model behavior belongs
  in profile templates or profile skills.
- Treat external CLIs as delegated builder lanes only.
- Keep generated runtime bundles under `.harness/external-cli/`.
- Keep ticket evidence under `tickets/TASK-*/artifacts/external-cli/`.
- Do not add a new adapter without a dry-run test.
