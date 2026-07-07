# p-shuhua

TypeScript AI-agent for lambda19.org based on the OpenAI Agents SDK.

## Setup

Configure `.env`:

```env
OPENAI_API_KEY=your_api_key
```

Install dependencies:

```bash
npm install
```

Build:

```bash
npm run build
```

Run the sample router request:

```bash
npm start
```

## Integration API Test

File:

```text
tests/test-api-agent.ts
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

Run API tests:

```bash
npm run test:api
```

For quick testing, process only the first N rows:

```bash
RUN_API_TESTS=1 API_TEST_LIMIT=10 tsx --test tests/test-api-agent.ts
```

## Excel format

| request                               |
| ------------------------------------- |
| Hello, tell me more about the service |
| How much does implementation cost?    |
| Thanks, everything is clear           |

The columns `response`, `session_id`, and `toolspan` are created automatically.
