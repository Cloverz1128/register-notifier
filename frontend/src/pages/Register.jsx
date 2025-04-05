import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    });

    if (res.ok) {
      alert("Registered successfully. You can now log in.");
      navigate("/login");
    } else {
      const msg = await res.json();
      alert("Register failed: " + msg.error);
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
        <br />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
        <br />
        <button type="submit">Register</button>
      </form>
      <p><a href="/login">Already have an account?</a></p>
    </div>
  );
}

export default Register;
