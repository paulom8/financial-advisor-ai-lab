import { useEffect, useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export default function App() {
  const [records, setRecords] = useState([]);
  const [status, setStatus] = useState('loading');

  useEffect(() => {
    const controller = new AbortController();
    fetch(`${API_URL}/api/test-records`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Request failed (${response.status})`);
        return response.json();
      })
      .then((data) => {
        setRecords(data);
        setStatus('ready');
      })
      .catch((error) => {
        if (error.name !== 'AbortError') setStatus('error');
      });
    return () => controller.abort();
  }, []);

  return (
    <main className="page-shell">
      <header className="page-header">
        <div className="eyebrow"><span className="status-dot" /> LEARNING LAB</div>
        <h1>Database records</h1>
        <p className="intro">A small first step: reading saved records through the API.</p>
      </header>

      <section className="panel" aria-labelledby="records-heading">
        <div className="panel-heading">
          <div>
            <p className="eyebrow muted">SAMPLE DATA</p>
            <h2 id="records-heading">Test table</h2>
          </div>
          {status === 'ready' && <span className="record-count">{records.length} {records.length === 1 ? 'record' : 'records'}</span>}
        </div>

        {status === 'loading' && <p className="message">Loading records…</p>}
        {status === 'error' && <p className="message error">Could not connect to the API. Start the backend and refresh this page.</p>}
        {status === 'ready' && records.length === 0 && <p className="message">There are no records yet.</p>}
        {status === 'ready' && records.length > 0 && (
          <div className="table-wrap">
            <table>
              <thead><tr><th>ID</th><th>Description</th><th>Date inserted</th></tr></thead>
              <tbody>{records.map((record) => (
                <tr key={record.id}>
                  <td className="id-cell">{record.id}</td>
                  <td>{record.description}</td>
                  <td className="date-cell">{new Date(record.date_inserted).toLocaleString()}</td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        )}
        <div className="panel-footer">Records are sample data for this educational prototype.</div>
      </section>
    </main>
  );
}
