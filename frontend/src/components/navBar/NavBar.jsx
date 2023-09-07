import "./NavBar.css";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useState } from "react";
import {LinkContainer} from 'react-router-bootstrap'
import logo from "../../image/logo.png"


function NavBar() {
    const [active, setActive] = useState('navBar');
    const navigate = useNavigate();
    return (
        <div className="NavbarContainer">
          <NavLink className="NavbarLogo" to="/">
            <img className="NavbarLogoImg" src={logo}>
            </img>
          </NavLink>
          
          <div className="NavbarMenu">
            <div className="NavbarItem">
              <NavLink className="NavbarLinks" to="/">Home</NavLink>
            </div>
            <div className="NavbarItem">
              <NavLink className="NavbarLinks" to="/chat">Chat</NavLink>
            </div>
          </div>
          <main>
            <Outlet/>
          </main>
        </div>
      );
    }
    export default NavBar;
    