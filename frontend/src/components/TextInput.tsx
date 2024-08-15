import React, { useState } from 'react';
import {submitText} from '../api/api';

const TextInput: React.FC = () => {
    const [text, setText] = useState<string>("");

    const handleSubmitText = (text: string) => {
        if(text === null || text === "") {
            alert("Please enter longer text");
            return;
        }
        submitText(text)
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
            value={text}
            onChange={(e) => setText(e.target.value)}
            />
            <button onClick={() => handleSubmitText(text)}>Run Query</button>
        </div>
        </>
    )
}

export default TextInput;