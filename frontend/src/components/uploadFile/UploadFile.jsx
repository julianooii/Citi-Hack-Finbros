import React, { useState } from 'react';
import axios from 'axios';
import './UploadFile.css';

function UploadFile() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState('');
  
    const handleFileUpload = async () => {
      try {
        setResult({result: "Uploading..."})
        const formData = new FormData();
        formData.append('file', file);
  
        const response = await axios.post('http://127.0.0.1:80/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
  
        setResult(response.data);
        console.log(result);

      } catch (error) {
        console.error('Error uploading file:', error);
        // Handle error gracefully
      }
    };
  
    return (
      <div className='uploadfile'>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button className="uploadfile-button" onClick={handleFileUpload}>Upload</button>
        <div>{result.result}</div>
      </div>
    );
  }
  
  export default UploadFile;