"""API integration test for full system routing via router agent."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
import unittest

import pandas as pd
import uuid_utils

from dotenv import load_dotenv, find_dotenv
from agents import Runner
from agents.extensions.memory import AsyncSQLiteSession

from neuro_seller.router import router_agent


# Load .env using find_dotenv (more robust in monorepos / nested runs)
load_dotenv(find_dotenv())

ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"


class TestApiSystemFromExcel(unittest.TestCase):
    """Integration test for full routing system (router + tools)."""

    @classmethod
    def setUpClass(cls) -> None:
        if os.getenv("RUN_API_TESTS") != "1":
            raise unittest.SkipTest(
                "Set RUN_API_TESTS=1 to run API integration tests."
            )

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not configured.")

    def _extract_toolspan(self, result) -> str:
        """
        Extract tool/agent used by router (Agent-as-Tool).
        Fallback: 'unknown'
        """
        try:
            for item in getattr(result, "new_items", []):

                # direct name (newer SDK)
                name = getattr(item, "name", None)
                if name:
                    return str(name)

                # raw item fallback
                raw = getattr(item, "raw_item", None)
                if raw:
                    name = getattr(raw, "name", None)
                    if name:
                        return str(name)

        except Exception:
            pass

        return "unknown"

    async def _run_once(self, text: str) -> tuple[str, str, str]:
        session_id = str(uuid_utils.uuid7())

        session = AsyncSQLiteSession(
            session_id=session_id,
            db_path="users.db",
        )

        try:
            result = await Runner.run(
                starting_agent=router_agent,
                input=text,
                session=session,
            )

            response = str(result.final_output)
            toolspan = self._extract_toolspan(result)

            return response, toolspan, session_id

        finally:
            await session.close()

    def _process_file(self, source_file: str, result_file: str) -> None:
        input_path = TESTS_DIR / source_file

        if not input_path.exists():
            self.fail(f"Input file not found: {input_path}")

        df = pd.read_excel(input_path)

        if "request" not in df.columns:
            self.fail(f"Column 'request' not found in {source_file}")

        limit = os.getenv("API_TEST_LIMIT")
        if limit:
            df = df.head(int(limit))

        responses: list[str] = []
        toolspans: list[str] = []
        session_ids: list[str] = []

        for request in df["request"].fillna("").astype(str):
            response, toolspan, session_id = asyncio.run(
                self._run_once(request)
            )

            responses.append(response)
            toolspans.append(toolspan)
            session_ids.append(session_id)

        output_df = pd.DataFrame(
            {
                "row_id": range(1, len(df) + 1),
                "request": df["request"],
                "response": responses,
                "toolspan": toolspans,
                "session_id": session_ids,
            }
        )

        output_path = TESTS_DIR / result_file
        output_df.to_excel(output_path, index=False)

        print(f"\nSaved: {output_path}")

    def test_process_consult(self) -> None:
        self._process_file(
            source_file="for_test_consult.xlsx",
            result_file="result_consult.xlsx",
        )

    def test_process_goodbye(self) -> None:
        self._process_file(
            source_file="for_test_goodbye.xlsx",
            result_file="result_goodbye.xlsx",
        )


if __name__ == "__main__":
    unittest.main()