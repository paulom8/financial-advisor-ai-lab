import React, { useState } from 'react';
import { runEvaluation } from './api.js';
import LabNav from './LabNav.jsx';

const STATUS_LABELS = { passed: 'Passed', failed: 'Failed', error: 'Error' };

function toolUse(used) {
  return used ? 'Used' : 'Not used';
}

function CaseResult({ result }) {
  const hasAnswer = result.status !== 'error';
  const toolMatched = result.database_function_used === result.expected_database_function_used;

  return (
    <article className="panel" aria-labelledby={`case-${result.id}`}>
      <div className="case-heading">
        <h2 id={`case-${result.id}`}>{result.title}</h2>
        <span className={`case-status ${result.status}`}>{STATUS_LABELS[result.status]}</span>
      </div>
      <p className="answer-question">{result.question}</p>
      <dl className="case-answers">
        <div>
          <dt>Expected answer</dt>
          <dd>{result.expected_answer}</dd>
        </div>
        <div>
          <dt>Model answer</dt>
          <dd className="answer-text">{hasAnswer ? result.answer : 'Unavailable'}</dd>
        </div>
      </dl>
      {hasAnswer ? (
        <ul className="case-checks">
          <li>
            <strong>{toolMatched ? 'Pass' : 'Fail'}</strong> · Database function
            {' — '}expected {toolUse(result.expected_database_function_used).toLowerCase()},
            {' '}observed {toolUse(result.database_function_used).toLowerCase()}.
          </li>
          <li><strong>{result.answer_matched ? 'Pass' : 'Fail'}</strong> · Answer check</li>
        </ul>
      ) : (
        <p className="error">{result.error}</p>
      )}
    </article>
  );
}

export default function EvaluationPage() {
  const [run, setRun] = useState({ status: 'idle' });
  const running = run.status === 'running';
  const report = run.report;

  async function handleRun() {
    if (running) return;
    setRun({ status: 'running' });
    try {
      setRun({ status: 'complete', report: await runEvaluation() });
    } catch (error) {
      setRun({ status: 'error', message: error.message });
    }
  }

  return (
    <main className="page-shell">
      <LabNav page="evaluation" />
      <header className="page-header">
        <h1>Evaluate the model</h1>
        <p className="intro">See whether the model uses the database when expected and gives the expected answer.</p>
      </header>

      <section className="panel evaluation-controls" aria-label="Evaluation controls">
        <p>Each run checks the largest saved target, an absent demo client, and a general compound interest question. The answer checks use the formats requested in each question.</p>
        <button type="button" onClick={handleRun} disabled={running}>
          {running ? 'Running evaluation…' : 'Run evaluation'}
        </button>
        <p className="privacy-note">Running sends three fictional questions to OpenAI and may incur API charges.</p>
        <div role="status">
          {running && <p>Waiting for the model to answer all three questions.</p>}
          {report && (
            <p>
              <strong>{report.cases.filter((result) => result.status === 'passed').length} of {report.cases.length} passed</strong>
              {' · '}{report.model}
            </p>
          )}
        </div>
        {run.status === 'error' && <p className="error" role="alert">{run.message}</p>}
      </section>

      {report?.cases.map((result) => <CaseResult key={result.id} result={result} />)}
    </main>
  );
}
