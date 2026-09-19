from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "bin" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

import skill_suggestion


class FakeClient:
    def __init__(self, responses: list[object]) -> None:
        self.responses = list(responses)
        self.calls: list[dict[str, object]] = []

    def system_one(self, **kwargs: object) -> object:
        self.calls.append(dict(kwargs))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def answer(*, noul: float | None = None, choice: str = "", probabilities: dict[str, float] | None = None) -> object:
    return SimpleNamespace(noul=noul, choice=choice, probabilities=probabilities or {})


def response(answers: dict[str, object]) -> object:
    return SimpleNamespace(answers=answers)


class SkillSuggestionTests(unittest.TestCase):
    def records(self, root: Path) -> dict[str, dict[str, object]]:
        skill_path = root / "skills" / "research" / "SKILL.md"
        skill_path.parent.mkdir(parents=True)
        skill_path.write_text("# Research\nUse current external evidence.\n", encoding="utf-8")
        return {
            "research": {
                "name": "research",
                "description": "Research current external evidence.",
                "path": "skills/research/SKILL.md",
            },
            "impl-plan": {
                "name": "impl-plan",
                "description": "Create a repository-grounded implementation plan.",
                "path": "skills/impl-plan/SKILL.md",
            },
            "review": {
                "name": "review",
                "description": "Review evidence and return a verdict.",
                "path": "skills/review/SKILL.md",
            },
        }

    def test_official_two_pass_recipe_returns_choice_winner(self) -> None:
        wide = response(
            {
                "which": answer(probabilities={"impl-plan": 0.2, "research": 0.7, "review": 0.1}),
                "gate::acts_on_user_system": answer(noul=0.7),
                "gate::would_follow_documented_procedure": answer(noul=0.8),
                "gate::prose_suffices": answer(noul=0.2),
            }
        )
        detailed = response(
            {
                "which": answer(choice="research"),
                "fits::research": answer(noul=0.9),
                "fits::impl-plan": answer(noul=0.4),
                "fits::review": answer(noul=0.2),
            }
        )
        client = FakeClient([wide, detailed])
        with tempfile.TemporaryDirectory() as tmp:
            result = skill_suggestion.suggest_entry_skill(
                project_root=Path(tmp),
                request="Find current JEV hook implementations.",
                records=self.records(Path(tmp)),
                client=client,
                environ={skill_suggestion.ENABLED_ENV: "1"},
            )
        self.assertEqual(result, "research")
        self.assertEqual(len(client.calls), 2)
        self.assertEqual(list(client.calls[1]["questions"])[0], "which")
        detailed_criteria = client.calls[1]["questions"]["which"]["criteria"]
        self.assertEqual(list(detailed_criteria), ["research", "impl-plan", "review"])
        self.assertIn("# Research", detailed_criteria["research"])

    def test_gate_abstains_before_detailed_call(self) -> None:
        wide = response(
            {
                "which": answer(probabilities={"research": 1.0}),
                "gate::acts_on_user_system": answer(noul=0.0),
                "gate::would_follow_documented_procedure": answer(noul=0.0),
                "gate::prose_suffices": answer(noul=1.0),
            }
        )
        client = FakeClient([wide])
        with tempfile.TemporaryDirectory() as tmp:
            result = skill_suggestion.suggest_entry_skill(
                project_root=Path(tmp),
                request="What is a monad?",
                records=self.records(Path(tmp)),
                client=client,
                environ={skill_suggestion.ENABLED_ENV: "1"},
            )
        self.assertEqual(result, "")
        self.assertEqual(len(client.calls), 1)

    def test_low_absolute_fit_rejects_choice_winner(self) -> None:
        wide = response(
            {
                "which": answer(probabilities={"research": 1.0}),
                "gate::acts_on_user_system": answer(noul=1.0),
                "gate::would_follow_documented_procedure": answer(noul=1.0),
                "gate::prose_suffices": answer(noul=0.0),
            }
        )
        detailed = response(
            {"which": answer(choice="research"), "fits::research": answer(noul=0.2)}
        )
        client = FakeClient([wide, detailed])
        with tempfile.TemporaryDirectory() as tmp:
            result = skill_suggestion.suggest_entry_skill(
                project_root=Path(tmp),
                request="Post to an unsupported service.",
                records=self.records(Path(tmp)),
                client=client,
                environ={skill_suggestion.ENABLED_ENV: "1"},
            )
        self.assertEqual(result, "")

    def test_disabled_and_failures_are_silent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            records = self.records(Path(tmp))
            self.assertEqual(
                skill_suggestion.suggest_entry_skill(
                    project_root=Path(tmp), request="Research this", records=records, environ={}
                ),
                "",
            )
            self.assertEqual(
                skill_suggestion.suggest_entry_skill(
                    project_root=Path(tmp),
                    request="Research this",
                    records=records,
                    client=FakeClient([TimeoutError("slow")]),
                    environ={skill_suggestion.ENABLED_ENV: "1"},
                ),
                "",
            )

    def test_malformed_response_fails_open(self) -> None:
        client = FakeClient([response({"which": answer(probabilities={"research": 1.0})})])
        with tempfile.TemporaryDirectory() as tmp:
            result = skill_suggestion.suggest_entry_skill(
                project_root=Path(tmp),
                request="Research this",
                records=self.records(Path(tmp)),
                client=client,
                environ={skill_suggestion.ENABLED_ENV: "1"},
            )
        self.assertEqual(result, "")

    def test_context_is_advisory(self) -> None:
        context = skill_suggestion.suggestion_context("research")
        self.assertEqual(
            context,
            "<skill_relevance>\n"
            "Relevant to the current request: research. Ignore this if it does not fit "
            "what the user actually asked for.\n"
            "</skill_relevance>",
        )
        self.assertEqual(skill_suggestion.suggestion_context(""), "")

    def test_openrouter_client_posts_decisions_shape(self) -> None:
        class HttpResponse:
            def __enter__(self) -> "HttpResponse":
                return self

            def __exit__(self, *args: object) -> None:
                return None

            def read(self) -> bytes:
                return b'{"answers":{"fit":{"type":"noul","noul":0.9}}}'

        client = skill_suggestion.HttpDecisionClient(
            api_key="secret", endpoint="https://example.test/decisions", provider="openrouter", timeout=2.5
        )
        with patch.object(skill_suggestion, "urlopen", return_value=HttpResponse()) as send:
            result = client.system_one(
                state={"request": "research"},
                questions={"fit": {"type": "noul", "instructions": "Does it fit?"}},
                model="typesafe/jev-1.13",
            )
        request = send.call_args.args[0]
        body = __import__("json").loads(request.data)
        self.assertEqual(request.get_header("Authorization"), "Bearer secret")
        self.assertEqual(body["model"], "typesafe/jev-1.13")
        self.assertEqual(body["questions"]["fit"]["type"], "noul")
        self.assertEqual(result["answers"]["fit"]["noul"], 0.9)

    def test_featherless_provider_requires_doppler_key(self) -> None:
        self.assertIsNone(skill_suggestion._build_client(
            {
                skill_suggestion.PROVIDER_ENV: "featherless",
                skill_suggestion.ENABLED_ENV: "1",
            }
        ))

    def test_featherless_doppler_key_selects_production(self) -> None:
        client = skill_suggestion._build_client(
            {
                skill_suggestion.PROVIDER_ENV: "featherless",
                skill_suggestion.FEATHERLESS_API_KEY_ENV: "secret",
            }
        )
        self.assertEqual(client.api_key, "secret")
        self.assertEqual(client.provider, "featherless")
        self.assertEqual(client.endpoint, "https://api.featherless.ai/v1/classifier")

    def test_openrouter_remains_default_and_requires_doppler_key(self) -> None:
        self.assertIsNone(skill_suggestion._build_client({}))
        client = skill_suggestion._build_client(
            {skill_suggestion.OPENROUTER_API_KEY_ENV: "secret"}
        )
        self.assertEqual(client.provider, "openrouter")


if __name__ == "__main__":
    unittest.main()
