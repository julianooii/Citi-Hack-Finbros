import React, { useState } from 'react';
import axios from 'axios';

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
            const authResponse = await axios.post('http://127.0.0.1:90/oneDriveAuth', {
                directory: directoryInput
            });

            const code = authResponse.data.message[0];
            setAuthenticatorCode(code);

            // Step 2: Send POST request to oneDriveFileExtract
            const extractResponse = await axios.post('http://127.0.0.1:90/oneDriveFileExtract');

            const uploadMessage = extractResponse.data.message;
            setUploadMessage(uploadMessage);
        } catch (error) {
            console.error('Error uploading directory: ', error);
        }
    };

    return (
        <div className="uploadOnedrive">
            <b>OneDrive</b>
            <br></br>
            <input
                className="file-input"
                type="text"
                placeholder="Enter folder directory"
                value={directoryInput}
                onChange={handleInputChange}
            />
            <button className="file-button" onClick={handleUpload}>Upload to OneDrive</button>
            <div>{authenticatorCode && <div>Authenticator Code: {authenticatorCode}</div>}</div>
            <div>{uploadMessage && <div>{uploadMessage}</div>}</div>
        </div>
    );
};

export default UploadOneDrive;
