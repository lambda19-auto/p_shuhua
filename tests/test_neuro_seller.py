"""Tests for NeuroSeller intent normalization and execution safety."""

from __future__ import annotations

from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import openai  # noqa: F401
except ModuleNotFoundError:
    openai_stub = types.ModuleType("openai")

    class _OpenAI:  # pragma: no cover - compatibility stub for import-time only
        pass

    openai_stub.OpenAI = _OpenAI
    sys.modules["openai"] = openai_stub

from agents.neuro_seller import NeuroSeller


class TestNeuroSellerIntents(unittest.TestCase):
    """Validate orchestration is resilient to malformed router output."""

    def setUp(self) -> None:
        self.seller = NeuroSeller(client=object())
        self.seller.handlers = {
            "consult": lambda text, context: "consult_answer",
            "goodbye_hard": lambda text, context: "goodbye_hard_answer",
            "goodbye_soft": lambda text, context: "goodbye_soft_answer",
        }

    def test_run_ignores_unknown_intent_and_falls_back(self) -> None:
        with patch(
            "agents.neuro_seller.route_intents",
            return_value={"intents": ["unknown_label"]},
        ):
            answer, _ = self.seller.run("Привет")

        self.assertEqual(answer, "consult_answer")

    def test_run_skips_unknown_and_sorts_known_intents(self) -> None:
        with patch(
            "agents.neuro_seller.route_intents",
            return_value={"intents": ["goodbye_soft", "???", "consult"]},
        ):
            answer, _ = self.seller.run("Спасибо")

        self.assertEqual(answer, "consult_answer\ngoodbye_soft_answer")


if __name__ == "__main__":
    unittest.main()
