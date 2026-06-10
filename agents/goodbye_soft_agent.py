"""Soft goodbye agent."""

from __future__ import annotations

import os

from openai import OpenAI

from .openai_call import generate_text

INSTRUCTION = """
Ты — Дарья, менеджер по продажам.

Твоя задача — корректно завершить диалог после проведённой консультации.

Контекст:
Диалог завершён в нормальном рабочем формате. Общение закрывается без конфликта.

Стиль общения:

    Тон: Профессиональный, спокойный, доброжелательный.
    Формулировки: Краткие и чёткие.

Ограничения:

    Не инициируй новый диалог.
    Не задавай вопросов.
    Не предлагай дополнительные услуги.
    Ответ 1–3 коротких предложения.
    Без подписей и смайлов.

Структура:

    - Краткое подведение итогов или фиксация завершения.
    - Нейтральное пожелание.
    - Точка.
""".strip()

DEFAULT_MODEL = "gpt-4.1-mini"


def goodbye_soft(
    client: OpenAI,
    answer: str,
    context: str,
    instruction: str = INSTRUCTION,
    model: str | None = None,
    verbose: int = 1,
) -> str:
    """Return soft-close message."""
    message = f"""
    {instruction}

    Пожалуйста, давай действовать последовательно:
    1. Ознакомся с контекстом диалога.
    2. Проанализируй полученное сообщение.
    3. Сформулируй и выведи только ответ.

    Контекст: {context}
    Сообщение: {answer}
    """

    selected_model = model or os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    result = generate_text(client=client, model=selected_model, message=message)

    if verbose:
        print("\n goodbye_soft: \n", result)

    return result
