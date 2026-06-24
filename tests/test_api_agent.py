"""API integration test that processes Excel datasets and writes generated responses."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
import unittest

import pandas as pd
from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import Runner  # type: ignore

from neuro_seller.consult import consult_agent
from neuro_seller.goodbye_soft import goodbye_soft_agent


ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"

load_dotenv(ROOT / ".env")


class TestApiAgentFromExcel(unittest.TestCase):
    """Integration test using real OpenAI API."""

    @classmethod
    def setUpClass(cls) -> None:
        if os.getenv("RUN_API_TESTS") != "1":
            raise unittest.SkipTest(
                "Set RUN_API_TESTS=1 to run API integration tests."
            )

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not configured.")

        cls.client = AsyncOpenAI()

    def _process_file(
        self,
        source_file: str,
        result_file: str,
        agent,
    ) -> None:
        input_path = TESTS_DIR / source_file

        if not input_path.exists():
            self.fail(f"Input file not found: {input_path}")

        df = pd.read_excel(input_path)

        if "request" not in df.columns:
            self.fail(
                f"Column 'request' not found in {source_file}"
            )

        limit = os.getenv("API_TEST_LIMIT")

        if limit:
            df = df.head(int(limit))

        responses: list[str] = []

        async def generate(text: str) -> str:
            result = await Runner.run(
                starting_agent=agent,
                input=text,
            )
            return str(result.final_output)

        for request in df["request"].fillna("").astype(str):
            response = asyncio.run(generate(request))
            responses.append(response)

        df["response"] = responses

        output_path = TESTS_DIR / result_file
        df.to_excel(output_path, index=False)

        print(f"\nSaved: {output_path}")

    def test_process_consult(self) -> None:
        self._process_file(
            source_file="for_test_consult.xlsx",
            result_file="result_consult.xlsx",
            agent=consult_agent,
        )

    def test_process_goodbye(self) -> None:
        self._process_file(
            source_file="for_test_goodbye.xlsx",
            result_file="result_goodbye.xlsx",
            agent=goodbye_soft_agent,
        )


if __name__ == "__main__":
    unittest.main()
