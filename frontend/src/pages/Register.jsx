// src/pages/Register.jsx

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { registerUser } from "../services/accountsServices";
import "../styles/auth.css";

export default function Register() {

const navigate = useNavigate();

const [form,setForm] = useState({
username:"",
email:"",
password:"",
password2:""
});

const [error,setError] = useState("");
const [loading,setLoading] = useState(false);
const [showPassword,setShowPassword] = useState(false);

/* HANDLE INPUT */

const handleChange = (e)=>{

setForm({
...form,
[e.target.name]:e.target.value
});

};

/* FORM VALIDATION */

const validateForm = ()=>{

if(!form.username || !form.email || !form.password || !form.password2){
return "All fields are required";
}

if(form.password.length < 4){
return "Password must be at least 4 characters";
}

if(form.password !== form.password2){
return "Passwords do not match";
}

return null;

};

/* REGISTER SUBMIT */

const handleSubmit = async(e)=>{

e.preventDefault();

const validationError = validateForm();

if(validationError){
setError(validationError);
return;
}

setError("");
setLoading(true);

try{

const response = await registerUser({
username:form.username.trim(),
email:form.email.trim(),
password:form.password
});

console.log("Register success:",response);

alert("Registration Successful ✅");

navigate("/login");

}

catch(err){

console.error("Register error:",err);

if(err.response && err.response.data){
setError(JSON.stringify(err.response.data));
}else{
setError("Registration failed. Please try again.");
}

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

{/* REGISTER CARD */}

<form className="auth-card" onSubmit={handleSubmit}>

<h2>Create Account</h2>

{error && (
<p className="error-msg">
{error}
</p>
)}

<input
name="username"
placeholder="Username"
value={form.username}
onChange={handleChange}
/>

<input
type="email"
name="email"
placeholder="Email"
value={form.email}
onChange={handleChange}
/>

<div className="password-box">

<input
type={showPassword ? "text" : "password"}
name="password"
placeholder="Password"
value={form.password}
onChange={handleChange}
/>

<span
className="toggle-pass"
onClick={()=>setShowPassword(!showPassword)}
>

{showPassword ? "Hide" : "Show"}

</span>

</div>

<input
type={showPassword ? "text" : "password"}
name="password2"
placeholder="Confirm Password"
value={form.password2}
onChange={handleChange}
/>

<button type="submit" disabled={loading}>

{loading ? "Registering..." : "Register"}

</button>

<div className="auth-link">

Already have an account?{" "}

<Link to="/login">
Login
</Link>

</div>

</form>

</div>

);

}