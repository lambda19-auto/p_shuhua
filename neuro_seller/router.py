"""Router agent for intent detection."""
import asyncio
import os
import uuid_utils

from openai.types.shared import Reasoning
from agents import Agent, ModelSettings, Runner  #type:ignore
from agents.extensions.memory import SQLAlchemySession
from dotenv import load_dotenv, find_dotenv

from .consult import consult_agent
from .goodbye_hard import goodbye_hard_agent
from .goodbye_soft import goodbye_soft_agent


load_dotenv(find_dotenv())

database_url = os.getenv("DATABASE_URL")

if database_url is None:
    raise RuntimeError("DATABASE_URL is not set")

INSTRUCTION = """
# Роль

Ты сотрудник отдела маршрутизации обращений клиентов.

Твоя задача — внимательно прочитать сообщение клиента и определить, к какому агенту оно относится.

Ты не ведёшь диалог с клиентом.
Ты не отвечаешь на вопросы клиента.
Ты не объясняешь своё решение.

---

# Доступные интенты

## consult

Выбирай этот агент, если клиент:

* интересуется продуктом или услугой;
* задаёт вопросы;
* уточняет стоимость;
* уточняет сроки;
* уточняет условия сотрудничества;
* интересуется автоматизацией;
* интересуется возможностями продукта;
* интересуется кейсами;
* продолжает обсуждение;
* просит дополнительную информацию.

Примеры:

* Сколько стоит?
* Расскажите подробнее.
* Какие есть тарифы?
* А это можно интегрировать с CRM?
* Покажите примеры работ.
* Мне интересно узнать подробнее.

---

## goodbye_soft

Выбирай этот агент, если клиент вежливо завершает общение.

Обычно клиент:

* благодарит;
* сообщает, что получил нужную информацию;
* прощается;
* завершает разговор.

Примеры:

* Спасибо, всё понятно.
* Благодарю за консультацию.
* Хорошо, спасибо.
* Всего доброго.
* Спасибо, я подумаю.

---

## goodbye_hard

Выбирай этот агент, если клиент оскорбляет или не хочет продолжать общение.

Сюда относятся:

* оскорбления;
* агрессия;
* грубость;
* токсичность;
* угрозы;
* унижения;
* обвинения;
* отказ от услуг;
* отказ от общения;
* просьба больше не писать;
* нежелание продолжать разговор;
* спор ради спора;
* попытка конфликтовать.

Примеры:

* Не интересует.
* Больше не пишите.
* Мне ваши услуги не нужны.
* Отстаньте.
* Вы мошенники.
* Идите к чёрту.
* Хватит мне писать.

---
""".strip()


router_agent = Agent(
    name="router",
    instructions=INSTRUCTION,
    model="gpt-5.4-nano-2026-03-17",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="none"), 
        verbosity="low"),
    tools=[
        consult_agent.as_tool(
            tool_name="consult",
            tool_description="Ответы на вопросы клиента и консультация по услугам."
        ),
        goodbye_soft_agent.as_tool(
            tool_name="goodbye_soft",
            tool_description="Клиент вежливо завершает общение"
        ),
        goodbye_hard_agent.as_tool(
            tool_name="goodbye_hard",
            tool_description="Клиент оскорбляет или не хочет продолжать общение."
        )
    ],
    tool_use_behavior="stop_on_first_tool"
)

async def main(database_url: str):
    user_id = str(uuid_utils.uuid7())

    session = SQLAlchemySession.from_url(
        session_id=user_id,
        url=database_url,
        create_tables=True,
    )

    try:
        result = await Runner.run(
            router_agent,
            input="Здравствуйте, получил ваше письмо и хотел бы уточнить детали.",
            session=session,
        )
        print(result.final_output)

    finally:
        await session.engine.dispose()

if __name__ == "__main__":
    asyncio.run(main(database_url=database_url))