 import React, { useState, ChangeEvent, FormEvent } from 'react';

 const ImageInput: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);

    const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        if(event.target.files && event.target.files.length > 0) {
            setFile(event.target.files[0]);
        }
    };

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();
        if(!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8080/rag/process_image_test', {
                method: 'POST',
                body: formData
            });
        
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const data = await response.json();
                console.log("extracted text", data.text);
            } else {
                const text = await response.text();
                console.log("extracted text", text);
            }
        } catch(error) {
            console.error("Error uploading image", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} accept=".pdf, .png, .jpg, .jpeg" placeholder='Insert image' />
            <button type="submit">Upload</button>
        </form>
    )
 }

 export default ImageInput;