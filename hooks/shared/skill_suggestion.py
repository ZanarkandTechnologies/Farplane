"""Suggests one entry skill with TypeSafe's official two-pass JEV recipe.

The generated registry owns the broad roster. Detailed reranking reads bounded
excerpts from the registry-recorded `SKILL.md` paths. OpenRouter or Featherless
provides the decision endpoint; every provider or response failure is fail-open.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Mapping
from urllib.request import Request, urlopen


MODEL_ENV = "FARPLANE_JEV_MODEL"
ENABLED_ENV = "FARPLANE_JEV_SKILL_SUGGESTION"
PROVIDER_ENV = "FARPLANE_JEV_PROVIDER"
ENDPOINT_ENV = "FARPLANE_JEV_ENDPOINT"
OPENROUTER_API_KEY_ENV = "OPENROUTER_API_KEY"
FEATHERLESS_API_KEY_ENV = "FEATHERLESS_API_KEY"
PROVIDERS = {
    "openrouter": {
        "endpoint": "https://openrouter.ai/api/alpha/decisions",
        "model": "typesafe/jev-1.13",
        "api_key_env": OPENROUTER_API_KEY_ENV,
    },
    "featherless": {
        "endpoint": "https://api.featherless.ai/v1/classifier",
        "model": "featherless-ai/gemma-4-26B-A4B-classifier",
        "api_key_env": FEATHERLESS_API_KEY_ENV,
    },
}
SHORTLIST = 3
EXCERPT_CHARS = 700
GATE_THRESHOLD = 0.30
FITS_THRESHOLD = 0.30

CHOICE_INSTRUCTIONS = (
    "Which of these skills, if any, is the right one to load to help with the "
    "user's latest request?"
)
GATE_QUESTIONS = {
    "acts_on_user_system": (
        "Is the assistant being asked to act on the user's files, accounts, devices, "
        "or online services, rather than only to explain or advise?"
    ),
    "would_follow_documented_procedure": (
        "Would a careful expert answering this consult a specific documented procedure "
        "or set of commands, rather than answering from general understanding?"
    ),
    "prose_suffices": (
        "Could a knowledgeable generalist fully satisfy this request in prose, with "
        "no tools, no documentation, and no access to the user's files or accounts?"
    ),
}
INVERTED_GATES = {"prose_suffices"}
RERANK_INSTRUCTIONS = (
    "Exactly one of these skills is the right entry skill to load for the user's "
    "latest request. Which one? Read what each actually does, not just its name."
)


def enabled(environ: Mapping[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return str(env.get(ENABLED_ENV, "")).strip().lower() in {"1", "true", "yes", "on"}


def _skill_excerpt(project_root: Path, record: Mapping[str, object]) -> str:
    raw_path = record.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        return ""
    path = project_root / raw_path
    try:
        return path.read_text(encoding="utf-8")[:EXCERPT_CHARS]
    except OSError:
        return ""


def _provider_config(environ: Mapping[str, str]) -> Mapping[str, str] | None:
    provider = str(environ.get(PROVIDER_ENV, "openrouter")).strip().lower()
    config = PROVIDERS.get(provider)
    if config is None:
        return None
    return {"provider": provider, **config}


def _build_client(environ: Mapping[str, str]) -> object | None:
    config = _provider_config(environ)
    if config is None:
        return None
    api_key = str(environ.get(config["api_key_env"], "")).strip()
    if not api_key:
        return None
    return HttpDecisionClient(
        api_key=api_key,
        endpoint=str(environ.get(ENDPOINT_ENV) or config["endpoint"]),
        provider=config["provider"],
        timeout=2.5,
    )


class HttpDecisionClient:
    """Minimal adapter for compatible OpenRouter and Featherless endpoints."""

    def __init__(self, *, api_key: str, endpoint: str, provider: str, timeout: float) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.provider = provider
        self.timeout = timeout

    def system_one(
        self,
        *,
        state: Mapping[str, object],
        questions: Mapping[str, object],
        model: str,
    ) -> Mapping[str, object]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if self.provider == "openrouter":
            headers["X-OpenRouter-Title"] = "Farplane JEV Skill Suggestion"
        request = Request(
            self.endpoint,
            data=json.dumps(
                {"model": model, "state": state, "questions": questions}
            ).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urlopen(request, timeout=self.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, dict) or not isinstance(payload.get("answers"), dict):
            raise ValueError(f"{self.provider} decision response has no answers object")
        return payload


def _answers(response: object) -> Mapping[str, object]:
    if isinstance(response, Mapping):
        answers = response.get("answers")
    else:
        answers = getattr(response, "answers", None)
    if not isinstance(answers, Mapping):
        raise ValueError("decision response has no answers mapping")
    return answers


def _field(answer: object, name: str) -> object:
    if isinstance(answer, Mapping):
        return answer.get(name)
    return getattr(answer, name)


def suggest_entry_skill(
    *,
    project_root: Path,
    request: str,
    records: Mapping[str, Mapping[str, object]],
    client: object | None = None,
    environ: Mapping[str, str] | None = None,
) -> str:
    """Return one cookbook-selected skill name, or an empty fail-open result."""
    env = os.environ if environ is None else environ
    if not enabled(env) or not request.strip() or not records:
        return ""
    active_client = client or _build_client(env)
    if active_client is None:
        return ""

    by_name = {
        str(record.get("name") or lookup): record
        for lookup, record in records.items()
        if str(record.get("description") or "").strip()
    }
    if not by_name:
        return ""

    try:
        questions: dict[str, object] = {
            "which": {
                "type": "choice",
                "instructions": CHOICE_INSTRUCTIONS,
                "criteria": {
                    name: str(record.get("description") or "").strip()
                    for name, record in by_name.items()
                },
            }
        }
        for key, text in GATE_QUESTIONS.items():
            questions[f"gate::{key}"] = {"type": "noul", "instructions": text}
        state = {"request": request, "recent_context": ""}
        wide = active_client.system_one(
            state=state,
            questions=questions,
            model=str(env.get(MODEL_ENV) or (_provider_config(env) or {})["model"]),
        )
        wide_answers = _answers(wide)
        probabilities = _field(wide_answers["which"], "probabilities")
        if not isinstance(probabilities, Mapping):
            return ""
        ranked = sorted(probabilities.items(), key=lambda item: -float(item[1]))
        gate_values = {
            key.removeprefix("gate::"): float(_field(answer, "noul"))
            for key, answer in wide_answers.items()
            if key.startswith("gate::")
        }
        if set(gate_values) != set(GATE_QUESTIONS):
            return ""
        oriented = [
            (1.0 - value) if key in INVERTED_GATES else value
            for key, value in gate_values.items()
        ]
        if sum(oriented) / len(oriented) < GATE_THRESHOLD:
            return ""

        names = tuple(name for name, _ in ranked[:SHORTLIST] if name in by_name)
        if not names:
            return ""
        rerank_questions: dict[str, object] = {
            "which": {
                "type": "choice",
                "instructions": RERANK_INSTRUCTIONS,
                "criteria": {
                    name: (
                        f"{by_name[name].get('description', '')} — "
                        f"{_skill_excerpt(project_root, by_name[name])}"
                    )
                    for name in names
                },
            }
        }
        for name in names:
            rerank_questions[f"fits::{name}"] = {
                "type": "noul",
                "instructions": (
                    f"Does the skill '{name}' do the specific thing the user's request "
                    f"asks for? It is described as: {by_name[name].get('description', '')}"
                ),
            }
        detailed = active_client.system_one(
            state=state,
            questions=rerank_questions,
            model=str(env.get(MODEL_ENV) or (_provider_config(env) or {})["model"]),
        )
        detailed_answers = _answers(detailed)
        fits = {
            key.removeprefix("fits::"): float(_field(answer, "noul"))
            for key, answer in detailed_answers.items()
            if key.startswith("fits::")
        }
        if not fits or max(fits.values()) < FITS_THRESHOLD:
            return ""
        winner = str(_field(detailed_answers["which"], "choice"))
        return winner if winner in names else ""
    except Exception:
        return ""


def suggestion_context(skill_name: str) -> str:
    if not skill_name:
        return ""
    return (
        "<skill_relevance>\n"
        f"Relevant to the current request: {skill_name}. Ignore this if it does not "
        "fit what the user actually asked for.\n"
        "</skill_relevance>"
    )
