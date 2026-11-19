#!/bin/sh
# PreToolUse (Bash, start_session): deny a new git worktree unless the operator asked
# for one. Threads ran `git worktree add` 196 times and started 55 sessions with
# use_worktree in the week of 22-29 Oct 2026, against "only when I specify". The
# override is explicit and visible: FARPLANE_WORKTREE_OK=1 on the git command.

IFS= read -r payload || [ -n "$payload" ] || exit 0
case $payload in *worktree*) ;; *) exit 0 ;; esac
input=$(printf '%s' "$payload" | sed -e 's/.*"tool_input"//' -e 's/\\[nt]/ /g')
# A repo that works one worktree per change opts out (Oures, Kenji 19 Nov 2026: "yes worktree per change"):
#   git config farplane.worktreePerChange true
cwd=$(printf '%s' "$payload" | sed -n 's/.*"cwd": *"\([^"]*\)".*/\1/p')
[ -n "$cwd" ] && [ "$(git -C "$cwd" config --bool farplane.worktreePerChange 2>/dev/null)" = true ] && exit 0
case $payload in
  *'"tool_name":"Bash"'* | *'"tool_name": "Bash"'*)
    printf '%s' "$input" | grep -Eq '\bworktree +add\b' || exit 0
    printf '%s' "$input" | grep -q 'FARPLANE_WORKTREE_OK=1' && exit 0 ;;
  *start_session*)
    printf '%s' "$input" | grep -Eq '"use_worktree": ?true' || exit 0 ;;
  *) exit 0 ;;
esac

printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked new worktree: Kenji allows a new git worktree only when he asks for one (or the repo sets git config farplane.worktreePerChange true, as Oures does: run it from that checkout). Work in the existing shared checkout for this version instead, commit only your own files, pull --no-rebase, push; for a new session pass use_worktree: false. If Kenji asked in his own words, rerun as FARPLANE_WORKTREE_OK=1 git worktree add ... and quote his words in your reply."}}'
