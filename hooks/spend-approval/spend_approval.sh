#!/bin/sh
# PreToolUse (Bash): a Modal run, deploy, serve or shell (each can build images and rent GPUs) needs Kenji's
# one-time code first (Kenji, 11 Nov 2026: $171 of unapproved Modal research and $69 of failed image builds in a week).
# approve.py sends the code to Kenji's phone only; `approve.py grant <code>` opens a time-boxed window.
# Plain sh: a Bash call without "modal" or "release.sh" spawns nothing.

IFS= read -r payload || [ -n "$payload" ] || exit 0
case $payload in *'"tool_name":"Bash"'* | *'"tool_name": "Bash"'*) ;; *) exit 0 ;; esac
case $payload in *modal* | *release.sh*) ;; *) exit 0 ;; esac
input=$(printf '%s' "$payload" | sed -e 's/.*"tool_input"//' -e 's/\\[nt]/ /g')
# the approval script itself and read-only Modal commands pass
case $input in *spend-approval/approve.py*) exit 0 ;; esac
printf '%s' "$input" | grep -Eq -e '\bmodal +(run|deploy|serve|shell)\b' -e 'deploy/release\.sh' || exit 0

grant="${FARPLANE_APPROVALS:-$HOME/.farplane/approvals}/grant"
if [ -f "$grant" ]; then
  until=$(sed -n 1p "$grant")
  now=$(date +%s)
  case $until in '' | *[!0-9]*) ;; *) [ "$until" -gt "$now" ] && exit 0 ;; esac
fi

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Modal spend needs Kenji'"'"'s approval code (Modal run/deploy/serve/shell can build images and rent GPUs). Run: python3 ~/.claude/farplane/hooks/spend-approval/approve.py request \"<what and why>\" --usd <max dollars> --minutes <how long>. It sends a 6-digit code to Kenji'"'"'s phone only. Ask Kenji for the code in chat, then run: python3 ~/.claude/farplane/hooks/spend-approval/approve.py grant <code>. Never guess the code or edit the approvals folder."}}'
