#!/bin/sh
# PostToolUse (Bash, Edit, Write): once every 45 minutes since Kenji's last message, tell the thread to ship and
# report the smallest finished ask instead of holding it inside a long turn. Claude only.
# capture_user_turn.py writes the start time at each user message: <turns>/<session id> = "<epoch>\n<slots told>\n".
# Plain sh with builtins: a tool call inside the first 45 minutes spawns only `date`.

[ "$FARPLANE_AGENT_RUNTIME" = claude ] || exit 0
IFS= read -r payload || [ -n "$payload" ] || exit 0
head=$(printf '%.400s' "$payload")
case $head in *'"agent_id"'*) exit 0 ;; esac            # a subagent's tools: its parent owns the turn
sid=${head#*\"session_id\"}
[ "$sid" != "$head" ] || exit 0
sid=${sid#*\"}
sid=${sid%%\"*}
case $sid in '' | *[!A-Za-z0-9_-]*) exit 0 ;; esac
file="${FARPLANE_TURNS:-$HOME/.farplane/turns}/$sid"
[ -f "$file" ] || exit 0
{ IFS= read -r start; IFS= read -r told; } < "$file"
case $start in '' | *[!0-9]*) exit 0 ;; esac
case $told in '' | *[!0-9]*) told=0 ;; esac
now=$(date +%s)
slot=$(( (now - start) / ${FARPLANE_TURN_CLOCK_SECONDS:-2700} ))
[ "$slot" -gt "$told" ] || exit 0
printf '%s\n%s\n' "$start" "$slot" > "$file"
minutes=$(( (now - start) / 60 ))
printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"Turn clock: %s minutes since the last user message and no reply yet. If that message held more than one ask, or a small ask sits inside bigger work, finish the smallest one now, commit it on its own and say so in one line, then carry on. A step that only waits on a job belongs in the background. Do not end the turn because of this note."}}\n' "$minutes"
