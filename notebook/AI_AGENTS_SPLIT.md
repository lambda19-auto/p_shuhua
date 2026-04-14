# Разбиение `shuhua.ipynb` на файлы AI-агентов

Из ноутбука вынесены агенты в пакет `src/p_shuhua/agents/`:

- `router_agent.py` — роутер интентов (`consult`, `goodbye_soft`, `goodbye_hard`)
- `consult_agent.py` — консультационный агент
- `goodbye_soft_agent.py` — мягкое завершение диалога
- `goodbye_hard_agent.py` — жёсткое завершение диалога
- `neuro_seller.py` — оркестратор `NeuroSeller`
- `__init__.py` — экспорт `NeuroSeller`, `goodbye_soft`, `goodbye_hard`

## Пример использования в коде

```python
from p_shuhua.agents import NeuroSeller

seller = NeuroSeller()
answer, context = seller.run("Нужно автоматизировать заявки", context="")
print(answer)
```

## Тестирование запуском через `python3`

Добавлен CLI-скрипт `scripts/test_agents.py`, который повторяет логику теста из ноутбука:

```bash
python3 scripts/test_agents.py \
  --input src/p_shuhua/notebook/for_test_seller.xlsx \
  --output src/p_shuhua/notebook/result_consult_cli.xlsx
```

Требования:
- во входном файле должна быть колонка `request`
- должны быть настроены переменные окружения для OpenAI API (например, `OPENAI_API_KEY`)
