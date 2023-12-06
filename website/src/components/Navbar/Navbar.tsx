import logo from "./ucslogo.webp";
import { NavLink } from "react-router-dom";

function Navbar() {
  const linkStyle = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium ${
      isActive ? "bg-blue-500 text-white" : "text-gray-600 hover:bg-gray-200"
    }`;

  const isAdmin = JSON.parse(localStorage.getItem('isAdmin') || 'false');

  return (
    <nav className="bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between py-3">
          {/* Logo and brand name */}
          <NavLink to="/" className="flex items-center space-x-2">
            <img src={logo} alt="logo" className="w-32" />
          </NavLink>
          {/* Navigation Links */}
          <div className="flex space-x-4">
            {/* Use NavLink for "Data" */}
            <NavLink to="/data" className={linkStyle}>
              Verified Data
            </NavLink>
            {/* Use NavLink for "Updates" */}
            <NavLink to="/updates" className={linkStyle}>
              Proposed Changes
            </NavLink>
            <NavLink to="/changelog" className={linkStyle}>
              Changelog
            </NavLink>
            {isAdmin && (
              <NavLink to="/users" className={linkStyle}>
                User Management
              </NavLink>
            )}
            <NavLink to="/logout" className={linkStyle}>
              Logout
            </NavLink>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
