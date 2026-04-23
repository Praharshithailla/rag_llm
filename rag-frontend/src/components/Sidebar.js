import React, { useEffect, useState } from "react";
import { getSessions, createSession } from "../services/api";

function Sidebar({ sessionId, setSessionId, devMode, setDevMode }) {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    loadSessions();
  }, []);

  // Refresh list whenever session changes (e.g. title updated after first message)
  useEffect(() => {
    if (sessionId) loadSessions();
  }, [sessionId]);

  const loadSessions = async () => {
    try {
      const res = await getSessions();
      setSessions(res.data.sessions || []);
    } catch (err) {
      console.error("Error loading sessions:", err);
      setSessions([]);
    }
  };

  const handleNewChat = async () => {
    try {
      const res = await createSession();
      setSessionId(res.data.session_id);
      await loadSessions();
    } catch (err) {
      console.error("Error creating session:", err);
    }
  };

  const getTitle = (s) => {
    if (s.title && s.title !== "New Chat") return s.title;
    return `Chat #${s.id}`;
  };

  return (
    <div className="sidebar">

      {/* ── Header: logo + new chat button ── */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">R</div>
          <span className="sidebar-logo-text">RAG Studio</span>
        </div>
        <button className="new-chat-btn" onClick={handleNewChat}>
          New Conversation
        </button>
      </div>

      {/* ── Session history list ── */}
      <div className="sidebar-sessions-label">History</div>

      <div className="sidebar-sessions">
        {sessions.length === 0 && (
          <div style={{
            padding: "16px 12px",
            fontSize: "12px",
            color: "var(--text-muted)",
            textAlign: "center"
          }}>
            No conversations yet
          </div>
        )}

        {sessions.map((s) => (
          <div
            key={s.id}
            onClick={() => setSessionId(s.id)}
            className={`session ${sessionId === s.id ? "active" : ""}`}
            title={getTitle(s)}
          >
            {getTitle(s)}
          </div>
        ))}
      </div>

      {/* ── Footer: Dev Mode toggle — ALWAYS VISIBLE ── */}
      <div className="sidebar-footer">
        <label
          className={`toggle-wrapper ${devMode ? "active" : ""}`}
          title="Toggle developer panel to see chunks and retrieval scores"
        >
          <input
            type="checkbox"
            className="toggle-checkbox"
            checked={devMode}
            onChange={() => setDevMode(!devMode)}
          />
          <div className={`toggle-track ${devMode ? "on" : ""}`}>
            <div className="toggle-thumb" />
          </div>
          <div className="toggle-text">
            <span className="toggle-label">Dev Mode</span>
            <span className="toggle-sublabel">
              {devMode ? "panel visible ↓" : "shows retrieval data"}
            </span>
          </div>
        </label>
      </div>

    </div>
  );
}

export default Sidebar;