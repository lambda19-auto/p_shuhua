# Разбиение `shuhua.ipynb` на файлы AI-агентов

Из ноутбука вынесены агенты в пакет `agents/`:

- `router_agent.py` — роутер интентов (`consult`, `goodbye_soft`, `goodbye_hard`)
- `consult_agent.py` — консультационный агент
- `goodbye_soft_agent.py` — мягкое завершение диалога
- `goodbye_hard_agent.py` — жёсткое завершение диалога
- `neuro_seller.py` — оркестратор `NeuroSeller`
- `__init__.py` — экспорт `NeuroSeller`, `goodbye_soft`, `goodbye_hard`

## Пример использования в коде

```python
from agents import NeuroSeller

seller = NeuroSeller()
answer, context = seller.run("Нужно автоматизировать заявки", context="")
print(answer)
```

## Тестирование запуском через `python3`

Добавлен CLI-скрипт `tests/run_table_tests.py`, который повторяет логику теста из ноутбука и пишет результаты в `tests/`:

```bash
python3 tests/run_table_tests.py \
  --single-input tests/for_test_seller.xlsx \
  --single-output tests/result_for_test_seller.xlsx
```

Требования:
- во входном файле должна быть колонка `request`
- должны быть настроены переменные окружения для OpenAI API (например, `OPENAI_API_KEY`)
- `tests/for_test_seller.xlsx` и `tests/for_test_consult.xlsx` добавляются вручную (бинарники не хранятся в PR)
