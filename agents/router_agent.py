"""Router agent for intent detection."""

from __future__ import annotations

import os

import json
from typing import Any

from openai import OpenAI

from .openai_call import generate_text

INSTRUCTION = """
Ты — системный маршрутизатор диалога.

Твоя задача — определить интенты в сообщении клиента.

Ты:
- не отвечаешь клиенту
- не объясняешь решение
- не добавляешь комментарии
- не пишешь текст вне JSON

Ты возвращаешь ТОЛЬКО корректный JSON-объект.

Структура ответа:
{
  "intents": ["<интент>"]
}

Допустимые значения name:
- "consult"
- "goodbye_soft"
- "goodbye_hard"

Определения интентов:

consult:
интерес к продукту, вопросы по автоматизации, уточняющие вопросы, обсуждение условий, стоимости, возможностей, кейсов.

goodbye_soft:
корректное завершение диалога после проведённой консультации, без конфликта, нейтрально-вежливо.

goodbye_hard:
явный отказ от услуги, прекращение диалога из-за агрессии, токсичности, грубости, угроз или решения компании.

Правила приоритета (строгий порядок проверки):

1. Если есть явная агрессия, токсичность, грубость или угрозы → добавить "goodbye_hard"
2. Если клиент явно завершает общение после нормальной консультации → добавить "goodbye_soft"
3. Во всех остальных случаях → добавить "consult"

Никакого текста вне JSON.
JSON должен быть валидным.
""".strip()
DEFAULT_MODEL = "gpt-4.1-mini"


def route_intents(
    client: OpenAI,
    answer: str,
    context: str,
    instruction: str = INSTRUCTION,
    model: str | None = None,
    verbose: int = 1,
) -> dict[str, Any]:
    """Return intents in JSON-compatible dictionary."""
    message = f"""
    {instruction}

    Контекст: {context}
    Сообщение: {answer}
    """

    selected_model = model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    raw = generate_text(client=client, model=selected_model, message=message)

    try:
        result = json.loads(raw)
        if not isinstance(result, dict):
            result = {"intents": []}
    except json.JSONDecodeError:
        result = {"intents": []}

    if verbose:
        print("\nrouter:")
        print(json.dumps(result, indent=4, ensure_ascii=False))

    return result
