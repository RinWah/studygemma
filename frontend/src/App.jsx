import React, { useState } from 'react';
import './App.css';

export default function App() {
  const [notes, setNotes] = useState('');
  const [mode, setMode] = useState('explain');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [showResponse, setShowResponse] = useState(false);

  const modes = [
    { id: 'explain', label: '✨ Explain', icon: 'ti ti-bulb' },
    { id: 'quiz me', label: '🧠 Quiz Me', icon: 'ti ti-brain' },
    { id: 'notebook notes', label: '📝 Notes', icon: 'ti ti-notes' },
    { id: 'practice problems', label: '⚙️ Practice', icon: 'ti ti-code' },
    { id: 'interview mode', label: '🎯 Interview', icon: 'ti ti-target' },
  ];

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!notes.trim()) return;

    setLoading(true);
    setShowResponse(false);

    try {
      const res = await fetch('http://127.0.0.1:8000/study', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes, mode }),
      });

      const data = await res.json();
      setResponse(data.response || 'No response received');
      setShowResponse(true);
    } catch (err) {
      setResponse(`Error: ${err.message}`);
      setShowResponse(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1 className="title">StudyGemma</h1>
        <p className="subtitle">Transform messy notes into clear explanations</p>
      </div>

      <div className="main-card">
        <form onSubmit={handleAnalyze}>
          <div className="form-group">
            <label className="label">Your notes</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Paste lecture notes, code, homework prompts, or textbook excerpts..."
              className="textarea"
            />
          </div>

          <div className="form-group">
            <label className="label">What do you need?</label>
            <div className="modes-grid">
              {modes.map((m) => (
                <button
                  key={m.id}
                  type="button"
                  onClick={() => setMode(m.id)}
                  className={`mode-button ${mode === m.id ? 'active' : ''}`}
                  title={m.label}
                >
                  <span className="mode-label">{m.label}</span>
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={!notes.trim() || loading}
            className="submit-button"
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Learning...
              </>
            ) : (
              <>
                <i className="ti ti-sparkles"></i>
                Study with Gemma
              </>
            )}
          </button>
        </form>
      </div>

      {showResponse && (
        <div className="response-container">
          <div className="response-header">
            <h2>Your result</h2>
            <button
              className="close-button"
              onClick={() => setShowResponse(false)}
              aria-label="Close response"
            >
              <i className="ti ti-x"></i>
            </button>
          </div>
          <div className="response-text">
            {response.split('\n').map((line, i) => (
              <p key={i}>{line || <br />}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}