 import React, { useState, ChangeEvent, FormEvent } from 'react';
import {uploadImage} from '../api/api';

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

        try {
            const data = await uploadImage(file);
            console.log("extracted text: ", data);
        } catch(error) {
            console.error(error);
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