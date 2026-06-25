# Testing

## Integration API Test

File:

```text
tests/test_api_agent.py
```

Input data:

```text
tests/for_test_consult.xlsx
tests/for_test_goodbye.xlsx
```

Required column:

```text
request
```

After execution, the following files are created:

```text
tests/result_consult.xlsx
tests/result_goodbye.xlsx
```

The following columns are added to the results:

```text
response
session_id
toolspan
```

## Running

Before running, configure `.env`:

```env
OPENAI_API_KEY=your_api_key
```

Run:

```bash
RUN_API_TESTS=1 python -m unittest -v tests.test_api_agent
```

## Row limit

For quick testing, you can process only the first N rows:

```bash
RUN_API_TESTS=1 API_TEST_LIMIT=10 python -m unittest -v tests.test_api_agent
```

## Excel format

Example:

| request                               |
| ------------------------------------- |
| Hello, tell me more about the service |
| How much does implementation cost?    |
| Thanks, everything is clear           |

The columns `response`, `session_id`, `toolspan` will be created automatically.


---


# Тестирование

## Интеграционный API-тест

Файл:

```text
tests/test_api_agent.py
```

Входные данные:

```text
tests/for_test_consult.xlsx
tests/for_test_goodbye.xlsx
```

Обязательная колонка:

```text
request
```

После выполнения теста создаются:

```text
tests/result_consult.xlsx
tests/result_goodbye.xlsx
```

В результаты добавляется колонка:

```text
response
session_id
toolspan
```

---

## Запуск

Перед запуском настройте `.env`:

```env
OPENAI_API_KEY=your_api_key
```

Запуск:

```bash
RUN_API_TESTS=1 python -m unittest -v tests.test_api_agent
```

---

## Ограничение количества строк

Для быстрого тестирования можно обработать только первые N строк:

```bash
RUN_API_TESTS=1 API_TEST_LIMIT=10 python -m unittest -v tests.test_api_agent
```

---

## Формат Excel

Пример:

| request                                      |
| -------------------------------------------- |
| Здравствуйте, расскажите подробнее об услуге |
| Сколько стоит внедрение?                     |
| Спасибо, всё понятно                         |

Колонка `response`, `session_id`, `toolspan` будет создана автоматически.
