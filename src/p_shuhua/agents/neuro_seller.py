"""Neuro-seller orchestrator over split agent files."""

from __future__ import annotations

from collections.abc import Callable

from openai import OpenAI

from p_shuhua.agents.consult_agent import consult
from p_shuhua.agents.goodbye_hard_agent import goodbye_hard
from p_shuhua.agents.goodbye_soft_agent import goodbye_soft
from p_shuhua.agents.router_agent import route_intents

EXECUTION_ORDER = ["goodbye_hard", "consult", "goodbye_soft"]


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
        intents = router_result.get("intents", [])

        if not intents:
            intents = ["consult"]

        intents = sorted(intents, key=lambda intent: EXECUTION_ORDER.index(intent))
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
