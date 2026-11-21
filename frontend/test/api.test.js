import assert from 'node:assert/strict';
import test from 'node:test';
import { askQuestion } from '../src/api.js';

const question = 'Explain simple interest using a fictional example.';

test('submits one question to the API and returns its answer', async (t) => {
  const answer = 'A fictional $100 deposit at 2% simple interest earns $2 in one year.';
  const fetch = t.mock.method(globalThis, 'fetch', async () => Response.json({
    answer,
    database_function_used: false,
  }));

  assert.deepEqual(await askQuestion(question), { answer, databaseFunctionUsed: false });
  assert.equal(fetch.mock.callCount(), 1);
  const [url, options] = fetch.mock.calls[0].arguments;
  assert.equal(url.href, 'http://localhost:8000/api/ask');
  assert.equal(options.method, 'POST');
  assert.equal(options.headers['Content-Type'], 'application/json');
  assert.deepEqual(JSON.parse(options.body), { question });
});

test('passes a backend error detail to the form', async (t) => {
  const detail = 'OpenAI rejected the backend API key. Update OPENAI_API_KEY and restart the backend.';
  t.mock.method(globalThis, 'fetch', async () => Response.json({ detail }, { status: 503 }));
  await assert.rejects(askQuestion(question), { message: detail });
});

test('identifies the attempted API address when a connection fails', async (t) => {
  t.mock.method(globalThis, 'fetch', async () => { throw new TypeError('Failed to fetch'); });
  await assert.rejects(askQuestion(question), /Could not reach http:\/\/localhost:8000/);
});

for (const [name, payload] of [
  ['invalid JSON', '<html>Unexpected document</html>'],
  ['missing answer', '{}'],
  ['blank answer', '{"answer":" "}'],
  ['non-text answer', '{"answer":42}'],
]) {
  test(`rejects a successful response with ${name}`, async (t) => {
    t.mock.method(globalThis, 'fetch', async () => new Response(payload));
    await assert.rejects(askQuestion(question), /without a text answer/);
  });
}
