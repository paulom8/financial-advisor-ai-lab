import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import EvaluationPage from './EvaluationPage.jsx';
import './styles.css';

const Page = window.location.pathname.replace(/\/+$/, '') === '/evaluation' ? EvaluationPage : App;

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Page />
  </React.StrictMode>,
);
