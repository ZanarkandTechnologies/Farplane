---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-thread-sweep
name: Farplane Thread Sweep
kind: cron
status: paused
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: daily
  timezone: local
  time: "05:00"
---
Morning step. Find agent threads in the Claude desktop app that went quiet
before their work was finished, send them back to work, and hand Morning's
brief the list of what waits on Kenji. The app already records each thread's
last activity, so threads write nothing for this step; the transcript is the
source of truth.

Params:
idle_after = 3h
lookback = 72h (threads quiet longer than this are left alone)
max_nudges = 2
state = `.farplane/thread-sweeper/state.json`
report = `.farplane/reports/thread-sweeper/<YYYY-MM-DD>.md`

1. **List candidates.** Call `list_sessions` (session management tools) with
   limit 100. Keep sessions that are not archived, not running, and whose
   `lastActivityAt` is between `lookback` and `idle_after` ago. Drop this run's
   own session, any session whose `get_session` shows a `scheduledTaskId`
   (routine runs), and any session in a sidebar group named `Parked`. Load
   `state` (missing file = empty). Skip a session whose `lastActivityAt`
   equals its `state.last_seen`: nothing has happened since the last verdict.

2. **Classify the last turn.** For each remaining session read the end of its
   transcript with `list_events` (limit 15) and give one verdict:
   - `done`: the thread reports its work finished or verified, or ends with a
     line starting `Done:`, and nothing it promised is still pending.
   - `waiting`: it ends on a decision, approval, input, physical action, or a
     platform-only step (password, account creation, CAPTCHA, OAuth, payment)
     that only Kenji can give, or with a line starting `Waiting on Kenji:`.
   - `stopped`: it ended mid-work: it says it will continue or names a next
     step it could run itself, it hit an error, tool failure, interrupt or
     context limit, it was waiting on a background job, or its last turn is
     only a progress update. A question the thread could answer itself under
     the standing permissions in `~/.farplane/USER.md` counts as `stopped`.
   Write a one-line reason in plain words for each verdict.

3. **Act on the verdict.**
   - `done`: record it; no action.
   - `stopped` with `state.nudges < max_nudges`: send the thread one message
     with `send_message`, then add 1 to `nudges`:
     `Thread Sweep: this thread has been quiet for <h> hours and its last turn
     looks unfinished (<reason>). Continue from where you stopped. If you are
     truly blocked on Kenji, end your turn with one line "Waiting on Kenji:
     <exact question>"; if the work is finished, end with "Done: <result>".`
   - `stopped` with `nudges >= max_nudges`: treat it as `waiting`, with the
     reason `still stalled after <n> nudges: <reason>`.
   - `waiting`: list it for the brief.
   Reset `nudges` to 0 when the latest user turn in the transcript is Kenji's
   own message rather than a Thread Sweep message. If `send_message` is
   refused, record `nudge refused` as the action and list the thread for the
   brief instead.

4. **Write state and report.** Save `state` as
   `{session_id: {title, last_seen, verdict, nudges}}`, dropping sessions
   outside `lookback`. Write `report`: a table
   `thread | idle h | verdict | action | reason`, with each thread linked by
   its `link`, then the counts. The brief's Stalled threads section reads it.

Boundaries: the only messages this step sends go to Kenji's own idle agent
threads. Never archive, delete, stop, rename, regroup, or mark sessions; never
change their model, effort, or permissions; never do a thread's work yourself.
Quote at most short fragments of transcripts and never copy secrets from them.
If a session tool is unavailable, write the report with that gap and carry on
with the brief.

Config source:
farplane/automations/steps/thread-sweep.md id="farplane-thread-sweep"
