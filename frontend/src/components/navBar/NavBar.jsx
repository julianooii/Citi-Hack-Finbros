import "./NavBar.css";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useState } from "react";
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import {LinkContainer} from 'react-router-bootstrap'
import logo from "../../image/logo.png"
// import Container from 'react-bootstrap/Container';
// import Nav from 'react-bootstrap/Nav';
// import Navbar from 'react-bootstrap/Navbar';
// import {LinkContainer} from 'react-router-bootstrap'


function NavBar() {
    const [active, setActive] = useState('navBar');
    const navigate = useNavigate();
    return (
        <section>
          <nav className="navigation">
            {/* <a href="/" className="brand-name">
              <img className="logo" src="edventure_logo.png" alt="" />
            </a> */}
            <div
              className="navigation-menu">
              <ul>
                <li>
                  <NavLink to="/" className="navLink" style={({ isActive }) => { return { color: isActive ? 'white' : '', background: isActive ? '#004486' : "white", borderRadius: isActive ? "12px" : '', textDecoration: "none" } }}>Home</NavLink>
                </li>
                <li>
                  <NavLink to="/chat" className="navLink" style={({ isActive }) => { return { color: isActive ? 'white' : '', background: isActive ? '#004486' : "white", borderRadius: isActive ? "12px" : '', textDecoration: "none" } }}>Chat</NavLink>
                </li>
                {/* <li>
                  <NavLink to="/profile" className="navLink" style={({ isActive }) => { return { color: isActive ? 'white' : '', background: isActive ? '#456bf5' : "white", borderRadius: isActive ? "12px" : '', textDecoration: "none" } }}>Profile</NavLink>
                </li> */}
                {/* <li>
                    <button className="navLink" onClick={logOut}>Log out</button>
                </li> */}
              </ul>
            </div>
          </nav>
    
          <main>
            <Outlet/>
          </main>
          </section>
        
      );
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
    