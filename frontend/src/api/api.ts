const API_BASE_URL: string = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8080';

export async function queryLlm(query: string) {
    const response = await fetch(`${API_BASE_URL}/rag/query_llm`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: query })
    })

    if(!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

export async function uploadImage(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/rag/process_image_contract`, {
        method: 'POST',
        body: formData
    });

    if(!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const contentType = response.headers.get("content-type");
    if(contentType && contentType.indexOf("application/json") !== -1) {
        return response.json();
    } else {
        return response.text();
    }
}

export async function submitUrl(url: string) {
    const response = await fetch(`${API_BASE_URL}/rag/process_url_contract`, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })

    if(!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

export async function submitText(text: string) {
    const response = await fetch(`${API_BASE_URL}/rag/process_text_contract`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })

    if(!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

export async function submitFeedback(feedback_type: boolean, classification: string, explanation: string, phrase: string) {
    const data = {
        "feedback_time": new Date().toISOString(),
        "feedback_type": feedback_type,
        "classification": classification,
        "explanation": explanation,
        "phrase": phrase
    }

    const response = await fetch(`${API_BASE_URL}/feedback/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })

    if(!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}