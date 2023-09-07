import React, { useState } from 'react';
import "./UploadGoogledrive.css";
import axios from 'axios';

const UploadGoogleDrive = () => {
    const [directoryInput, setDirectoryInput] = useState('');
    const [authenticatorCode, setAuthenticatorCode] = useState(null);

    const handleInputChange = (event) => {
        setDirectoryInput(event.target.value);
    };

    const handleUpload = async () => {
        try {
            const response = await uploadDirectory(directoryInput);
        } catch (error) {
            console.error('Error uploading directory: ', error);
        }
    };

    const uploadDirectory = async (directory) => {
        // Simulated upload function
        const res = await axios.post('http://localhost:80/gdrive', {
            query: directory,
        });
        console.log(res);
    };

    return (
        <div className="uploadGoogleDrive">
            <h2><b>Google Drive</b></h2>
            <br></br>
            <input
                className="file-input"
                type="text"
                placeholder="Enter URL"
                value={directoryInput}
                onChange={handleInputChange}
            />
            <button className="file-button" onClick={handleUpload}>Submit</button>
        </div>
    );
};

export default UploadGoogleDrive;
