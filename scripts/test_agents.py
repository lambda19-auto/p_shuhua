#!/usr/bin/env python3
"""Run notebook-style agent tests from command line."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from p_shuhua.agents import NeuroSeller  # noqa: E402


def run_test(input_file: Path, output_file: Path) -> None:
    df = pd.read_excel(input_file)
    if "request" not in df.columns:
        raise ValueError(f"В файле {input_file} нет колонки 'request'.")

    seller = NeuroSeller()
    responses: list[str] = []

    for request in df["request"].fillna("").astype(str):
        answer, _ = seller.run(request, context="")
        responses.append(answer)

    df["response"] = responses
    df.to_excel(output_file, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Тестирование AI-агентов из командной строки через python3.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Путь до входного .xlsx файла (должен содержать колонку 'request').",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Путь до выходного .xlsx файла с ответами агентов.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_test(args.input, args.output)
    print(f"Готово: результаты сохранены в {args.output}")


if __name__ == "__main__":
    main()
