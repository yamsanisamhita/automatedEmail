import React, { useState } from "react";

function App() {
  const [prompt, setPrompt] = useState("");
  const [recipient, setRecipient] = useState("");
  const [status, setStatus] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("⏳ Sending...");

    try {
      const response = await fetch("http://localhost:5000/send-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt, email: recipient }),
      });

      const result = await response.json();
      if (response.ok) {
        setStatus("✅ " + result.message);
      } else {
        setStatus("❌ " + result.error);
      }
    } catch (error) {
      setStatus("❌ Failed to connect to backend.");
    }
  };

  return (
    <div style={styles.background}>
      <div style={styles.card}>
        <h1 style={styles.heading}>✨ AI Email Generator</h1>
        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>💡 Email Purpose</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            required
            rows={4}
            placeholder="Enter purpose of the email..."
            style={styles.textarea}
          />

          <label style={styles.label}>📬 Recipient Email</label>
          <input
            type="email"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
            placeholder="example@example.com"
            style={styles.input}
          />

          <button type="submit" style={styles.button}>
            🚀 Generate & Send
          </button>
        </form>
        {status && <p style={styles.status}>{status}</p>}
      </div>
    </div>
  );
}

const styles = {
  background: {
    height: "100vh",
    width: "100vw",
    background: "linear-gradient(to right, #6a11cb, #2575fc)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  card: {
    backgroundColor: "white",
    padding: "2.5rem",
    borderRadius: "16px",
    width: "90%",
    maxWidth: "500px",
    boxShadow: "0 20px 50px rgba(0,0,0,0.3)",
    fontFamily: "'Segoe UI', sans-serif",
  },
  heading: {
    marginBottom: "1.5rem",
    textAlign: "center",
    fontSize: "1.8rem",
    color: "#6a11cb",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1.2rem",
  },
  label: {
    fontWeight: "600",
    color: "#333",
  },
  input: {
    padding: "0.8rem",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontSize: "1rem",
    outline: "none",
  },
  textarea: {
    padding: "0.8rem",
    borderRadius: "8px",
    border: "1px solid #ccc",
    fontSize: "1rem",
    resize: "vertical",
    outline: "none",
  },
  button: {
    background: "linear-gradient(to right, #a18cd1, #fbc2eb)",
    color: "white",
    fontWeight: "bold",
    padding: "0.8rem",
    border: "none",
    borderRadius: "10px",
    fontSize: "1rem",
    cursor: "pointer",
    transition: "0.3s ease-in-out",
  },
  status: {
    marginTop: "1.2rem",
    textAlign: "center",
    color: "#222",
    fontWeight: "500",
  },
};

export default App;
