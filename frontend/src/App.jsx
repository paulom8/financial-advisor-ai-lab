import { useState } from 'react';
import { askQuestion } from './api.js';

const MAX_QUESTION_LENGTH = 4_000;

export default function App() {
  const [question, setQuestion] = useState('');
  const [submission, setSubmission] = useState({ status: 'idle' });
  const trimmedQuestion = question.trim();
  const isTooLong = Array.from(trimmedQuestion).length > MAX_QUESTION_LENGTH;
  const isSubmitting = submission.status === 'loading';
  const canSubmit = Boolean(trimmedQuestion) && !isTooLong && !isSubmitting;

  async function handleSubmit(event) {
    event.preventDefault();
    if (!canSubmit) return;
    setSubmission({ status: 'loading' });
    try {
      const result = await askQuestion(trimmedQuestion);
      setSubmission({ status: 'answered', question: trimmedQuestion, ...result });
    } catch (error) {
      setSubmission({ status: 'error', message: error.message });
    }
  }

  return (
    <main className="page-shell">
      <header className="page-header">
        <h1>Ask the model</h1>
        <p className="intro">Your question will be sent to OpenAI. Use a fictional example.</p>
      </header>

      <form className="panel question-form" onSubmit={handleSubmit}>
        <label htmlFor="question">Your question</label>
        <textarea
          id="question"
          aria-describedby={isTooLong ? 'privacy-note length-error' : 'privacy-note'}
          aria-invalid={isTooLong}
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Explain compound interest using a fictional example."
          rows={5}
          required
        />
        <p className="privacy-note" id="privacy-note">
          Use synthetic data only. Do not enter real personal or client financial information.
        </p>
        {isTooLong && (
          <p className="error" id="length-error" role="alert">
            Shorten your question to {MAX_QUESTION_LENGTH.toLocaleString()} characters or fewer.
          </p>
        )}
        <button type="submit" disabled={!canSubmit}>
          {isSubmitting ? 'Waiting for answer…' : 'Submit question'}
        </button>
        <span className="visually-hidden" role="status">
          {isSubmitting && 'Waiting for OpenAI…'}
          {submission.status === 'answered' && 'Answer received.'}
        </span>
        {submission.status === 'error' && <p className="error" role="alert">{submission.message}</p>}
      </form>

      {submission.status === 'answered' && (
        <section className="panel" aria-labelledby="answer-heading">
          <h2 id="answer-heading">Answer</h2>
          <p className="answer-question">{submission.question}</p>
          <p className={`function-status ${submission.databaseFunctionUsed ? 'used' : 'not-used'}`}>
            Database function {submission.databaseFunctionUsed ? 'used' : 'not used'}
          </p>
          <p className="answer-text">{submission.answer}</p>
          <p className="panel-footer">AI-generated answer for educational use. Review it before relying on it.</p>
        </section>
      )}
    </main>
  );
}
