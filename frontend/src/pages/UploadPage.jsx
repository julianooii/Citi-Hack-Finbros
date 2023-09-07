import Chat from "../components/chat/Chat";
import React, { useState, useEffect, useContext } from "react";
import NavBar from "../components/navBar/NavBar";
import UploadFile from "../components/uploadFile/UploadFile";

const UploadPage = () => {
    return(
        <div>
            <UploadFile/>
        </div>
    );
};
export default UploadPage;