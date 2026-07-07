import 'dotenv/config';
import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { test } from 'node:test';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import XLSX from 'xlsx';

import { runRouterOnce } from '../neuro_seller/router.js';

type ApiRow = {
  request?: string;
};

type ResultRow = {
  row_id: number;
  request: string;
  response: string;
  toolspan: string;
  session_id: string;
};

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const testsDir = join(root, 'tests');

function extractToolspan(result: { newItems?: unknown[] }): string {
  for (const item of result.newItems ?? []) {
    if (typeof item !== 'object' || item === null) {
      continue;
    }

    const candidate = item as Record<string, unknown>;
    const directName = candidate.name;
    if (typeof directName === 'string' && directName.length > 0) {
      return directName;
    }

    const rawItem = candidate.rawItem;
    if (typeof rawItem === 'object' && rawItem !== null) {
      const rawName = (rawItem as Record<string, unknown>).name;
      if (typeof rawName === 'string' && rawName.length > 0) {
        return rawName;
      }
    }
  }

  return 'unknown';
}

async function processFile(sourceFile: string, resultFile: string): Promise<void> {
  const inputPath = join(testsDir, sourceFile);
  assert.ok(existsSync(inputPath), `Input file not found: ${inputPath}`);

  const workbook = XLSX.readFile(inputPath);
  const firstSheetName = workbook.SheetNames[0];
  assert.ok(firstSheetName, `No worksheets found in ${sourceFile}`);

  const worksheet = workbook.Sheets[firstSheetName];
  const inputRows = XLSX.utils.sheet_to_json<ApiRow>(worksheet, { defval: '' });

  assert.ok(
    inputRows.length === 0 || Object.hasOwn(inputRows[0], 'request'),
    `Column 'request' not found in ${sourceFile}`,
  );

  const limit = process.env.API_TEST_LIMIT ? Number(process.env.API_TEST_LIMIT) : undefined;
  const rows = Number.isInteger(limit) && limit !== undefined ? inputRows.slice(0, limit) : inputRows;

  const resultRows: ResultRow[] = [];

  for (const [index, row] of rows.entries()) {
    const request = String(row.request ?? '');
    const { response, sessionId, result } = await runRouterOnce(request);

    resultRows.push({
      row_id: index + 1,
      request,
      response,
      toolspan: extractToolspan(result),
      session_id: sessionId,
    });
  }

  const outputWorkbook = XLSX.utils.book_new();
  const outputWorksheet = XLSX.utils.json_to_sheet(resultRows);
  XLSX.utils.book_append_sheet(outputWorkbook, outputWorksheet, 'results');
  XLSX.writeFile(outputWorkbook, join(testsDir, resultFile));
}

const runApiTests = process.env.RUN_API_TESTS === '1';
const apiTest = runApiTests ? test : test.skip;

apiTest('process consult Excel requests through router', async () => {
  assert.ok(process.env.OPENAI_API_KEY, 'OPENAI_API_KEY is not configured.');
  await processFile('for_test_consult.xlsx', 'result_consult.xlsx');
});

apiTest('process goodbye Excel requests through router', async () => {
  assert.ok(process.env.OPENAI_API_KEY, 'OPENAI_API_KEY is not configured.');
  await processFile('for_test_goodbye.xlsx', 'result_goodbye.xlsx');
});
