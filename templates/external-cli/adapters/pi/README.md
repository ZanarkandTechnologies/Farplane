# Pi Adapter

Adapter contract for Mario Zechner's Pi coding agent.

## Expected Executable

```bash
pi
```

Install hint:

```bash
npm install -g @mariozechner/pi-coding-agent
```

## Command Shape

```bash
PI_TELEMETRY=0 pi --model openrouter/moonshotai/kimi-k2.6 --thinking high --skill <skill-path> -p "$(cat <prompt-path>)"
```

`@file` attaches a file to Pi; it does not make the file contents the
instruction message. The Farplane launcher must pass the rendered prompt text as
the `-p` message and reserve `@...` only for attachments.

Use dry-run mode before live execution. Live model execution may require
provider credentials and spend.
