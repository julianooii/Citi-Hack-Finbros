import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css';

function FileUpload() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState('');
  
    const handleFileUpload = async () => {
      try {
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
      <div className='fileupload'>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button className="file-button" onClick={handleFileUpload}>Upload and OCR</button>
        <div>{result.result}</div>
      </div>
    );
  }
  
  export default FileUpload;