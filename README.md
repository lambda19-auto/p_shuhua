## p-shuhua

Проект с оркестратором `NeuroSeller` и агентами:
- `consult`
- `goodbye_soft`
- `goodbye_hard`

## Проверка импортов

Импорты внутри пакета `agents` сделаны относительными, поэтому код запускается напрямую из корня репозитория без несуществующего `src/`.

## Тестирование

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

Запуск:

```bash
RUN_API_TESTS=1 OPENAI_API_KEY=<ваш_ключ> python -m unittest -v tests.test_api_agent
```

Опционально можно ограничить число обработанных строк в каждом файле:

```bash
RUN_API_TESTS=1 OPENAI_API_KEY=<ваш_ключ> API_TEST_LIMIT=10 python -m unittest -v tests.test_api_agent
```
