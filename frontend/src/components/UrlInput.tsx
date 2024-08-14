import React, { useState } from 'react';

const UrlInput: React.FC = () => {
    const [url, setUrl] = useState<string>("");
    
    const submitUrl = (url: string) => {
        const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
        if(!urlRegex.test(url)) {
            alert("Please enter a URL");
            return;
        }
        fetch('http://localhost:8080/rag/process_url_contract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .catch(error => console.error(error))
    }
    return (
        <>
        <div>
            <input 
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            />
            <button onClick={() => submitUrl(url)}>Run Query</button>
        </div>
        </>
    )
}

export default UrlInput;