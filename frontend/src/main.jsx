import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import EvaluationPage from './EvaluationPage.jsx';
import DocumentsPage from './DocumentsPage.jsx';
import './styles.css';

const path = window.location.pathname.replace(/\/+$/, '');
const Page = path === '/documents' ? DocumentsPage : path === '/evaluation' ? EvaluationPage : App;

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Page />
  </React.StrictMode>,
);
