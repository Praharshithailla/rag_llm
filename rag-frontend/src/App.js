import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import "./App.css";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [devMode, setDevMode] = useState(false);

  return (
    <div className="app">
      {/*
        Sidebar receives:
          - sessionId      → to highlight the active chat
          - setSessionId   → to switch sessions
          - devMode        → so the toggle can read current state
          - setDevMode     → so the toggle can change it
       */}
      <Sidebar
        sessionId={sessionId}
        setSessionId={setSessionId}
        devMode={devMode}
        setDevMode={setDevMode}
      />

      <div className="main">
        <ChatWindow
          sessionId={sessionId}
          devMode={devMode}
        />
      </div>
    </div>
  );
}

export default App;