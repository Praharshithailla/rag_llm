import React from "react";

function MessageBubble({ msg }) {
  const isUser = msg.role === "user";

  return (
    <div className={`bubble-wrapper ${isUser ? "user" : "assistant"}`}>
      <div className={`bubble-avatar ${isUser ? "user-avatar" : "ai-avatar"}`}>
        {isUser ? "U" : "AI"}
      </div>
      <div className={`bubble ${msg.role}`}>
        {msg.content}
      </div>
    </div>
  );
}

export default MessageBubble;