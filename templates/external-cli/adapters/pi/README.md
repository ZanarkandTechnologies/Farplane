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
PI_TELEMETRY=0 pi --model openrouter/moonshotai/kimi-k2.6 --thinking high --skill <skill-path> -p @<prompt-path>
```

Use dry-run mode before live execution. Live model execution may require
provider credentials and spend.
