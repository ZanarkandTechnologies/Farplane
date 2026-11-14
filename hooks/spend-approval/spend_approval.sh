#!/bin/sh
# PreToolUse (Bash): a Modal run, deploy, serve or shell (each can build images and rent GPUs) needs Kenji's
# one-time code first (Kenji, 11 Nov 2026: $171 of unapproved Modal research and $69 of failed image builds in a week).
# approve.py sends the code to Kenji's phone only; `approve.py grant <code>` opens a time-boxed window.
# A request of $1 or less opens the window at once (Kenji, 14 Nov 2026), up to $10 a day.
# Plain sh: a Bash call without "modal" or "release.sh" spawns nothing.

IFS= read -r payload || [ -n "$payload" ] || exit 0
case $payload in *'"tool_name":"Bash"'* | *'"tool_name": "Bash"'*) ;; *) exit 0 ;; esac
case $payload in *modal* | *release.sh*) ;; *) exit 0 ;; esac
input=$(printf '%s' "$payload" | sed -e 's/.*"tool_input"//' -e 's/\\[nt]/ /g')
# the approval script itself and read-only Modal commands pass
case $input in *spend-approval/approve.py*) exit 0 ;; esac
# release.sh counts only when it is run (sh/bash, ./, or first word), not when a command reads or names it
printf '%s' "$input" | grep -Eq -e '\bmodal +(run|deploy|serve|shell)\b' \
  -e '(\b(sh|bash|zsh) +(-[a-z]+ +)*|-- +|[;&|(] *|"command": ?" *)(\./)?([A-Za-z0-9_.~/-]*/)?deploy/release\.sh' || exit 0

grant="${FARPLANE_APPROVALS:-$HOME/.farplane/approvals}/grant"
if [ -f "$grant" ]; then
  until=$(sed -n 1p "$grant")
  now=$(date +%s)
  case $until in '' | *[!0-9]*) ;; *) [ "$until" -gt "$now" ] && exit 0 ;; esac
fi

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Modal spend needs Kenji'"'"'s approval code (Modal run/deploy/serve/shell can build images and rent GPUs). Run: python3 ~/.claude/farplane/hooks/spend-approval/approve.py request \"<what and why>\" --usd <max dollars> --minutes <how long>. Ask for the leanest run that answers the question (one room, one GPU, a cached image), never a large budget. At $1 or less (up to $10 a day) it approves itself and you can rerun at once. Otherwise it sends a 6-digit code to Kenji'"'"'s phone only: ask Kenji for the code in chat, then run: python3 ~/.claude/farplane/hooks/spend-approval/approve.py grant <code>. Never guess the code or edit the approvals folder."}}'
