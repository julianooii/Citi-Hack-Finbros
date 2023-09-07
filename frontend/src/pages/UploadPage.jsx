import React, { useState, useEffect, useContext } from "react";
import NavBar from "../components/navBar/NavBar";
import UploadOneDrive from "../components/uploadOnedrive/UploadOnedrive";
import UploadFile from "../components/uploadFile/UploadFile";
import UploadGoogleDrive from "../components/uploadGoogledrive/UploadGoogledrive";

const UploadPage = () => {
    return(
        <div>
            <UploadFile/>
            <UploadOneDrive />
            <UploadGoogleDrive/>
        </div>
    );
};
export default UploadPage;