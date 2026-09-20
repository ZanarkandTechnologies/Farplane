# Company OS Automation Template

Use this shape for the paired Daily and Weekly cron records. The prompt must
bind concrete source paths and output paths rather than copying reasoning rules
from the skill.

```text
Use $pm-daily | $pm-weekly.

1. Fetch the bounded provider and project context; freeze sources and coverage.
2. Cache exact local inputs with IDs, revisions, timestamps, URLs, and hashes.
3. Run the owning skill against local files only; require one exact JSON output.
4. Validate, render reports or memory, apply authorized existing-issue actions,
   reread before mutation, and read back every effect.

Do not create or execute tickets, invent strategy, promote broad knowledge, or
perform external side effects.
```
