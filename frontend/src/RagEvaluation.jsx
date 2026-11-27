import React, { useState } from 'react';
import { runRagEvaluation } from './api.js';

function verdict(passed) {
  if (passed == null) return 'Not scored';
  return passed ? 'Pass' : 'Fail';
}

function MethodResult({ result }) {
  const titles = { keyword: 'Keyword search', vector: 'Saved vector search' };
  return (
    <section>
      <h4>{titles[result.method]}</h4>
      <p><strong>Retrieval:</strong> {verdict(result.retrieval_passed)}</p>
      <p><strong>Retrieved:</strong> {result.passages.join(', ') || 'None'}</p>
      <p><strong>Answer:</strong> {verdict(result.answer_passed)}</p>
      {result.answer && <p>{result.answer}</p>}
      {result.citations.length > 0 && <p><strong>Cited:</strong> {result.citations.join(', ')}</p>}
      {result.error && <p className="error">{result.error}</p>}
    </section>
  );
}

export default function RagEvaluation() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function run() {
    setBusy(true);
    setReport(null);
    setError('');
    try {
      setReport(await runRagEvaluation());
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel">
      <h2>RAG evaluation</h2>
      <p>Compare keyword and saved-vector search on three fixed demo questions.</p>
      <button type="button" onClick={run} disabled={busy}>Run RAG evaluation</button>
      <p className="privacy-note">This calls OpenAI. The checks use expected passages, facts, citations and whether the model declines an unsupported question.</p>
      <p role="status">{busy ? 'Evaluating retrieval and answers…' : report ? 'Evaluation complete.' : ''}</p>
      {error && <p role="alert" className="error">{error}</p>}
      {report?.cases.map((item) => (
        <section key={item.question}>
          <h3>{item.question}</h3>
          <p><strong>Expected answer:</strong> {item.expected_answer}</p>
          {item.expected_passage
            ? <p><strong>Expected passage:</strong> {item.expected_passage}</p>
            : <p>Retrieval is unscored because no passage contains the answer.</p>}
          <div className="case-answers">
            {item.results.map((result) => <MethodResult key={result.method} result={result} />)}
          </div>
        </section>
      ))}
    </section>
  );
}
