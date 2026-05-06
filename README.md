## p-shuhua

Проект с оркестратором `NeuroSeller` и агентами:
- `consult`
- `goodbye_soft`
- `goodbye_hard`

## Проверка импортов

Импорты внутри пакета `agents` сделаны относительными, поэтому код запускается напрямую из корня репозитория без несуществующего `src/`.

## Тестирование

> Напоминание: перед запуском тестов поместите файлы `for_test_consult.xlsx` и `for_test_seller.xlsx` в директорию `tests/`.

### 1) Быстрые unit-тесты (без API)

```bash
python -m unittest -v tests.test_neuro_seller
```

### 2) Интеграционный API-тест с обработкой Excel

`tests/test_api_agent.py` работает последовательно:
1. читает `tests/for_test_consult.xlsx`,
2. берет `request` по строкам,
3. отправляет запрос в `NeuroSeller` (через OpenAI API),
4. записывает ответ в `response`,
5. сохраняет таблицу в `tests/result_consult.xlsx`,
6. затем повторяет те же шаги для `tests/for_test_goodbye.xlsx`,
7. сохраняет результат в `tests/result_goodbye.xlsx`.

Запуск (ключ `OPENAI_API_KEY` подхватывается из файла `.env`):

```bash
RUN_API_TESTS=1 python -m unittest -v tests.test_api_agent
```

Опционально можно ограничить число обработанных строк в каждом файле:

```bash
RUN_API_TESTS=1 API_TEST_LIMIT=10 python -m unittest -v tests.test_api_agent
```


## Конфигурация модели

Модель OpenAI задаётся через переменную окружения `OPENAI_MODEL` в файле `.env`.

Пример:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Если `OPENAI_MODEL` не задана, по умолчанию используется `gpt-4.1-mini`.


### Способ вызова моделей

В проекте используется адаптер вызова OpenAI в `agents/openai_call.py`:
- для семейства `gpt-4.1*` используется `client.chat.completions.create(...)`;
- для остальных моделей (включая `gpt-5*`) используется `client.responses.create(...)`.

Это позволяет переключать `OPENAI_MODEL` в `.env` без изменения кода агентов.
