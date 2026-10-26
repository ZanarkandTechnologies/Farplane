#!/bin/sh
# PreToolUse (Bash): deny a foreground call that sleeps 30 s or more, or polls in an
# until/while/for-sleep loop, and say how to rerun it. Claude only (Codex has no
# run_in_background). A timeout of 30000 ms or less marks a short wait and passes.
# Plain sh: a Bash call without "sleep" spawns nothing; one with it spawns sed and grep.

[ "$FARPLANE_AGENT_RUNTIME" = claude ] || exit 0
IFS= read -r payload || [ -n "$payload" ] || exit 0
case $payload in *'"tool_name":"Bash"'* | *'"tool_name": "Bash"'*) ;; *) exit 0 ;; esac
case $payload in *sleep*) ;; *) exit 0 ;; esac
case $payload in *'"run_in_background":true'* | *'"run_in_background": true'*) exit 0 ;; esac
# Only the tool input counts; escaped newlines and tabs become spaces so word boundaries hold.
input=$(printf '%s' "$payload" | sed -e 's/.*"tool_input"//' -e 's/\\[nt]/ /g')
case $input in *'"timeout"'*)
  timeout=$(printf '%s' "$input" | sed -nE 's/.*"timeout": ?([0-9]+).*/\1/p')
  [ -n "$timeout" ] && [ "$timeout" -le 30000 ] && exit 0 ;;
esac
printf '%s' "$input" | grep -Eq \
  -e '\b(until|while|for)\b.*\bdo\b.*\bsleep\b' \
  -e '\bsleep +0*([3-9][0-9]|[1-9][0-9]{2,})(\.[0-9]+)?s?\b' \
  -e '\bsleep +[0-9.]*[1-9][0-9.]*[mh]\b' || exit 0

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked foreground wait: this Bash call sleeps 30 s or more, or polls in an until/while/for sleep loop, and would hold the turn. Rerun it with run_in_background: true and keep working or end the turn; you are re-invoked when it exits. To wait on a condition (a file, a log line, a pod), put the until-loop in that background call or under Monitor. If the whole wait is under 30 s, rerun it with timeout: 30000 or less."}}'
