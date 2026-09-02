// src/pages/Login.jsx

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser } from "../services/accountsServices";
import "../styles/auth.css";

export default function Login() {

const navigate = useNavigate();

const [form,setForm] = useState({
username:"",
password:""
});

const [loading,setLoading] = useState(false);
const [errorMsg,setErrorMsg] = useState("");
const [showPassword,setShowPassword] = useState(false);

/* HANDLE INPUT */

const handleChange = (e)=>{

setForm({
...form,
[e.target.name]:e.target.value
});

};

/* LOGIN SUBMIT */

const handleSubmit = async(e)=>{

e.preventDefault();

setErrorMsg("");

setLoading(true);

try{

const res = await loginUser(form);

/* SAVE TOKENS */

localStorage.setItem("access",res.access);
localStorage.setItem("refresh",res.refresh);

/* SAVE USERNAME FOR DASHBOARD */

localStorage.setItem("username",form.username);

alert("Login successful ✅");

/* REDIRECT */

navigate("/dashboard");

}

catch(error){

console.error("Login failed:",error);

setErrorMsg(
error?.response?.data?.detail ||
error.message ||
"Invalid username or password"
);

}

finally{

setLoading(false);

}

};

return(

<div className="auth-bg">

{/* NAVBAR */}

<nav className="auth-navbar">

<h2 className="logo">
WeatherPro
</h2>

<div className="nav-links">

<Link to="/">
Home
</Link>

<Link to="/login">
Login
</Link>

<Link to="/register">
Register
</Link>

</div>

</nav>

{/* LOGIN CARD */}

<form className="auth-card" onSubmit={handleSubmit}>

<h2>Login</h2>

{errorMsg && (
<p className="error-msg">
{errorMsg}
</p>
)}

<input
name="username"
placeholder="Username"
value={form.username}
onChange={handleChange}
required
/>

<div className="password-box">

<input
type={showPassword ? "text" : "password"}
name="password"
placeholder="Password"
value={form.password}
onChange={handleChange}
required
/>

<span
className="toggle-pass"
onClick={()=>setShowPassword(!showPassword)}
>

{showPassword ? "Hide" : "Show"}

</span>

</div>

<button
type="submit"
disabled={loading}
>

{loading ? "Logging in..." : "Login"}

</button>

<div className="auth-link">

Don't have an account?{" "}

<Link to="/register">
Register
</Link>

</div>

</form>

</div>

);

}