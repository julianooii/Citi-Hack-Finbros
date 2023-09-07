import React, { useState } from 'react';

const UploadOneDrive = () => {
    const [directoryInput, setDirectoryInput] = useState('');
    const [authenticatorCode, setAuthenticatorCode] = useState(null);

    const handleInputChange = (event) => {
        setDirectoryInput(event.target.value);
    };

    const handleUpload = async () => {
        try {
            const response = await uploadDirectory(directoryInput);
            setAuthenticatorCode(response.data.authenticatorCode);
        } catch (error) {
            console.error('Error uploading directory: ', error);
        }
    };

    const uploadDirectory = async (directory) => {
        // Simulated upload function
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({ data: { authenticatorCode: '123456' } });
            }, 2000); // Simulating a 2-second delay for the upload process
        });
    };

    return (
        <div className="uploadOnedrive">
            <input
                className="file-input"
                type="text"
                placeholder="Enter folder directory"
                value={directoryInput}
                onChange={handleInputChange}
            />
            <button className="file-button" onClick={handleUpload}>Upload</button>
            <div>{authenticatorCode && <div>Authenticator Code: {authenticatorCode}</div>}</div>
        </div>
    );
};

export default UploadOneDrive;
