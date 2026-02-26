import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { resetPassword } from "../../api/auth.api";

export default function ResetConfirmation() {
  const [searchParams] = useSearchParams();
  const [token, setToken] = useState(searchParams.get("token") || "");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await resetPassword(token, password);
      setMessage(res.data?.message || "Password reset successful");
      setTimeout(() => navigate("/login"), 800);
    } catch (err) {
      setMessage(err?.response?.data?.detail || "Reset failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow p-6">
        <h1 className="text-xl font-bold mb-2">Reset Password</h1>
        <p className="text-sm text-gray-500 mb-6">Paste token and set a new password.</p>
        <form onSubmit={submit} className="space-y-4">
          <textarea
            value={token}
            onChange={(e) => setToken(e.target.value)}
            placeholder="Reset token"
            className="w-full border rounded-lg px-3 py-2 min-h-[90px]"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="New password"
            className="w-full border rounded-lg px-3 py-2"
            minLength={8}
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-2 rounded-lg disabled:bg-gray-400"
          >
            {loading ? "Submitting..." : "Reset Password"}
          </button>
        </form>
        {message && <p className="mt-4 text-sm">{message}</p>}
      </div>
    </div>
  );
}
