## p-shuhua

Проект с оркестратором `NeuroSeller` и агентами:
- `consult`
- `goodbye_soft`
- `goodbye_hard`

## Проверка импортов

Импорты внутри пакета `agents` сделаны относительными, поэтому код запускается напрямую из корня репозитория без несуществующего `src/`.

## Табличные тесты в директории `tests`

Файлы для пакетных тестов:
- `tests/for_test_seller.xlsx`
- `tests/for_test_consult.xlsx`

> Эти бинарные файлы не хранятся в PR. Положите их в `tests/` вручную перед запуском.

Запуск (как в notebook, но с результатами в `tests/`):

```bash
python tests/run_table_tests.py
```

Скрипт создаёт:
- `tests/result_for_test_seller.xlsx`
- `tests/result_for_test_consult.xlsx`

Можно прогнать один файл:

```bash
python tests/run_table_tests.py \
  --single-input tests/for_test_seller.xlsx \
  --single-output tests/result_for_test_seller.xlsx
```
