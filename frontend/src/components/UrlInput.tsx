import React, { useState } from 'react';
import { submitUrl} from '../api/api';

const UrlInput: React.FC = () => {
    const [url, setUrl] = useState<string>("");
    
    const handleUrlSubmit = (url: string) => {
        const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
        if(!urlRegex.test(url)) {
            alert("Please enter a URL");
            return;
        }
        submitUrl(url)
            .then(data => {
                console.log(data);
            })
            .catch(error => console.error(error));
    }
    return (
        <>
        <div>
            <input 
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            />
            <button onClick={() => handleUrlSubmit(url)}>Run Query</button>
        </div>
        </>
    )
}

export default UrlInput;