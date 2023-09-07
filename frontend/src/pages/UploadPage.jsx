import React, { useState, useEffect, useContext } from "react";
import NavBar from "../components/navBar/NavBar";
import UploadOneDrive from "../components/uploadOnedrive/UploadOnedrive";
import UploadFile from "../components/uploadFile/UploadFile";

const UploadPage = () => {
    return(
        <div>
            <UploadOneDrive />
            <UploadFile/>
        </div>
    );
};
export default UploadPage;