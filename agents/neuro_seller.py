"""Neuro-seller orchestrator over split agent files."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .consult_agent import consult
from .goodbye_hard_agent import goodbye_hard
from .goodbye_soft_agent import goodbye_soft
from .router_agent import route_intents

EXECUTION_ORDER = ["goodbye_hard", "consult", "goodbye_soft"]

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


class NeuroSeller:
    """Main orchestrator class."""

    def __init__(self, client: OpenAI | None = None) -> None:
        self.client = client or OpenAI()
        self.handlers: dict[str, Callable[[str, str], str]] = {
            "consult": lambda text, context: consult(self.client, text, context),
            "goodbye_hard": lambda text, context: goodbye_hard(self.client, text, context),
            "goodbye_soft": lambda text, context: goodbye_soft(self.client, text, context),
        }

    def run(self, text: str, context: str = "") -> tuple[str, str]:
        """Run all relevant agents based on router intents."""
        print("request:\n", text)
        context = f"{context}\nКлиент: {text}".strip()

        router_result = route_intents(self.client, text, context)
        intents = self._normalize_intents(router_result.get("intents", []))
        answers: list[str] = []

        for intent in intents:
            handler = self.handlers.get(intent)
            if not handler:
                continue

            answer = handler(text, context)
            context += f"\nЯ: {answer}"
            answers.append(answer)

            if intent == "goodbye_hard":
                break

        final_answer = "\n".join(answers)
        return final_answer, context

    def _normalize_intents(self, raw_intents: object) -> list[str]:
        """Filter router output to known intents and sort by execution order."""
        if not isinstance(raw_intents, list):
            return ["consult"]

        known_intents = set(EXECUTION_ORDER)
        intents: list[str] = []

        for intent in raw_intents:
            if not isinstance(intent, str):
                continue
            if intent not in known_intents:
                continue
            if intent in intents:
                continue
            intents.append(intent)

        if not intents:
            return ["consult"]

        return sorted(intents, key=EXECUTION_ORDER.index)
