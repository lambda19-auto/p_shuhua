import 'dotenv/config';

import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';
import { test } from 'node:test';
import { dirname, resolve } from 'node:path';

import * as XLSX from 'xlsx';

import { runRouterOnce } from '../src/neuro-seller/router.js';

type ResultRow = {
  row_id: number;
  request: string;
  response: string;
  toolspan: string;
  session_id: string;
};

const root = resolve(import.meta.dirname, '..');
const testsDir = resolve(root, 'tests');

function readRequests(sourceFile: string): string[] {
  const workbook = XLSX.readFile(resolve(testsDir, sourceFile));
  const sheetName = workbook.SheetNames[0];
  assert.ok(sheetName, `Workbook ${sourceFile} must contain at least one sheet.`);
  const rows = XLSX.utils.sheet_to_json<Record<string, unknown>>(
    workbook.Sheets[sheetName],
  );

  assert.ok(
    rows.every((row) => Object.hasOwn(row, 'request')),
    `Column 'request' not found in ${sourceFile}`,
  );

  const limit = process.env.API_TEST_LIMIT
    ? Number.parseInt(process.env.API_TEST_LIMIT, 10)
    : undefined;

  return rows
    .slice(0, limit)
    .map((row) => String(row.request ?? ''));
}

async function processFile(sourceFile: string, resultFile: string): Promise<void> {
  if (process.env.RUN_API_TESTS !== '1') {
    test.skip('Set RUN_API_TESTS=1 to run API integration tests.');
    return;
  }

  assert.ok(process.env.OPENAI_API_KEY, 'OPENAI_API_KEY is not configured.');

  const rows: ResultRow[] = [];
  const requests = readRequests(sourceFile);

  for (const [index, request] of requests.entries()) {
    const { response, toolspan, sessionId } = await runRouterOnce(request);
    rows.push({
      row_id: index + 1,
      request,
      response,
      toolspan,
      session_id: sessionId,
    });
  }

  const outputPath = resolve(testsDir, resultFile);
  mkdirSync(dirname(outputPath), { recursive: true });

  const workbook = XLSX.utils.book_new();
  const worksheet = XLSX.utils.json_to_sheet(rows);
  XLSX.utils.book_append_sheet(workbook, worksheet, 'results');
  XLSX.writeFile(workbook, outputPath);

  console.log(`Saved: ${outputPath}`);
}

test('process consult Excel requests', async () => {
  await processFile('for_test_consult.xlsx', 'result_consult.xlsx');
});

test('process goodbye Excel requests', async () => {
  await processFile('for_test_goodbye.xlsx', 'result_goodbye.xlsx');
});
