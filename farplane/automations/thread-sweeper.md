---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-thread-sweeper
name: Farplane Thread Sweeper
kind: cron
status: active
runtime: claude
runtime_task: farplane-thread-sweeper
target:
  workspace: /Users/kenjipcx/Zanarkand Technologies/projects/Farplane
schedule:
  type: active_hours_interval
  timezone: local
  active_hours: "08:00-22:00"
  interval_minutes: 120
---
Find agent threads in the Claude desktop app that went quiet before their work
was finished, get them moving again, and tell Kenji only what actually needs
him. The app already records each thread's last activity, so threads write
nothing for this job; the transcript is the source of truth.

Work in `/Users/kenjipcx/Zanarkand Technologies/projects/Farplane`.

Params:
idle_after = 3h
lookback = 72h (threads quiet longer than this are left alone)
waiting_hold = 7d (a thread waiting on Kenji stays tracked this long)
max_nudges = 2
state = `.farplane/thread-sweeper/state.json`
report = `.farplane/reports/thread-sweeper/<YYYY-MM-DD>.md` (one section per run)

0. **Clear finished automation runs.** Each run should archive itself
   (`farplane/automations/steps/close-run.md`); this pass catches the ones
   that failed or could not. For each task from `list_scheduled_tasks`, call
   `list_task_runs` (limit 20) and take runs that are not archived and not
   this run. Older runs fall outside that limit, so also take every
   unarchived session from `list_sessions` (limit 100) whose `get_session`
   shows a `scheduledTaskId`; it is `running` when `isRunning`, otherwise
   finished. Skip any session whose `get_session` group is `Automations: needs
   you`.
   - `succeeded` or `failed`, last activity over 15 minutes ago, and its last
     turn (`list_events`, limit 3) has no line starting `Waiting on Kenji:`:
     `archive_session` with reason `finished <task> run`. When the task's two
     newest runs both `failed`, archive the older one and instead
     `move_sessions` the newest into `Automations: needs you` (create the
     group if missing) with the reason `<task> failed twice: <error>`, and add
     it to this run's Kenji list.
   - a last turn with `Waiting on Kenji:` outside that group: `move_sessions`
     it into `Automations: needs you`; it is the run's own question.
   - every run in `Automations: needs you`: add it to the Kenji list with its
     `Waiting on Kenji:` question, unless `state` shows that question was
     already told; track it in `state` like a `waiting` thread. Kenji archives
     these himself once answered.
   - `running` with no activity for 60 minutes: leave it, and add it to the
     Kenji list as `<task> run stuck since <time>; it blocks the schedule:
     open it and answer or stop it`, once per session.
   If an archive or move is refused, record `refused` and go on.

1. **List candidates.** Call `list_sessions` (session management tools) with
   limit 100. Keep sessions that are not archived, not running, and whose
   `lastActivityAt` is between `lookback` and `idle_after` ago. Drop this run's
   own session, any session whose `get_session` shows a `scheduledTaskId`
   (routine runs, including earlier sweeper runs), and any session in a sidebar
   group named `Parked`. Load `state` (missing file = empty). Also keep any
   thread whose `state.verdict` is `waiting`, up to `waiting_hold` idle, even
   past `lookback`. Skip a session whose `lastActivityAt` equals its
   `state.last_seen`: nothing has happened since the last verdict. The app
   also bumps `lastActivityAt` without a new turn (artifact or notification
   writes); when `list_events` shows no turn after the one last judged, keep
   the earlier verdict and set `last_seen` to the new time.

2. **Classify the last turn.** For each remaining session read the end of its
   transcript with `list_events` (limit 15) and give one verdict:
   - `done`: the thread reports its work finished or verified, or ends with a
     line starting `Done:`, and nothing it promised is still pending.
   - `waiting`: it needs something only Kenji can give: spend over the weekly
     cap, a password, login, account, CAPTCHA, OAuth grant or payment detail,
     a physical action, posting or messaging under his name, or a taste or
     product choice he has to make; or it ends with a line starting
     `Waiting on Kenji:`.
   - `stopped`: it ended mid-work: it says it will continue or names a next
     step it could run itself, it hit an error, tool failure, interrupt or
     context limit, it was waiting on a background job, or its last turn is
     only a progress update. A request for a go-ahead ("say go", "want me
     to build it?") on reversible work within the cap is `stopped`: the
     standing permissions in `~/.farplane/USER.md` already grant it, and the
     nudge should say so.
   Write a one-line reason in plain words for each verdict.

3. **Act on the verdict.**
   - `done`: record it; no action.
   - `stopped` with `state.nudges < max_nudges`: send the thread one message
     with `send_message`, then add 1 to `nudges`:
     `Thread Sweeper: this thread has been quiet for <h> hours and its last
     turn looks unfinished (<reason>). Continue from where you stopped; a
     go-ahead for reversible work within the spend cap is already granted
     by the standing permissions in ~/.farplane/USER.md. If you
     are truly blocked on Kenji, end your turn with one line "Waiting on Kenji:
     <exact question>"; if the work is finished, end with "Done: <result>".`
   - `stopped` with `nudges >= max_nudges`: treat it as `waiting`, with the
     reason `still stalled after <n> nudges: <reason>`.
   - `waiting`: add it to this run's Kenji list unless its question is the
     one in `state.notified_question` (he has already been told).
   Reset `nudges` to 0 when the latest user turn in the transcript is Kenji's
   own message rather than a Thread Sweeper message. If `send_message` is
   refused, record `nudge refused` as the action and add the thread to the
   Kenji list with the reason `stalled; tap to restart: <reason>`.

4. **Tell Kenji once.** If the Kenji list is not empty, send one Telegram
   message with `$notify` (intent `blocker`, title `Thread Sweeper`, no thread
   route). For each thread: its title, hours idle, the exact question or
   blocker in at most 25 words, and its `link`. End with: `Reply in the
   thread itself (tap its link).` Then set `notified_at` and
   `notified_question` for those threads. Send nothing when the list is empty.
   Record the message id the script prints as the delivery receipt.

   **Daily reminder.** On the first run of each local day, if any tracked
   thread is still `waiting` and was told on an earlier day, add one
   `Still waiting on you` section to that run's message (or send it alone),
   oldest first: title, days waiting, the question in at most 15 words, its
   `link`. A thread reaching `waiting_hold` gets a last line `dropping after
   today` and then leaves `state`.

5. **Write state and report.** Save `state` as
   `{session_id: {title, last_seen, verdict, nudges, notified_at,
   notified_question}}`, dropping sessions outside `lookback`, except
   `waiting` threads inside `waiting_hold`. Append a run section to `report`: the run time,
   then a table `thread | idle h | verdict | action | reason`, with each thread
   linked by its `link`, then the counts.

Boundaries: archive or regroup only scheduled-task runs, as in step 0; never
archive, delete, stop, rename, regroup, or mark any other session; never
change their model, effort, or permissions; never do a thread's work
yourself; nudge only threads inside `lookback` and message only Kenji on
Telegram.
Quote at most short fragments of transcripts and never copy secrets from them.
If `list_sessions` or `list_events` is unavailable, write the report with
that gap and stop.

Final response:
- Counts: candidates, skipped unchanged, done, waiting, stopped, nudged,
  escalated, Telegram sent or not (with the delivery receipt).
- The report path.
- Automation runs: archived, filed in `Automations: needs you`, stuck,
  refused.
- Receipt: no working thread archived, stopped, or changed; no work done on
  a thread's behalf.

Close: run `farplane/automations/steps/close-run.md`.

Config source:
farplane/automations/thread-sweeper.md id="farplane-thread-sweeper"
