import { useNavigate } from "react-router-dom";

export default function Navbar() {

  const nav = useNavigate();

  const logout = () => {
    localStorage.removeItem("access");
    nav("/login");
  };

  return (
    <nav className="navbar navbar-dark bg-dark px-4">
      <h4 className="text-white">🌤 Weather Pro</h4>

      <button className="btn btn-danger" onClick={logout}>
        Logout
      </button>
    </nav>
  );
}