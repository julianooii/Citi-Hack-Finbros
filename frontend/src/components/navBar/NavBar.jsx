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
          <div className="NavbarLogo" to="/">
            <img className="NavbarLogoImg" src={logo}>
            </img>
          </div>
          
          <div className="NavbarMenu">
            <div className="NavbarItem">
              <div className="NavbarLinks" to="/">Home</div>
            </div>
            <div className="NavbarItem">
              <div className="NavbarLinks" to="/chat">Chat</div>
            </div>
          </div>
          <main>
            <Outlet/>
          </main>
        </div>
      );
    }
    export default NavBar;
    