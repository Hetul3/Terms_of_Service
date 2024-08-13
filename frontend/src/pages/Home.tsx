import React from 'react';

const Home: React.FC = () => {
    const runQuery = () => {
        let query: string = "Give me a logical fallacy";
        fetch('http://localhost:8080/rag/query_llm', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: query })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log(error));
    }

    return (
        <div>
            <button onClick={runQuery}>Run Query</button>
        </div>
    )
}

export default Home;