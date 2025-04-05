import React, { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";

function Welcome() {
  const [email, setEmail] = useState("");
  const [messages, setMessages] = useState([]);
  const [unauthorized, setUnauthorized] = useState(false);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/sse");

    // get current user email
    fetch("http://localhost:8000/api/welcome", {
      credentials: "include",
    })
      .then((res) => {
        if (res.status === 401) {
          setUnauthorized(true);
          setLoading(false);
          eventSource.close(); // close event stream
          return null;
        }
        return res.json();
      })
      .then((data) => {
        if (data && data.email) setEmail(data.email);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setUnauthorized(true);
        setLoading(false);
        eventSource.close();
      });

    // get event stream
    eventSource.addEventListener("register", (e) => {
      setMessages((prev) => [...prev, { type: "register", text: e.data }]);
    });

    eventSource.onerror = () => {
      console.error("SSE error");
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [navigate]);

  const handleLogout = async () => {
    await fetch("http://localhost:8000/api/logout", {
      method: "POST",
      credentials: "include",
    });
    navigate("/");
  };

  // unauthorized
  if (unauthorized && !loading) {
    return (
      <div style={{ padding: "2rem", fontFamily: "sans-serif", color: "#b00" }}>
        <h2> Login Required </h2>
        <p>You need to log in to access this page.
          <Link to="/login">Login</Link>.
        </p>
        <p>
          Don’t have an account?{" "}
          <Link to="/register">Register one</Link>.
        </p>
      </div>
    );
  }

  if (loading) {
    return <p style={{ padding: "2rem" }}>Loading...</p>;
  }

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "1rem",
        }}
      >
        <div>
          Welcome <strong>{email}</strong>{" "}
          <button onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <div>
        <h3>Notifications</h3>
        <div
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "1rem",
            maxHeight: "300px",
            overflowY: "auto",
            background: "#f9f9f9",
          }}
        >
          {messages.length === 0 && <p>No messages yet.</p>}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                marginBottom: "0.5rem",
                color: msg.type === "register" ? "green" : "blue",
              }}
            >
              [{msg.type}] {msg.text}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Welcome;
