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
            const response = await fetch('http://localhost:8080/rag/process_image_contract', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            console.log(data);
        } catch(error) {
            console.error("Error uploading image", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} accept=".pdf, .png, .jpg, .jpeg" />
            <button type="submit">Upload</button>
        </form>
    )
 }

 export default ImageInput;