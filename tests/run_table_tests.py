"""Run NeuroSeller table-based test batches from the tests directory.

The script mirrors notebook-style processing:
- reads an Excel table with a required `request` column
- runs every request through NeuroSeller
- writes collected responses to a new Excel file
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.neuro_seller import NeuroSeller

if TYPE_CHECKING:
    import pandas as pd

DEFAULT_CASES = {
    "for_test_seller.xlsx": "result_for_test_seller.xlsx",
    "for_test_consult.xlsx": "result_for_test_consult.xlsx",
}


def _load_pandas() -> "pd":
    try:
        import pandas as pd  # type: ignore
    except ModuleNotFoundError as exc:  # pragma: no cover - environment dependent
        msg = (
            "Для табличных тестов требуется pandas + openpyxl. "
            "Установите зависимости и повторите запуск."
        )
        raise RuntimeError(msg) from exc

    return pd


def run_case(input_path: Path, output_path: Path) -> Path:
    pd = _load_pandas()

    if not input_path.exists():
        raise FileNotFoundError(
            f"Не найден входной файл: {input_path}. "
            "Скопируйте таблицу for_test_*.xlsx в директорию tests/."
        )

    df = pd.read_excel(input_path)
    if "request" not in df.columns:
        raise ValueError(f"В файле {input_path} отсутствует обязательная колонка 'request'.")

    seller = NeuroSeller()
    context = ""

    for index in range(len(df)):
        question = str(df.loc[index, "request"])
        answer, context = seller.run(question, context=context)
        df.loc[index, "response"] = answer
        context = ""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tests-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Директория с for_test_*.xlsx и куда писать result_*.xlsx.",
    )
    parser.add_argument(
        "--single-input",
        type=Path,
        help="Опционально: запустить только один Excel-файл.",
    )
    parser.add_argument(
        "--single-output",
        type=Path,
        help="Опционально: путь выходного файла для --single-input.",
    )
    args = parser.parse_args()

    if args.single_input and not args.single_output:
        raise ValueError("Для --single-input обязательно укажите --single-output.")

    if args.single_input and args.single_output:
        result = run_case(args.single_input, args.single_output)
        print(f"Готово: {result}")
        return

    for filename, result_name in DEFAULT_CASES.items():
        input_path = args.tests_dir / filename
        output_path = args.tests_dir / result_name
        result = run_case(input_path, output_path)
        print(f"Готово: {result}")


if __name__ == "__main__":
    main()
