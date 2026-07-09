// App.js
import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am your Medical AI Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when a new message arrives
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Calls your Python api.py bridge
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.text }),
      });
      
      const data = await response.json();
      setMessages((prev) => [...prev, { sender: 'bot', text: data.response }]);
    } catch (error) {
      setMessages((prev) => [...prev, { sender: 'bot', text: "Sorry, the server is down. Is api.py running?" }]);
    }
    
    setIsLoading(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.chatBox}>
        
        {/* === THE NEW HEADER WITH SVG LOGO === */}
        <div style={styles.header}>
          <svg width="35" height="35" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ marginRight: '10px' }}>
            <path d="M12 2C6.477 2 2 6.03 2 11C2 13.79 3.447 16.29 5.803 17.89C5.553 19.34 4.54 21.05 4.463 21.18C4.331 21.39 4.35 21.66 4.511 21.84C4.672 22.02 4.939 22.07 5.155 21.96C6.732 21.17 8.093 19.96 8.948 19.46C9.92 19.81 10.942 20 12 20C17.523 20 22 15.97 22 11C22 6.03 17.523 2 12 2Z" fill="white"/>
            <path d="M13 7H11V10H8V12H11V15H13V12H16V10H13V7Z" fill="#0056b3"/>
          </svg>
          <h2 style={{ margin: 0 }}>Medical AI Assistant</h2>
        </div>
        {/* ================================== */}

        <div style={styles.messageArea}>
          {messages.map((msg, index) => (
            <div key={index} style={msg.sender === 'user' ? styles.userMessageWrapper : styles.botMessageWrapper}>
              <div style={msg.sender === 'user' ? styles.userBubble : styles.botBubble}>
                {msg.text}
              </div>
            </div>
          ))}
          {isLoading && (
            <div style={styles.botMessageWrapper}>
              <div style={styles.botBubble}>Typing...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} style={styles.inputArea}>
          <input
            style={styles.input}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your medical question..."
          />
          <button style={styles.button} type="submit" disabled={isLoading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

// === THIS IS WHERE THE HEADER STYLE WAS CHANGED ===
const styles = {
  container: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' },
  chatBox: { width: '450px', height: '650px', backgroundColor: 'white', borderRadius: '15px', boxShadow: '0 4px 15px rgba(0,0,0,0.1)', display: 'flex', flexDirection: 'column', overflow: 'hidden' },
  
  // Notice the display: 'flex', alignItems: 'center' added here so the logo and text sit perfectly inline!
  header: { backgroundColor: '#0056b3', color: 'white', padding: '15px', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0' },
  
  messageArea: { flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '10px', backgroundColor: '#fafafa' },
  userMessageWrapper: { display: 'flex', justifyContent: 'flex-end' },
  botMessageWrapper: { display: 'flex', justifyContent: 'flex-start' },
  userBubble: { backgroundColor: '#0084ff', color: 'white', padding: '10px 15px', borderRadius: '18px 18px 0px 18px', maxWidth: '75%', wordWrap: 'break-word', fontSize: '15px' },
  botBubble: { backgroundColor: '#e4e6eb', color: 'black', padding: '10px 15px', borderRadius: '18px 18px 18px 0px', maxWidth: '75%', wordWrap: 'break-word', fontSize: '15px' },
  inputArea: { display: 'flex', padding: '15px', borderTop: '1px solid #ddd', backgroundColor: 'white' },
  input: { flex: 1, padding: '12px', borderRadius: '20px', border: '1px solid #ccc', outline: 'none', fontSize: '15px' },
  button: { marginLeft: '10px', padding: '10px 20px', backgroundColor: '#0056b3', color: 'white', border: 'none', borderRadius: '20px', cursor: 'pointer', fontWeight: 'bold' }
};

export default App;