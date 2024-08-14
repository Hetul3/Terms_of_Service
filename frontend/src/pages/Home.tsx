import React from 'react';
import { useState } from 'react';
import ImageInput from '../components/ImageInput';

const Home: React.FC = () => {
    const [query, setQuery] = useState<string>("");
    const [llmResponse, setLlmResponse] = useState<string>("");

    const runQuery = (query: string) => {
        fetch('http://localhost:8080/rag/query_llm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: query })
        })
        .then(response => response.json())
        .then(
            data => {
                console.log(data);
                setLlmResponse(data.response);
            }
        )
        .catch(error => console.error(error));
    }

    return (
        <div>
            <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button onClick={() => runQuery(query)}>Run Query</button>
            <ImageInput />
            <h1>{llmResponse}</h1>
        </div>
    )
}

export default Home;