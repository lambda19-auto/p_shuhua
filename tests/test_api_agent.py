"""API integration test that processes Excel datasets and writes generated responses."""

from __future__ import annotations

import os
from pathlib import Path
import unittest

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from agents.neuro_seller import NeuroSeller

ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"

load_dotenv(ROOT / ".env")


class TestNeuroSellerApiFromFiles(unittest.TestCase):
    """Read request rows from Excel files, call NeuroSeller, and save result files."""

    @classmethod
    def setUpClass(cls) -> None:
        if os.getenv("RUN_API_TESTS") != "1":
            raise unittest.SkipTest("Set RUN_API_TESTS=1 to run paid OpenAI API tests.")

        if not os.getenv("OPENAI_API_KEY"):
            raise unittest.SkipTest("OPENAI_API_KEY is required for API tests.")

        cls.limit = int(os.getenv("API_TEST_LIMIT", "0"))
        cls.seller = NeuroSeller(client=OpenAI())

    def _process_table(self, source_name: str, result_name: str) -> None:
        source_file = TESTS_DIR / source_name
        result_file = TESTS_DIR / result_name

        if not source_file.exists():
            raise FileNotFoundError(f"Test file not found: {source_file}")

        frame = pd.read_excel(source_file)

        if "request" not in frame.columns:
            raise AssertionError(f"Column 'request' not found in {source_file}")

        if "response" not in frame.columns:
            frame["response"] = ""
        else:
            frame["response"] = frame["response"].astype(object)

        processed = 0
        for row_index, request in frame["request"].items():
            request_text = "" if pd.isna(request) else str(request).strip()
            if not request_text:
                continue

            answer, _ = self.seller.run(request_text)
            frame.at[row_index, "response"] = (answer or "").strip()

            processed += 1
            if self.limit > 0 and processed >= self.limit:
                break

        frame.to_excel(result_file, index=False)

    def test_process_consult_then_goodbye(self) -> None:
        """Process consult table first, then goodbye table, saving two result files."""
        self._process_table("for_test_consult.xlsx", "result_consult.xlsx")
        self._process_table("for_test_goodbye.xlsx", "result_goodbye.xlsx")


if __name__ == "__main__":
    unittest.main()
