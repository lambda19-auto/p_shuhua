"""Soft goodbye agent."""

from __future__ import annotations

from openai import OpenAI

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

    1. Краткое подведение итогов или фиксация завершения.
    2. Нейтральное пожелание.
    3. Точка.
""".strip()

MODEL = "gpt-5-nano-2025-08-07"


def goodbye_soft(
    client: OpenAI,
    answer: str,
    context: str,
    instruction: str = INSTRUCTION,
    model: str = MODEL,
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

    completion = client.responses.create(
        model=model,
        input=message,
        reasoning={"effort": "minimal"},
    )
    result = completion.output_text

    if verbose:
        print("\n goodbye_soft: \n", result)

    return result
