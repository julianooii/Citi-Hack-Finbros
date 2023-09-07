import React, { useState } from 'react';
import axios from 'axios';
import "./UploadOnedrive.css"

const UploadOneDrive = () => {
    const [directoryInput, setDirectoryInput] = useState('');
    const [authenticatorCode, setAuthenticatorCode] = useState(null);
    const [uploadMessage, setUploadMessage] = useState('');

    const handleInputChange = (event) => {
        setDirectoryInput(event.target.value);
    };

    const handleUpload = async () => {
        try {
            // Step 1: Send POST request to oneDriveAuth
            const authResponse = await axios.post('http://127.0.0.1:80/oneDriveAuth', {
                message: directoryInput
            });

            const code = authResponse.data.message[0];
            console.log("Received authenticator code:", code);
            setAuthenticatorCode(code);

            // Step 2: Send POST request to oneDriveFileExtract
            const extractResponse = await axios.post('http://localhost:80/oneDriveFileExtract', {
                message: authResponse.data.message
            });

            console.log("authresponse here!!!!!", authResponse)

            const uploadMessage = extractResponse.data.message;
            setUploadMessage(uploadMessage);
        } catch (error) {
            console.error('Error uploading directory: ', error);
        }
    };

    return (
        <div className="uploadOnedrive">
            <h2><b>OneDrive</b></h2>
            <br></br>
            <input
                className="file-input"
                type="text"
                placeholder="Enter folder directory"
                value={directoryInput}
                onChange={handleInputChange}
            />
            <button className="file-button" onClick={handleUpload}>Submit</button>
            <div>{authenticatorCode !== null && <div>Authenticator Code: {authenticatorCode}</div>}</div>
            <div>{uploadMessage && <div>{uploadMessage}</div>}</div>
        </div>
    );
};

export default UploadOneDrive;
