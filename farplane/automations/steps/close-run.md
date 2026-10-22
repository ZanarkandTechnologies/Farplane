---
schema: farplane_project_automation_step
owner: automation-advisor
id: close-run
name: Close Run
kind: step
---
The last step of every Claude scheduled-task run. An automation run is not a
working thread: once its result sits in its durable home, the run archives its
own thread so the sidebar does not fill with run threads. Only a run that needs
Kenji's input in this thread stays open, filed in one sidebar group.

1. **Check delivery.** The result must already be in the home the record
   names, with a receipt: the report file exists and holds this run's section,
   a Telegram send printed its message id, a Notion or GitHub write was read
   back, or `send_message` to a thread succeeded. A quiet run with nothing to
   deliver counts as delivered (`nothing to deliver`). Do not deliver anything
   here that the record did not ask for.

2. **Decide.** The run needs Kenji when either holds:
   - delivery failed and no retry succeeded, so the result would be lost; or
   - the run cannot finish without an answer only Kenji can give (spend over
     the cap, a credential, login, CAPTCHA or OAuth grant, posting under his
     name, or a choice the record says is his), and that answer belongs in
     this thread.
   A Telegram message he only reads, a report for later, or a link to another
   thread does not need him here.

3. **Needs Kenji: stay open.** End the final response with one line
   `Waiting on Kenji: <exact question>`. Call `list_groups` (sidebar tools);
   take the group named exactly `Automations: needs you`, or `create_group`
   it when missing, then `move_sessions` with `["self"]` into it. Do not
   archive and send nothing: the Thread Sweeper tells him once on Telegram
   about runs waiting in that group.

4. **Otherwise: archive.** Write the final response first (the record's
   receipt), ending with one line `Done: <result in a few words> -> <where it
   was delivered>`. Then, as the very last tool call, `archive_session` with
   `session_id: "self"` and reason `<task name> run delivered`. The
   conversation ends with that call, so nothing may follow it.

If a sidebar or archive call is refused or unavailable, do not retry or wait:
add `close: <call> refused` to the final response and stop. The Thread
Sweeper archives finished runs it finds later and never touches a run in
`Automations: needs you`.
