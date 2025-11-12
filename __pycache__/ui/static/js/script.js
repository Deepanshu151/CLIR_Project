// CLIR System Frontend JavaScript

function performSearch() {
    const query = document.getElementById('queryInput').value.trim();
    const topK = parseInt(document.getElementById('topK').value) || 5;
    
    if (!query) {
        showError('Please enter a query');
        return;
    }
    
    // Hide previous results and errors
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    
    // Make API request
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: query,
            top_k: topK
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        document.getElementById('loading').style.display = 'none';
        showError('Network error: ' + error.message);
    });
}

function displayResults(data) {
    // Display translated query
    document.getElementById('translatedQuery').textContent = data.translated_query;
    
    // Display results
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = '';
    
    if (data.results.length === 0) {
        resultsList.innerHTML = '<p>No relevant documents found.</p>';
    } else {
        data.results.forEach((result, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            resultItem.innerHTML = `
                <h4>Result #${index + 1} <span class="score">Score: ${result.score.toFixed(3)}</span></h4>
                <p>${result.document}</p>
            `;
            resultsList.appendChild(resultItem);
        });
    }
    
    // Display translated top result if available
    if (data.translated_top_result) {
        document.getElementById('translatedResultText').textContent = data.translated_top_result;
        document.getElementById('translatedResult').style.display = 'block';
    }
    
    document.getElementById('results').style.display = 'block';
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').style.display = 'block';
}

// Allow Enter key to trigger search
document.getElementById('queryInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

