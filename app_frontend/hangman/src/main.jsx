// Import potřebných React knihoven
import React from 'react';
// Import funkce pro renderování do DOM
import ReactDOM from 'react-dom/client';
// Import hlavní aplikační komponenty
import App from './App';
// Import globálních stylů
import '../../../assets/styles/style.css';

// Vytvoření kořenového elementu a renderování aplikace
// StrictMode aktivuje dodatečné kontroly a varování během vývoje
ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
