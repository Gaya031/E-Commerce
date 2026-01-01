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
        <form onSubmit={submit}>
            <input placeholder='email' value={email} onChange={e => setEmail(e.target.value)} />
            <input placeholder='password' type="password" value={password} onChange={e => setPassword(e.target.value)} />
            <button type='submit'>Login</button>
        </form>
    )
}

export default Login