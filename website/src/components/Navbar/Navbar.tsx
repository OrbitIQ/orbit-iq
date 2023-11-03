import logo from "./ucslogo.webp";
import { Button } from "../ui/button";
import { Link } from "react-router-dom";

function Navbar() {
    return (
        <>
            <div
                style={{
                    margin: "auto",
                    width: 1600,
                    paddingTop: "2.3rem",
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "left",
                }}
            >
                <img src={logo} width={200} height={200} />
                <Link to="/data">
                    <Button variant="outline" size="icon">Data</Button>
                </Link>
                <Link to="/updates">
                    <Button variant="outline" size="icon">Update</Button>
                </Link>
                <Link to="/changelog">
                    <Button variant="outline" size="icon">Changelog</Button>
                </Link>
            </div>
        </>
    )
}

export default Navbar;