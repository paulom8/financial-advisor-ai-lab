const apiBaseUrl = import.meta.env?.VITE_API_URL?.trim() || 'http://localhost:8000';

export async function askQuestion(question) {
  let endpoint;
  try {
    const base = apiBaseUrl.replace(/\/+$/, '');
    endpoint = new URL(`${base}/api/ask`, globalThis.location?.origin);
  } catch {
    throw new Error('Check VITE_API_URL and restart Vite. The configured API address is invalid.');
  }

  let response;
  try {
    response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
  } catch {
    throw new Error(`Could not reach ${endpoint.origin}. Check that FastAPI is running at that address and allows this page’s origin.`);
  }

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = data?.detail;
    if (typeof detail === 'string') throw new Error(detail);
    throw new Error(`The API could not process the question (HTTP ${response.status}).`);
  }
  if (typeof data?.answer !== 'string' || !data.answer.trim()) {
    throw new Error('The API returned a response without a text answer.');
  }
  if (typeof data?.database_function_used !== 'boolean') {
    throw new Error('The API response is missing database function status.');
  }
  return { answer: data.answer, databaseFunctionUsed: data.database_function_used };
}
