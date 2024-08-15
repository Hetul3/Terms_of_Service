export async function uploadImage(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:8080/rag/process_image_test', {
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
    const response = await fetch('http://localhost:8080/rag/process_url_contract', {
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
    const response = await fetch('http://localhost:8080/rag/process_text_contract', {
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