# p-shuhua

TypeScript implementation of the `lambda19` sales-routing AI agent.

The project uses the official OpenAI Agents SDK for TypeScript (`@openai/agents`). The router agent reads a customer message, chooses one of the specialized agents through `Agent.asTool(...)`, and returns the first tool result with `toolUseBehavior: 'stop_on_first_tool'`.

## Structure

```text
src/main.ts
src/neuro-seller/router.ts
src/neuro-seller/consult.ts
src/neuro-seller/goodbye-soft.ts
src/neuro-seller/goodbye-hard.ts
tests/test-api-agent.test.ts
```

## Environment

Create `.env` in the repository root:

```env
OPENAI_API_KEY=your_api_key
```

## Install

```bash
npm install
```

## Type check

```bash
npm run build
```

## Run a single request

```bash
npm start -- "Здравствуйте, получил ваше письмо и хотел бы уточнить детали."
```

## Integration API test

File:

```text
tests/test-api-agent.test.ts
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

Run:

```bash
RUN_API_TESTS=1 npm run test:api
```

For quick testing, process only the first N rows:

```bash
RUN_API_TESTS=1 API_TEST_LIMIT=10 npm run test:api
```

Without `RUN_API_TESTS=1`, API tests are skipped so local checks can run without credentials or network calls.
