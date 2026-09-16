import React, { useState, useEffect } from 'react';
import ChapterCard from './components/ChapterCard';
import './index.css';

function App() {
  const [chapters, setChapters] = useState([]);
  const [apiKey, setApiKey] = useState(localStorage.getItem('antigravity_api_key') || '');

  const handleKeyChange = (e) => {
    const val = e.target.value;
    setApiKey(val);
    localStorage.setItem('antigravity_api_key', val);
  };

  useEffect(() => {
    // Fetch initial chapters list
    fetch('http://localhost:8000/api/chapters')
      .then(res => res.json())
      .then(data => setChapters(data))
      .catch(err => console.error("Failed to load chapters:", err));
  }, []);

  return (
    <div className="app-container">
      <header>
        <div>
          <h1>Antigravity Ebook Translator</h1>
          <p>Automated Pipeline for PDF to LaTeX Translation</p>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', alignItems: 'flex-end' }}>
          <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Antigravity API Key (for Cloud Deployment)</label>
          <input 
            type="password" 
            placeholder="Enter your API Key..." 
            value={apiKey} 
            onChange={handleKeyChange}
            style={{
              padding: '0.5rem',
              borderRadius: '0.5rem',
              border: '1px solid rgba(255,255,255,0.2)',
              background: 'rgba(255,255,255,0.05)',
              color: 'white',
              width: '300px'
            }}
          />
        </div>
      </header>
      
      <main className="chapters-grid">
        {chapters.map(chapter => (
          <ChapterCard key={chapter.id} chapter={chapter} apiKey={apiKey} />
        ))}
        {chapters.length === 0 && <p style={{textAlign: 'center', color: 'var(--text-muted)'}}>Loading chapters...</p>}
      </main>
    </div>
  );
}

export default App;
