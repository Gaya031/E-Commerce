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

  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const handleChange = e => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const submit = async e => {
    e.preventDefault();
    setError("");

    if (form.password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      await register(form);
      navigate("/login");
    } catch (err) {
      setError(
        err?.response?.data?.detail || "Registration failed"
      );
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="flex min-h-screen">
        {/* LEFT */}
        <div className="w-full px-8 py-10 bg-white lg:w-1/2">
          <div className="flex items-center gap-2 mb-8 text-lg font-semibold">
            📄 Sahu Mart
          </div>

          <h1 className="text-3xl font-bold text-gray-900">
            Create an account
          </h1>
          <p className="mt-2 text-sm text-gray-500">
            Connect with the best local sellers near you.
          </p>

          {/* Role Tabs */}
          <div className="flex gap-2 p-1 mt-6 ml-32 bg-blue-50 rounded-full w-fit">
            {["buyer", "seller", "partner"].map(r => (
              <button
                key={r}
                type="button"
                onClick={() => setForm({ ...form, role: r })}
                className={`px-6 py-2 text-sm rounded-full ${
                  form.role === r
                    ? "bg-blue-600 text-white"
                    : "text-blue-600"
                }`}
              >
                {r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>

          {/* FORM */}
          <form className="mt-8 space-y-5" onSubmit={submit}>
            <Input label="Full Name" name="name" value={form.name} onChange={handleChange}  />
            <Input label="Email Address" name="email" value={form.email} onChange={handleChange} />
            <Input label="Phone Number" name="phone" value={form.phone} onChange={handleChange} />

            <Input
              label="Password"
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
            />

            <div>
              <label className="block mb-1 text-sm text-gray-600">
                Confirm Password
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
                className={`w-full px-4 py-3 border rounded-full focus:outline-none focus:ring-2 ${
                  error ? "border-red-500 focus:ring-red-500" : "focus:ring-blue-500"
                }`}
              />
              {error && (
                <p className="mt-1 text-sm text-red-500">
                  {error}
                </p>
              )}
            </div>

            <button className="w-full py-3 text-white bg-blue-600 rounded-full hover:bg-blue-700">
              Create Account
            </button>
          </form>

          <p className="mt-6 text-sm text-center text-gray-500">
            Already have an account?{" "}
            <a href="/login" className="text-blue-600 hover:underline">
              Log in
            </a>
          </p>
        </div>

        {/* RIGHT (UNCHANGED) */}
        <div className="relative hidden w-1/2 lg:block">
          <img
            src="https://images.unsplash.com/photo-1603575448360-153f093fd0a9"
            alt="delivery"
            className="object-cover w-full h-full"
          />
          <div className="absolute inset-0 bg-black/40" />
        </div>
      </div>
    </div>
  );
}

/* Reusable input – UI unchanged */
function Input({ label, ...props }) {
  return (
    <div>
      <label className="block mb-1 text-sm text-gray-600">{label}</label>
      <input
        {...props}
        required
        className="w-full px-4 py-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
  );
}
