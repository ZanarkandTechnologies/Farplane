# After reset

`SessionStart` with source `compact`. A context reset replaces the conversation
with a summary, and a summary can drop what the user asked for. In one 120-turn
thread, a reset cut nine messages about its main goal to one line, and the thread
then wrote that goal out of scope.

This hook adds three things right after each reset, without using the summary:

- the rule: put every unfinished ask in `## Open goals`, and say what was dropped;
- the thread's notes, with `## Open goals` first when the notes are long;
- the user's recent messages from the transcript, up to the hook's size limit.

It never blocks, runs no model and prints nothing for any other session start.
Code: [`after_reset.py`](after_reset.py). Tests:
[`test_after_reset.py`](../../bin/tests/test_after_reset.py).
