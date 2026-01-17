import React, { useState, useEffect, useRef } from "react";
import api from "../../services/api";
import { toast } from "react-toastify";
import "../../styles/Chatbot.css";

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  /* Scroll to bottom */
  useEffect(() => {
    messagesEndRef.current?. scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  /* Load chat history */
  useEffect(() => {
    if (isOpen) loadHistory();
  }, [isOpen]);

  const loadHistory = async () => {
    try {
      const { data } = await api.get("/chatbot/history? limit=20");
      if (data.success) {
        const history = data.history. reverse().flatMap(h => ([
          { sender: "user", text: h.message },
          { sender: "bot", text: h.response }
        ]));
        setMessages(history);
      }
    } catch{
      console.warn("No chat history available");
    }
  };

  /* Send text message */
  const handleSendMessage = async () => {
    if (! inputMessage.trim()) return;

    const text = inputMessage;
    setMessages(prev => [...prev, { sender: "user", text }]);
    setInputMessage("");
    setLoading(true);

    try {
      console.log("📤 Sending message:", text);

      const response = await api.post("/chatbot/message", { message: text });

      console.log("📥 Received response:", response.data);

      if (response.data.success) {
        setMessages(prev => [...prev, { sender: "bot", text: response. data.response }]);
      } else {
        toast.error(response.data.error || "Failed to get response");
      }
    } catch (error) {
      console.error("Chatbot error:", error);
      console.error("Error response:", error.response?.data);
      toast.error(error.response?.data?.error || "Failed to get response");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Toggle Button */}
      <button
        className={`chatbot-toggle ${isOpen ? "active" : ""}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        {isOpen ? "✕" : "💬"}
      </button>

      {/* Chatbot Window */}
      {isOpen && (
        <div className="chatbot-window">
          {/* Header */}
          <div className="chatbot-header">
            <div className="header-content">
              <h3>🤖 RideWise Assistant</h3>
              <p>Ask me about bike rentals</p>
            </div>
            <button
              className="close-btn-chat"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          {/* Messages Area */}
          <div className="chatbot-messages">
            {messages.length === 0 && (
              <div className="chatbot-welcome">
                <div className="welcome-icon">👋</div>
                <p className="welcome-title">Hello! I'm your AI assistant</p>
                <p className="welcome-subtitle">Try asking me about: </p>
                <ul className="welcome-list">
                  <li>
                    <span className="list-icon">🌤️</span>
                    <span>Weather impact on rentals</span>
                  </li>
                  <li>
                    <span className="list-icon">⏰</span>
                    <span>Peak rental hours</span>
                  </li>
                  <li>
                    <span className="list-icon">📊</span>
                    <span>How to make predictions</span>
                  </li>
                  <li>
                    <span className="list-icon">📍</span>
                    <span>Finding bike stations</span>
                  </li>
                </ul>
              </div>
            )}

            {messages.map((m, i) => (
              <div key={i} className={`message ${m.sender}`}>
                {m.sender === "bot" && <div className="message-avatar">🤖</div>}
                <div className="message-content" style={{ whiteSpace: 'pre-line' }}>{m.text}</div>
                {m.sender === "user" && <div className="message-avatar user-avatar">👤</div>}
              </div>
            ))}

            {loading && (
              <div className="message bot">
                <div className="message-avatar">🤖</div>
                <div className="message-content typing">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="chatbot-input">
            <input
              value={inputMessage}
              onChange={e => setInputMessage(e. target.value)}
              onKeyDown={e => e.key === "Enter" && ! loading && handleSendMessage()}
              placeholder="Type your message..."
              disabled={loading}
              className="chat-input-field"
            />

            {/* Send Button */}
            <button
              className="send-btn"
              onClick={handleSendMessage}
              disabled={loading || !inputMessage.trim()}
              title="Send message"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;