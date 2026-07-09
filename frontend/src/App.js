import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am your Medical AI Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

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
        <div style={styles.header}>
          <h2>🏥 Medical AI Assistant</h2>
        </div>
        
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

// Built-in CSS so you don't have to mess with external files tonight
const styles = {
  container: { display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#f0f2f5' },
  chatBox: { width: '450px', height: '650px', backgroundColor: 'white', borderRadius: '15px', boxShadow: '0 4px 15px rgba(0,0,0,0.1)', display: 'flex', flexDirection: 'column', overflow: 'hidden' },
  header: { backgroundColor: '#0056b3', color: 'white', padding: '15px', textAlign: 'center', margin: '0' },
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