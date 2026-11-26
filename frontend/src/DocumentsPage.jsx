import React, { useState } from 'react';
import { askDocuments } from './api.js';
import LabNav from './LabNav.jsx';

const EXAMPLES = [
  'How often does the demo policy review a savings goal?',
  'Is there a fee for changing a goal?',
  'Where is the company located?',
  'How many employees does it have?',
  'What are its opening hours?',
  'How long has the company been operating?',
  'Who is the main contact?',
  'Who is the main contact, and where is the office?',
  'What AI consulting services are offered?',
];

function Result({ result }) {
  const cited = result.passages.filter((p) => result.citations?.includes(p.id));
  return (
    <article className="panel">
      <h2>{result.question}</h2>
      <p className="privacy-note">{result.retrieveOnly ? 'Retrieval only · No model call' : 'Document answer'}</p>
      {!result.retrieveOnly && (
        <>
          <h3>Answer</h3>
          {result.status === 'error' ? <p role="alert" className="error">{result.error}</p> :
            <p className="answer-text">{result.answer}</p>}
          {result.status === 'not_covered' && (
            <div className="contact-box">
              <p>Still have questions? Email Paulo and we will contact you within 48 hours. (Fictional demo policy.)</p>
              <a className="contact-link" href={`mailto:paulom8@hotmail.com?subject=${encodeURIComponent('Paulo Financial Planning enquiry')}`}>Email Paulo</a>
            </div>
          )}
          {cited.length > 0 && <><h3>Citations</h3><ul>{cited.map((p) => <li key={p.id}>{p.document} — {p.section}</li>)}</ul></>}
        </>
      )}
      <h3>Retrieved passages ({result.passages.length})</h3>
      {result.retrievalFailed ? <p>Retrieval result unavailable.</p> : result.passages.length === 0 && <p>No matching passages found.</p>}
      {result.passages.map((p) => (
        <div className="passage" key={p.id}>
          <strong>{p.document} — {p.section}</strong>
          <p className="privacy-note">Keyword score: {p.score}</p>
          <p>{p.text}</p>
        </div>
      ))}
      <p className="panel-footer">Inspect the source passages separately from the answer; citations alone do not prove accuracy.</p>
    </article>
  );
}

export default function DocumentsPage() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([]);
  const [busy, setBusy] = useState(false);
  const canSubmit = question.trim() && Array.from(question.trim()).length <= 4000 && !busy;

  async function submit(event, retrieveOnly = false) {
    event.preventDefault();
    if (!canSubmit) return;
    const submitted = question.trim();
    setQuestion('');
    setBusy(true);
    try {
      const result = await askDocuments(submitted, retrieveOnly);
      setHistory((previous) => [{ ...result, question: submitted, retrieveOnly }, ...previous]);
    } catch (error) {
      setHistory((previous) => [{ question: submitted, retrieveOnly: false, status: 'error', error: error.message, passages: [], retrievalFailed: true }, ...previous]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="page-shell">
      <LabNav page="documents" />
      <header className="page-header">
        <h1>Ask the documents</h1>
        <p className="intro">Explore RAG using four fictional company documents. Compare the retrieved evidence with the model's answer.</p>
      </header>
      <form className="panel question-form" onSubmit={submit}>
        <label htmlFor="document-question">Your question</label>
        <textarea id="document-question" rows={3} value={question} maxLength={4000}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="What are the company's opening hours?" required />
        <details><summary>Example questions</summary>
          <ul className="example-questions">{EXAMPLES.map((example) => <li key={example}>
            <button type="button" disabled={busy} onClick={() => setQuestion(example)}>{example}</button>
          </li>)}</ul>
        </details>
        <div className="document-actions">
          <button disabled={!canSubmit} type="submit">Ask the documents</button>
          <button disabled={!canSubmit} type="button" onClick={(event) => submit(event, true)}>Retrieve passages only</button>
        </div>
        <p className="privacy-note">Use synthetic data only. Asking the documents may call OpenAI and incur API charges. Retrieval only is offline. Questions are independent; history stays on this page until refreshed.</p>
        <p role="status" className="privacy-note">{busy ? 'Processing question…' : ''}</p>
      </form>
      {history.map((result, index) => <Result key={history.length - index} result={result} />)}
    </main>
  );
}
