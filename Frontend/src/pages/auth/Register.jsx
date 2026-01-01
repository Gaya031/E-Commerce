import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../../api/auth.api";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    password: "",
    role: "buyer",
  });

  const handleChange = e => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const submit = async e => {
    e.preventDefault();

    try {
      await register(form);
      alert("Registration successful. Please login.");
      navigate("/login");
    } catch (err) {
      console.error("Register failed:", err);
      alert(
        err?.response?.data?.detail || "Registration failed"
      );
    }
  };

  return (
    <form onSubmit={submit} style={{ padding: 20 }}>
      <h2>Register</h2>

      <input
        name="name"
        placeholder="Full Name"
        value={form.name}
        onChange={handleChange}
        required
      />

      <input
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
        required
      />

      <input
        name="phone"
        placeholder="Phone"
        value={form.phone}
        onChange={handleChange}
      />

      <input
        type="password"
        name="password"
        placeholder="Password"
        value={form.password}
        onChange={handleChange}
        required
      />

      <select
        name="role"
        value={form.role}
        onChange={handleChange}
      >
        <option value="buyer">Buyer</option>
        <option value="seller">Seller</option>
      </select>

      <button type="submit">Register</button>
    </form>
  );
}
