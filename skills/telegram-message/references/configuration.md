# Telegram Configuration

`telegram-message` sends one message to Kenji when local credentials are
available.

Credential rules:

- Read `TELEGRAM_CHAT_ID` from the environment.
- Read `TELEGRAM_BOT_TOKEN` from the environment or macOS Keychain item
  `codex-telegram-bot-token`.
- Never write token values to repo files, session files, logs, or chat output.

If configuration is missing, callers should keep their local artifact, such as
`feedback-request.md`, and report that Telegram delivery was skipped.
