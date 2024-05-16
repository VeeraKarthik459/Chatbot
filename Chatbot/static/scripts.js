async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const uploadResponse = document.getElementById('uploadResponse');

    if (fileInput.files.length === 0) {
        uploadResponse.innerText = 'Please select a file to upload.';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload_file', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (result.response) {
            uploadResponse.innerText = result.response;
        } else if (result.error) {
            uploadResponse.innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        uploadResponse.innerText = `Error: ${error.message}`;
    }
}

async function submitQuery() {
    const queryInput = document.getElementById('queryInput');
    const queryResponse = document.getElementById('queryResponse');
    const query = queryInput.value.trim();

    if (query === '') {
        queryResponse.innerText = 'Please enter a query.';
        return;
    }

    try {
        const response = await fetch('/get_query_result', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        const result = await response.json();
        if (result.response) {
            queryResponse.innerText = result.response;
        } else if (result.error) {
            queryResponse.innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        queryResponse.innerText = `Error: ${error.message}`;
    }
}
