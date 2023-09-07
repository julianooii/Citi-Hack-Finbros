import React, { useState, useEffect, useContext } from "react";
import NavBar from "../components/navBar/NavBar";
import Home from "../components/homecomponent/Home";
import FileUpload from "../components/fileUpload/FileUpload";

const HomePage = () => {
    return(
        <div>
        <Home />
        <FileUpload/>
        </div>
    );
};
export default HomePage;