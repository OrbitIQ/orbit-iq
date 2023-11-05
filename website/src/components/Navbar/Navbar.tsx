import logo from "./ucslogo.webp";
import { Button } from "../ui/button";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <>
      <nav className="navbar">
        <img src={logo} alt="UCS Logo" className="logo" />
        <Link to="/data">
          <Button variant="outline" buttonSize="icon" textSize="lg">
            Data
          </Button>
        </Link>
        <Link to="/updates">
          <Button variant="outline" buttonSize="icon" textSize="lg">
            Update
          </Button>
        </Link>
        <Link to="/changelog">
            <Button variant="outline" buttonSize="icon">Changelog</Button>
        </Link>
      </nav>
    </>
  );
}

export default Navbar;
