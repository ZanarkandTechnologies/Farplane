"""The merged Stop gate sends at most one nudge: length, continuation, then format."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "hooks/shared", ROOT / "hooks/continuation", ROOT / "bin/core"):
    sys.path.insert(0, str(directory))
import continuation  # noqa: E402
import response_format
import final_response_gate  # noqa: E402

spec = importlib.util.spec_from_file_location("stop_gate", ROOT / "hooks/stop-gate/stop_gate.py")
stop_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stop_gate)

ALL = frozenset({"continuation", "format"})


class Client:
    def __init__(self, nudge=0.1, shape="completed_change", gaps=None, feature=0.1, proposal=0.1):
        self.answers = {"nudge": {"noul": nudge}, "proposal": {"noul": proposal}, "user_deciding": {"noul": 0.1},
                        "shape": {"choice": shape},
                        "visible_feature": {"noul": feature}}
        for name in response_format.GAPS:
            self.answers[f"gap::{name}"] = {"noul": (gaps or {}).get(name, 0.1)}
        self.calls = []

    def system_one(self, **kwargs):
        self.calls.append(kwargs)
        return {"answers": {key: self.answers[key] for key in kwargs["questions"]}}


def human(text):
    return {"type": "user", "origin": {"kind": "human"}, "message": {"role": "user", "content": text}}


def assistant(text):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}


def edit_call(name="Edit"):
    return {"type": "assistant", "message": {"role": "assistant", "content": [
        {"type": "tool_use", "name": name, "input": {"file_path": "/tmp/x.py"}}]}}


def hook(text):
    return {"type": "user", "isMeta": True,
            "message": {"role": "user", "content": "Stop hook feedback:\n" + text}}


def facts(answers=True, status_first=True, narration=False, names=False, blocker=False):
    return lambda request, final: {"answers_latest": answers, "status_first": status_first,
                                   "process_narration": narration, "unexplained_names": names,
                                   "fixable_blocker": blocker}


class StopGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "transcript.jsonl"
        self.env = {"FARPLANE_CONFIG_DISABLE": "1"}
        self.logged = []
        mode = patch.object(response_format, "evidence_mode", lambda: "asleep")  # the strict side, whatever the Mac says
        mode.start()
        self.addCleanup(mode.stop)
        log = patch.object(continuation, "append_decision", self.logged.append)
        log.start()
        self.addCleanup(log.stop)

    def tearDown(self):
        self.temp.cleanup()

    def evaluate(self, rows, final, client, *, active=False, checks=ALL, reader=None):
        self.path.write_text("\n".join(json.dumps(row) for row in rows))
        return continuation.evaluate_stop(
            {"hook_event_name": "Stop", "transcript_path": str(self.path),
             "last_assistant_message": final, "stop_hook_active": active},
            environ=self.env, client=client, checks=checks, reader=reader)

    def test_uncited_completed_change_with_edits_gets_one_proof_nudge(self):
        client = Client()
        result = self.evaluate([human("Add the toggle."), edit_call()], "Done, toggle added.", client)
        self.assertIn(response_format.TAG, result["reason"])
        self.assertIn("Cite the proof", result["reason"])
        self.assertEqual(len(client.calls), 1)
        self.assertIn("nudge", client.calls[0]["questions"])
        self.assertTrue(client.calls[0]["state"]["files_changed"])

    def test_any_citation_means_proof_was_not_forgotten(self):
        for final in ("Done. Verified: 6 tests pass.", "Done: [diff](https://x.test/pr/1)",
                      "Done.\n```text\n6 passed\n```", "Done.\n![after](/tmp/after.png)"):
            with self.subTest(final=final):
                self.assertIsNone(self.evaluate([human("Fix it."), edit_call()], final, Client()))

    def test_new_visible_feature_needs_a_video_not_any_link(self):
        rows = [human("Add the chore map."), edit_call()]
        final = "Done.\n![map](/tmp/map.png) [ticket](/tmp/progress.md)"
        for shape in ("completed_change", "progress"):
            with self.subTest(shape=shape):
                result = self.evaluate(rows, final, Client(shape=shape, feature=0.9))
                self.assertIn("Record the new feature working", result["reason"])
        self.assertNotIn("Cite the proof", result["reason"])
        for proved in ("Done.\n[demo](/tmp/chores.mp4)", "Done. ![run](/tmp/run.webm)",
                       "Done.\n- **Unverified:** no display to record on this host."):
            with self.subTest(final=proved):
                self.assertIsNone(self.evaluate(rows, proved, Client(feature=0.9)))

    def test_awake_switch_drops_the_video_demand(self):
        rows = [human("Add the chore map."), edit_call()]
        with patch.object(response_format, "evidence_mode", lambda: "awake"):
            self.assertIsNone(self.evaluate(rows, "Done.\n![map](/tmp/map.png)", Client(feature=0.9)))
            result = self.evaluate(rows, "Done.", Client(feature=0.9))
            self.assertIn("Cite the proof", result["reason"])

    def test_length_nudges_stop_after_two(self):
        long = "word " * 600
        rows = [human("Explain."), assistant(long), hook(final_response_gate.gate_response(
            {"hook_event_name": "Stop", "last_assistant_message": long}, 500, 50)["reason"])]
        self.path.write_text("\n".join(json.dumps(r) for r in rows))
        self.assertEqual(continuation.length_nudges_this_turn(str(self.path)), 1)
        rows += [assistant(long), rows[-1]]
        self.path.write_text("\n".join(json.dumps(r) for r in rows))
        self.assertEqual(continuation.length_nudges_this_turn(str(self.path)), 2)
        capped = {"hook_event_name": "Stop", "last_assistant_message": long,
                  final_response_gate.LENGTH_CAPPED_KEY: True}
        self.assertIsNone(final_response_gate.gate_response(capped, 500, 50))

    def test_fixable_blocker_gets_a_fix_it_nudge(self):
        result = self.evaluate([human("Run the eval.")], "Blocked: the dev server is not running.",
                               Client(shape="blocked"), reader=facts(blocker=True))
        self.assertEqual(result["reason"], continuation.BLOCKER_NUDGE)
        self.assertEqual(self.logged[-1]["status"], "blocker_nudge")
        self.assertNotEqual(self.evaluate([human("Plan it.")], "Plan: retry by hash.",
                                          Client(shape="proposed_change"), reader=facts(blocker=True)),
                            {"decision": "block", "reason": continuation.BLOCKER_NUDGE})
        rows = [human("Run the eval."), assistant("Blocked."), hook(continuation.BLOCKER_NUDGE)]
        state = continuation.read_dialogue(str(self.path), "x") if self.path.write_text(
            "\n".join(json.dumps(r) for r in rows)) else None
        self.assertEqual(state["own_nudges_this_user_turn"], 1)

    def test_no_repeat_continuation_nudge_after_an_idle_reply(self):
        bash = {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "name": "Bash", "input": {"command": "make test"}}]}}
        nudged = [human("Finish the importer."), assistant("Next I'll fix the parser."),
                  hook(continuation.NUDGE)]
        checks = frozenset({"continuation"})
        # Restating the status after a nudge earns no second nudge.
        self.assertIsNone(self.evaluate(nudged, "The parser fix is next.", Client(nudge=0.9), checks=checks))
        self.assertTrue(self.logged[-1]["idle_after_nudge"])
        result = self.evaluate([*nudged, bash, bash], "Parser fixed; the writer is next.",
                               Client(nudge=0.9), checks=checks)
        self.assertEqual(result["reason"], continuation.NUDGE)

    def test_no_continuation_push_when_the_answer_waits_on_the_user(self):
        checks = frozenset({"continuation"})
        rows = [human("Finish the importer.")]
        self.assertIsNone(self.evaluate(rows, "The parser fix is ready.\n\nWaiting on you: approve the merge.",
                                        Client(nudge=0.9), checks=checks))
        self.assertTrue(self.logged[-1]["waits_on_user"])
        self.assertEqual(self.evaluate(rows, "Next I'll fix the parser.", Client(nudge=0.9),
                                       checks=checks)["reason"], continuation.NUDGE)

    def test_every_nudge_carries_its_shape_template(self):
        for shape in response_format.SHAPES:
            with self.subTest(shape=shape):
                text = response_format.feedback(["before_after_example"], shape)
                self.assertIn(str(response_format.SHAPES[shape]["skeleton"]), text)
                self.assertNotIn("**Context:**", text)
                # An in-place fix keeps the answer's own form: no template.
                self.assertNotIn("````markdown", response_format.feedback(["unanswered"], shape))
                self.assertIn("tables, diagrams", response_format.feedback(["unanswered"], shape))
        text = response_format.feedback(["before_after_example"], "completed_change", long_turn=True)
        self.assertTrue(response_format.has_context_line(text.split("````markdown\n")[1]))
        self.assertIn("**Before:**", text)

    def test_name_nudge_lists_the_names(self):
        import reader_check
        facts_ = {"answers_latest": True, "status_first": False, "process_narration": False,
                  "unexplained_names": True, "names": ["dev", "Blacksmith"]}
        self.assertEqual(reader_check.gaps(facts_), ["plain_names"])
        self.assertEqual(reader_check.gaps({**facts_, "process_narration": True}),
                         ["cold_read", "plain_names"])
        text = response_format.feedback(["plain_names"], "simple_answer", names=["dev", "Blacksmith"])
        self.assertIn("“dev”, “Blacksmith”", text)

    def test_reader_claims_are_checked(self):
        import reader_check
        final = ("**Merged.** [acme/shop#654](https://x.test/654) is in. P0 (cloud depth) "
                 "wins. tmux, a background terminal, keeps it alive. The carve step runs.")
        for name in ("shop#654", "38", "--fp-scale", "P0", "tmux", "Widgetry", "`tokens.css`"):
            with self.subTest(name=name):
                self.assertTrue(reader_check.known_name(name, final, "coding widgetry issues"))
        self.assertFalse(reader_check.known_name("carve", final, ""))
        self.assertTrue(reader_check.opens_with_status("### Fix\n**Context:** You asked x.\n\n**Partial: y.**"))
        self.assertFalse(reader_check.opens_with_status("I reran the scorer, then the parser."))
        self.assertTrue(reader_check.clip_request("a" * 4000 + "ASK").endswith("ASK"))

    def test_long_turn_opens_with_context(self):
        from datetime import datetime, timezone
        now = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)
        self.assertFalse(continuation.long_turn("", now=now))
        self.assertTrue(continuation.long_turn("2026-10-20T11:30:00Z", now=now))
        # A 20-minute live exchange gets no Context line, however many tools ran.
        self.assertFalse(continuation.long_turn("2026-10-20T11:40:00Z", now=now))
        answer = {"shape": {"choice": "simple_answer"}}
        _, gaps = response_format.select_gaps(answer, files_changed=False, final="All six found.", long_turn=True)
        self.assertEqual(gaps, ["context_line"])
        recalled = "### Openings\n**Context:** You asked me to rescore the openings; I reran the scorer.\nAll six found."
        _, gaps = response_format.select_gaps(answer, files_changed=False, final=recalled, long_turn=True)
        self.assertEqual(gaps, [])
        _, gaps = response_format.select_gaps(answer, files_changed=False, final="All six found.")
        self.assertEqual(gaps, [])

    def test_change_always_shows_before_after(self):
        long = "Done. " + "The importer now skips blank rows and keeps the valid ones in order. " * 4 + "Verified: tests pass."
        _, gaps = response_format.select_gaps({"shape": {"choice": "completed_change"}}, files_changed=True, final=long)
        self.assertEqual(gaps[0], "before_after_example")
        # A status relay or an answer in a turn that also edited files is not a change report.
        for shape in ("progress", "simple_answer", "blocked"):
            with self.subTest(shape=shape):
                _, gaps = response_format.select_gaps({"shape": {"choice": shape}}, files_changed=True, final=long)
                self.assertNotIn("before_after_example", gaps)
        shown = long + "\n> **Before:** blank rows stopped it.\n> **After:** they are skipped."
        _, gaps = response_format.select_gaps({"shape": {"choice": "completed_change"}}, files_changed=True, final=shown)
        self.assertNotIn("before_after_example", gaps)
        _, gaps = response_format.select_gaps({"shape": {"choice": "simple_answer"}}, files_changed=False, final=long)
        self.assertNotIn("before_after_example", gaps)

    def test_nonvisual_change_keeps_any_citation_as_proof(self):
        rows = [human("Bump the timeout."), edit_call()]
        self.assertIsNone(self.evaluate(rows, "Done. Verified: config test passes.", Client(feature=0.2)))

    def test_reader_gaps_apply_to_every_shape(self):
        for shape in response_format.SHAPES:
            with self.subTest(shape=shape):
                result = self.evaluate([human("Can graph syntax render?")], "Waiting on the fixers.",
                                       Client(shape=shape, gaps={"unanswered": 0.8}), reader=facts(answers=False))
                self.assertIn("Answer what the user's latest message asked", result["reason"])
                result = self.evaluate([human("Status?")], "Reach strip fixed; 6/7 agree.",
                                       Client(shape=shape), reader=facts(status_first=False, narration=True))
                self.assertIn("overall state in plain words", result["reason"])

    def test_session_started_threads_are_checked(self):
        started = {"type": "user", "turnOrigin": "sdk", "promptSource": "sdk",
                   "message": {"role": "user", "content": "Build piece 8."}}
        scheduled = {**started, "turnOrigin": "scheduled", "promptSource": "system",
                     "origin": {"kind": "task-notification"}}
        result = self.evaluate([started], "Waiting on the fixers.", Client(shape="simple_answer", gaps={"unanswered": 0.8}),
                               reader=facts(answers=False))
        self.assertIn("Answer what the user's latest message asked", result["reason"])
        result = self.evaluate([scheduled], "Waiting.", Client(shape="simple_answer", gaps={"unanswered": 0.8}),
                               reader=facts(answers=False))
        self.assertIn("Answer what the user's latest message asked", result["reason"])

    def test_wrap_up_stop_reads_the_turn_answer(self):
        wrap = {"type": "assistant", "message": {"role": "assistant", "content": [
            {"type": "tool_use", "name": "mcp__ccd_turn__wrap_up", "input": {}}]}}
        self.path.write_text("\n".join(json.dumps(row) for row in [
            human("Status?"), assistant("Old turn."), human("Now?"), assistant("Rooms load."), wrap]))
        self.assertEqual(continuation.last_turn_answer(str(self.path)), "Rooms load.")
        self.path.write_text("\n".join(json.dumps(row) for row in [human("Now?"), wrap]))
        self.assertEqual(continuation.last_turn_answer(str(self.path)), "")

    def test_unexplained_names_need_plain_words(self):
        result = self.evaluate([human("Status?")], "Rescored with T2's scorer at ab006f9; 6/6 found.",
                               Client(shape="simple_answer"), reader=facts(status_first=False, names=True))
        # Jargon alone asks for the names, not a vague "lead with the state".
        self.assertIn("what each name the user did not use is", result["reason"])
        self.assertNotIn("overall state in plain words", result["reason"])
        result = self.evaluate([human("Status?")], "All six found. Rescored with T2's scorer at ab006f9.",
                               Client(shape="simple_answer"), reader=facts(names=True))
        self.assertIn("what each name the user did not use is", result["reason"])

    def test_process_with_status_first_passes_the_reader(self):
        self.assertIsNone(self.evaluate([human("Status?")], "Works. I then tuned X.", Client(shape="simple_answer"),
                                        reader=facts(narration=True)))

    def test_reader_sees_the_whole_answer_and_failure_allows(self):
        seen = []
        final = "Start. " + "middlemiddlemiddlemiddlemiddlemiddlemiddlemiddle " * 120 + "End."  # 5,000+ chars, under 180 words
        self.evaluate([human("Explain.")], final, Client(shape="simple_answer"),
                      reader=lambda request, answer: seen.append(answer))
        self.assertEqual(seen, [final])
        self.assertEqual(self.logged[-1]["reader"], "unavailable")
        self.assertEqual(self.logged[-1]["status"], "allow")

    def test_relative_file_paths_get_an_absolute_path_nudge(self):
        for final in ("See [plan](docs/plan.md).", "Edited `hooks/stop-gate/README.md:12`.",
                      "![shot](/Users/me/My%20Docs/a.png)", "See [a](</Users/me/My Docs/a.md>)."):
            with self.subTest(final=final):
                result = self.evaluate([human("Where?")], final, Client(shape="simple_answer"))
                self.assertIn("absolute path", result["reason"])
        for final in ("See [plan](/Users/me/docs/plan.md).", "See [PR](https://x.test/1).",
                      "Use `a/b` or `README.md`.", "Open `~/notes/a.md`.", "Run `./bin/start.sh`.",
                      "![shot](/Users/me/My Docs/a.png)", "See [plan](/Users/me/My Docs/plan.md).",
                      "Broken: `![shot](/Users/me/My%20Docs/a.png)`."):
            with self.subTest(final=final):
                self.assertIsNone(self.evaluate([human("Where?")], final, Client(shape="simple_answer")))

    def test_one_format_rewrite_per_user_turn_even_after_more_work(self):
        rows = [human("Fix it."), edit_call(), assistant("Done."),
                hook(response_format.feedback(["conclusion_first"]))]
        client = Client(shape="simple_answer", gaps={"conclusion_first": 0.9})
        self.assertIsNone(self.evaluate(rows, "Rewritten.", client, active=True))
        rows += [edit_call("Bash"), assistant("More work.")]
        self.assertIsNone(self.evaluate(rows, "Done after more work.", client, active=True))

    def test_reader_knows_only_the_users_own_earlier_words(self):
        noisy = "<system-reminder>\nLinked sessions now: fast-walk.\n</system-reminder>\nshould i use the shadow lite?"
        self.assertEqual(continuation.own_words(noisy), "should i use the shadow lite?")

    def test_relaying_another_sessions_news_is_not_unanswered(self):
        news = human("<cross-session-message from=\"local_x\">FYI: the canvas has a new layout.</cross-session-message>")
        final = "The v2 page has a new layout, version 31. Waiting on you: your review."
        self.assertIsNone(self.evaluate([news], final, Client(shape="simple_answer", gaps={"unanswered": 0.8}),
                                        reader=facts(answers=False)))
        result = self.evaluate([human("Is the canvas updated?")], final,
                               Client(shape="simple_answer", gaps={"unanswered": 0.8}), reader=facts(answers=False))
        self.assertIn("latest message asked", result["reason"])
        # Haiku alone over-reports; Jev must agree the message went unanswered.
        self.assertIsNone(self.evaluate([human("Is the canvas updated?")], final,
                                        Client(shape="simple_answer"), reader=facts(answers=False)))

    def test_long_plain_answer_gets_cut_to_a_short_one(self):
        answer = {"shape": {"choice": "simple_answer"}}
        long = "The matcher misses because the crop is cut. " * 32  # 256 words
        _, gaps = response_format.select_gaps(answer, files_changed=False, final=long)
        self.assertEqual(gaps, ["short_answer"])
        self.assertIn("ASD-STE100", response_format.feedback(gaps, "simple_answer"))
        table = long[:200] + "\n\n| a | b |\n| --- | --- |\n" + "| x y z w | v u t s |\n" * 60
        _, gaps = response_format.select_gaps(answer, files_changed=False, final=table)
        self.assertEqual(gaps, [])
        report = {"shape": {"choice": "completed_change"}}
        _, gaps = response_format.select_gaps(report, files_changed=False, final=long)
        self.assertNotIn("short_answer", gaps)

    def test_format_nudges_stop_at_the_turn_ceiling(self):
        rows = [human("Fix it.")]
        for _ in range(continuation.MAX_FORMAT_NUDGES):
            rows += [edit_call("Bash"), assistant("Done."), hook(response_format.feedback(["proof"]))]
        rows += [edit_call("Bash")]
        client = Client(shape="simple_answer", gaps={"conclusion_first": 0.9})
        self.assertIsNone(self.evaluate(rows, "Done.", client, active=True))

    def test_no_edits_means_no_proof_nudge(self):
        self.assertIsNone(self.evaluate([human("Fix it."), edit_call("Read")], "Done.", Client()))

    def test_continuation_wins_over_format(self):
        result = self.evaluate([human("Fix it."), edit_call()], "I'll test next.", Client(nudge=0.9))
        self.assertEqual(result["reason"], continuation.NUDGE)

    def test_valuable_proposal_gets_a_do_it_nudge(self):
        final = "Done. Next I could cache the scan crops to halve rebuild time. Want me to?"
        result = self.evaluate([human("Speed up rebuilds.")], final, Client(proposal=0.8))
        self.assertEqual(result["reason"], continuation.PROPOSAL_NUDGE)
        self.assertEqual(self.logged[-1]["status"], "proposal_nudge")
        self.assertIsNone(self.evaluate([human("Speed up rebuilds.")], "Done. Verified: 2x.",
                                        Client(proposal=0.2)))
        rows = [human("Speed up rebuilds."), assistant(final), hook(continuation.PROPOSAL_NUDGE)]
        self.path.write_text("\n".join(json.dumps(r) for r in rows))
        self.assertEqual(continuation.read_dialogue(str(self.path), "x")["own_nudges_this_user_turn"], 1)

    def test_proposals_titled_by_work_get_a_gain_line_in_any_shape(self):
        for shape in ("simple_answer", "proposed_change"):
            with self.subTest(shape=shape):
                result = self.evaluate([human("Why is it slow?")], "Next: add a cache layer.",
                                       Client(shape=shape, gaps={"proposal_gain": 0.9}))
                self.assertIn("Title each proposed next step by its gain", result["reason"])

    def test_only_gaps_of_the_chosen_shape_count(self):
        client = Client(shape="simple_answer", gaps={"decision_choice": 0.95, "conclusion_first": 0.65})
        result = self.evaluate([human("Why?")], "Because the loop exits early.", client)
        self.assertIn("Lead with the conclusion", result["reason"])
        self.assertNotIn("recommendation", result["reason"])

    def test_format_nudges_once_per_user_turn(self):
        rows = [human("Fix it."), edit_call(), assistant("Done."),
                hook(response_format.feedback(["proof"]))]
        client = Client()
        self.assertIsNone(self.evaluate(rows, "Done again.", client, active=True))
        self.assertNotIn("shape", client.calls[0]["questions"])

    def test_spent_format_nudge_still_leaves_one_proof_nudge(self):
        rows = [human("Give desks a role."), edit_call(), assistant("Done."),
                hook(response_format.feedback(["progress_ledger"]))]
        client = Client(feature=0.9)
        result = self.evaluate(rows, "Done. Verified: tests pass.", client, active=True,
                               reader=facts(answers=False))
        self.assertIn("Record the new feature working", result["reason"])
        self.assertNotIn("latest message asked", result["reason"])
        rows += [assistant("Done. Verified: tests pass."), hook(result["reason"])]
        self.assertIsNone(self.evaluate(rows, "Done again.", Client(feature=0.9), active=True))

    def test_new_user_turn_resets_edits_and_format_count(self):
        rows = [human("Fix it."), edit_call(), hook(response_format.feedback(["proof"])),
                human("Now explain it.")]
        self.assertIsNone(self.evaluate(rows, "It skips blanks.", Client()))

    def test_codex_rollout_tracks_apply_patch_and_wrapped_format_feedback(self):
        def codex(role, text, kinds):
            item = {"type": "message", "role": role,
                    "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}],
                    "internal_chat_message_metadata_passthrough": {"turn_id": "t1", "content_item_kinds": kinds}}
            return {"type": "response_item", "payload": item}
        patch_call = {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "apply_patch"}}
        rows = [codex("user", "Fix it.", ["user.text"]), patch_call]
        self.assertIn("Cite the proof", self.evaluate(rows, "Done.", Client())["reason"])
        wrapped = f'<hook_prompt hook_run_id="stop:1">{response_format.feedback(["proof"])}</hook_prompt>'
        rows += [codex("assistant", "Done.", []), codex("user", wrapped, ["unknown"])]
        self.assertIsNone(self.evaluate(rows, "Done again.", Client(), active=True))

    def test_continuation_only_checks_ask_only_the_nudge(self):
        client = Client()
        self.evaluate([human("Fix it."), edit_call()], "Done.", client, checks=frozenset({"continuation"}))
        self.assertEqual(list(client.calls[0]["questions"]), ["nudge", "proposal", "user_deciding"])

    def test_gaps_capped_at_two_and_feedback_never_adds_headings(self):
        client = Client(shape="proposed_change", gaps={"before_after_example": 0.9, "proof_planned": 0.8})
        result = self.evaluate([human("Plan it.")], "We should improve caching.", client)
        self.assertEqual(result["reason"].count("**Add:**"), 2)
        self.assertIn("no empty headings", result["reason"])


class EntrypointTests(unittest.TestCase):
    def test_length_blocks_first_without_a_jev_call(self):
        payload = {"hook_event_name": "Stop", "last_assistant_message": "word " * 600}
        with patch.object(stop_gate, "load_runtime_env", return_value={}), \
                patch.object(stop_gate, "jev_gate") as jev:
            result = stop_gate.run_gate(payload)
        self.assertIn("Response length", result["reason"])
        jev.assert_not_called()

    def test_checks_env_selects_checks(self):
        self.assertEqual(stop_gate.configured_checks({}), stop_gate.ALL_CHECKS)
        self.assertEqual(stop_gate.configured_checks({"FARPLANE_STOP_CHECKS": "length, bogus"}),
                         frozenset({"length"}))
        with patch.object(stop_gate, "load_runtime_env", return_value={"FARPLANE_STOP_CHECKS": "length"}), \
                patch.object(stop_gate, "jev_gate") as jev:
            self.assertIsNone(stop_gate.run_gate({"hook_event_name": "Stop", "last_assistant_message": "ok"}))
        jev.assert_not_called()

    def test_gate_names_follow_the_reason_marker(self):
        self.assertEqual(stop_gate.gate_name(response_format.feedback(["proof"])), "response-format")
        self.assertEqual(stop_gate.gate_name(continuation.NUDGE), "continuation")
        self.assertEqual(stop_gate.gate_name("#### Response length"), "response-length")

    def test_root_hooks_register_only_the_merged_blocking_gate(self):
        payload = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        commands = [hook["command"] for group in payload["hooks"]["Stop"] for hook in group["hooks"]]
        self.assertIn('python3 "$HOME/.codex/hooks/stop-gate/stop_gate.py"', commands)
        self.assertFalse(any("continuation_gate" in c or "final_response_gate" in c for c in commands))


class CatalogTests(unittest.TestCase):
    def test_every_shape_mirrors_an_agents_template_heading(self):
        headings = set(re.findall(r"^### (.+)$",
                                  (ROOT / "runtimes/AGENTS.md").read_text(), re.M))
        for name, spec in response_format.SHAPES.items():
            with self.subTest(shape=name):
                self.assertIn(spec["template"], headings)
                self.assertTrue(set(spec["gaps"]) <= set(response_format.GAPS))

    def test_eval_cases_use_known_shapes_and_gaps(self):
        cases = json.loads((ROOT / "hooks/stop-gate/eval_cases.json").read_text())
        known = set(response_format.GAPS) | {"proof", "video_proof"}
        for case in cases:
            self.assertIn(case["expected_shape"], response_format.SHAPES)
            self.assertTrue(set(case["expected_fixes"]) <= known, case["id"])


if __name__ == "__main__":
    unittest.main()
