import React from 'react';

export default function LabNav({ page }) {
  return (
    <nav className="lab-nav" aria-label="Learning pages">
      <a href="/" aria-current={page === 'ask' ? 'page' : undefined}>Ask the model</a>
      <a href="/evaluation" aria-current={page === 'evaluation' ? 'page' : undefined}>Evaluate the model</a>
    </nav>
  );
}
