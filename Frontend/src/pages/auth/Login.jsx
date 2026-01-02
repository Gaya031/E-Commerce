import React from 'react'
import { useState } from 'react';
import { login, getMe } from '../../api/auth.api';
import { useAuthStore } from '../../store/auth.store';
import { Navigate, useNavigate } from 'react-router-dom';
const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const setAuth = useAuthStore(state => state.setAuth);

    // console.log(email)
    // console.log(password)
    const submit = async e => {
        e.preventDefault();
        try {
            const res = await login({ email, password });
            const { access_token } = res.data;
            setAuth(null, access_token);
            
            const me = await getMe();
            console.log("Login Success: ", me.data);
            
            setAuth(me.data, access_token);
            navigate("/");
        } catch (err) {
            console.log("Login Failed: ", err);
            alert("Invalid credentials");
        }
    };
    return (
    <div className="min-h-screen bg-slate-50">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
        <div className="flex items-center gap-2 text-lg font-semibold">
          🛍️ Sahu Mart
        </div>

        <div className="flex items-center gap-6 text-sm">
          <a className="text-gray-600 hover:text-black" href="#">Home</a>
          <a className="text-gray-600 hover:text-black" href="#">About Us</a>
          <a className="text-gray-600 hover:text-black" href="#">Contact Support</a>
          <button className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700">
            Register
          </button>
        </div>
      </nav>

      {/* Main Card */}
      <div className="flex items-center justify-center px-4 py-16">
        <div className="flex w-full max-w-5xl overflow-hidden bg-white shadow-xl rounded-2xl">
          
          {/* Left Section */}
          <div className="w-full p-10 lg:w-1/2">
            <h1 className="text-2xl font-bold text-gray-900">Welcome Back</h1>
            <p className="mt-2 text-sm text-gray-500">
              Log in to access your dashboard, track orders, or manage your store.
            </p>

            {/* Role Tabs */}
            <div className="flex gap-2 p-1 mt-6 bg-gray-100 rounded-lg w-fit ml-24">
              <button className="px-4 py-1 text-sm font-medium bg-white rounded-md shadow">
                Buyer
              </button>
              <button className="px-4 py-1 text-sm text-gray-600">
                Seller
              </button>
              <button className="px-4 py-1 text-sm text-gray-600">
                Partner
              </button>
            </div>

            {/* OAuth */}
            <div className="flex gap-3 mt-6">
              <button className="flex items-center justify-center w-1/2 gap-2 py-2 border rounded-lg hover:bg-gray-50">
                🌐 Google
              </button>
              <button className="flex items-center justify-center w-1/2 gap-2 py-2 border rounded-lg hover:bg-gray-50">
                📱 Phone
              </button>
            </div>

            <div className="my-6 text-xs text-center text-gray-400">
              OR LOGIN WITH EMAIL
            </div>

            {/* Form */}
            <form className="space-y-4" onSubmit={submit}>
              <div>
                <label className="block mb-1 text-sm text-gray-600">
                  Email or Username
                </label>
                <input
                  type="email"
                  placeholder="name@sahumart.com"
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onChange={e => setEmail(e.target.value)}
                />
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <label className="text-sm text-gray-600">Password</label>
                  <a href="#" className="text-sm text-blue-600 hover:underline">
                    Forgot Password?
                  </a>
                </div>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onChange={e => setPassword(e.target.value)}
                />
              </div>

              <button type='submit' className="w-full py-3 mt-2 font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">
                Sign In →
              </button>
            </form>

            <p className="mt-6 text-sm text-center text-gray-500">
              Don’t have an account?{" "}
              <a href="#" className="text-blue-600 hover:underline">
                Register
              </a>
            </p>
          </div>

          {/* Right Section */}
          <div className="relative hidden w-1/2 lg:block">
            <img
              src="https://images.unsplash.com/photo-1600180758890-6b94519a8ba6"
              alt="delivery"
              className="object-cover w-full h-full"
            />
            <div className="absolute inset-0 bg-gradient-to-tr from-blue-900/80 to-blue-600/60" />

            <div className="absolute inset-0 flex flex-col justify-end p-10 text-white">
              <span className="inline-flex items-center gap-2 px-3 py-1 mb-3 text-xs bg-white/20 rounded-full w-fit">
                🚚 QUICK COMMERCE
              </span>
              <h2 className="text-3xl font-bold leading-tight">
                Fastest Delivery<br />in Your Town
              </h2>
              <p className="mt-3 text-sm text-white/90">
                Join thousands of local sellers and happy customers connecting
                through Sahu Mart every day.
              </p>

              <div className="flex items-center gap-3 mt-4 text-sm">
                <span>👥 2k+</span>
                <span>⭐⭐⭐⭐⭐</span>
                <span className="opacity-90">Trusted by local vendors</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default Login