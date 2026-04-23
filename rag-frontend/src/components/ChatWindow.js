import React, { useEffect, useRef, useState } from "react";
import { sendMessage, getMessages } from "../services/api";
import MessageBubble from "./MessageBubble";
import DevPanel from "./DevPanel";

function ChatWindow({ sessionId, devMode }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [devData, setDevData] = useState(null);
  const [sessionTitle, setSessionTitle] = useState("");

  const bottomRef = useRef(null);
  const messagesRef = useRef(null);

  // ── Load messages when session changes ──────────────────
  useEffect(() => {
    if (!sessionId) {
      setMessages([]);
      setSessionTitle("");
      setDevData(null);
      return;
    }

    const load = async () => {
      try {
        const res = await getMessages(sessionId);
        const raw = res.data.messages || [];

        const transformed = [];
        raw.forEach((m) => {
          if (m.user) transformed.push({ role: "user", content: m.user });
          if (m.bot) transformed.push({ role: "assistant", content: m.bot });
        });

        setMessages(transformed);
        if (res.data.title) setSessionTitle(res.data.title);

      } catch (err) {
        console.error("Error loading messages:", err);
        setMessages([]);
      }
    };

    load();

    // 🔥 FIX: session change appudu scroll TOP ki control
    if (messagesRef.current) {
      messagesRef.current.scrollTo({
        top: 0,
        behavior: "auto",
      });
    }

  }, [sessionId]);

  // ── Auto-scroll to bottom (only when messages exist) ──
  useEffect(() => {
    if (messages.length > 0) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, loading]);

  // ── Stream text into last assistant bubble ─────────────
  const streamText = async (text) => {
    let temp = "";
    for (let char of text) {
      temp += char;
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: temp,
        };
        return updated;
      });
      await new Promise((res) => setTimeout(res, 10));
    }
  };

  // ── Send message ───────────────────────────────────────
  const handleSend = async () => {
    if (!input.trim() || loading || !sessionId) return;

    const currentInput = input.trim();
    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", content: currentInput },
      { role: "assistant", content: "" },
    ]);

    setLoading(true);

    try {
      const res = await sendMessage({
        query: currentInput,
        session_id: sessionId,
      });

      setDevData(res.data);
      await streamText(res.data.answer || "No response");

      if (res.data.session_title) {
        setSessionTitle(res.data.session_title);
      }

    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          role: "assistant",
          content: "⚠️ Error fetching response. Is backend running?",
        };
        return updated;
      });
    }

    setLoading(false);
  };

  const isEmpty = messages.length === 0 && !loading;

  return (
    <div className="chat-window">

      {/* Header */}
      <div className="chat-header">
        <div className="chat-title">
          <div className="chat-title-dot" />
          {sessionId
            ? (sessionTitle && sessionTitle !== "New Chat"
                ? sessionTitle
                : `Session #${sessionId}`)
            : "RAG Studio"}
        </div>
      </div>

      {/* Messages */}
      {!sessionId ? (
        <div className="no-session">
          <div className="no-session-icon">◈</div>
          <div className="no-session-text">
            Create or select a chat<br />from the sidebar
          </div>
        </div>
      ) : (
        <div className="messages" ref={messagesRef}>
          
          {isEmpty && (
            <div className="messages-empty">
              <div className="messages-empty-icon">◈</div>
              <div className="messages-empty-text">
                Ask anything about your documents
              </div>
            </div>
          )}

          {messages.map((m, i) => (
            <MessageBubble key={i} msg={m} />
          ))}

          {loading && (
            <div className="bubble-wrapper assistant">
              <div className="bubble-avatar ai-avatar">AI</div>
              <div className="loader">
                <div className="loader-dots">
                  <div className="loader-dot" />
                  <div className="loader-dot" />
                  <div className="loader-dot" />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      )}

      {/* Input */}
      <div className="input-area">
        <div className="input-box">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              sessionId
                ? "Ask something about your documents..."
                : "Select a session first..."
            }
            onKeyDown={(e) =>
              e.key === "Enter" && !e.shiftKey && handleSend()
            }
            disabled={!sessionId || loading}
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={!input.trim() || !sessionId || loading}
          >
            ↑
          </button>
        </div>
      </div>

      {/* Dev Panel */}
      {devMode && <DevPanel data={devData} />}

    </div>
  );
}

export default ChatWindow;