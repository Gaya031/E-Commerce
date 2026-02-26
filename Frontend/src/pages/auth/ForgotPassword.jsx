import { useState } from "react";
import { Link } from "react-router-dom";
import { forgotPassword } from "../../api/auth.api";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await forgotPassword(email);
      setMessage(res.data?.message || "Reset instructions generated.");
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Failed to generate reset token");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow p-6">
        <h1 className="text-xl font-bold mb-2">Forgot Password</h1>
        <p className="text-sm text-gray-500 mb-6">Enter your email to reset your password.</p>
        <form onSubmit={submit} className="space-y-4">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="name@example.com"
            className="w-full border rounded-lg px-3 py-2"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg disabled:bg-gray-400"
          >
            {loading ? "Generating..." : "Generate Reset Link"}
          </button>
        </form>
        {message && <p className="mt-4 text-sm text-gray-700">{message}</p>}
        <div className="mt-4 text-sm">
          <Link to="/reset-confirmation" className="text-blue-600 hover:underline">
            Go to Reset Confirmation
          </Link>
        </div>
      </div>
    </div>
  );
}
