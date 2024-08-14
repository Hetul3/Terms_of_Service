import React, { useState } from 'react';

const TextInput: React.FC = () => {
    const [text, setText] = useState<string>("");

    const submitText = (text: string) => {
        if(text === null || text === "") {
            alert("Please enter longer text");
            return;
        }
        fetch('http://localhost:8080/rag/process_text_contract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .catch(error => console.error(error))
    }

    return (
        <>
        <div>
            <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            />
            <button onClick={() => submitText(text)}>Run Query</button>
        </div>
        </>
    )
}

export default TextInput;