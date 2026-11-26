import assert from 'node:assert/strict';
import test from 'node:test';
import { askDocuments } from '../src/api.js';

test('retrieval-only requests use the offline endpoint', async (t) => {
  const data = { passages: [{ id: 'company-profile:1' }] };
  const fetch = t.mock.method(globalThis, 'fetch', async () => Response.json(data));
  assert.deepEqual(await askDocuments('Where is the office?', true), data);
  const [url, options] = fetch.mock.calls[0].arguments;
  assert.equal(url.pathname, '/api/documents/retrieve');
  assert.deepEqual(JSON.parse(options.body), { question: 'Where is the office?' });
});

test('document questions submit independently and preserve abstention', async (t) => {
  const data = { passages: [], status: 'not_covered', answer: "The documents don't cover this question.", citations: [] };
  const fetch = t.mock.method(globalThis, 'fetch', async () => Response.json(data));
  assert.deepEqual(await askDocuments('Is there a fee?'), data);
  const [url, options] = fetch.mock.calls[0].arguments;
  assert.equal(url.pathname, '/api/documents/ask');
  assert.deepEqual(JSON.parse(options.body), { question: 'Is there a fee?' });
});
