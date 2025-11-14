document.addEventListener('DOMContentLoaded', function () {
    const previewButton = document.getElementById('preview-button');
    const htmlInput = document.getElementById('html-input');
    const previewFrame = document.getElementById('preview-frame');

    // New elements for pipeline control
    const startCycleButton = document.getElementById('start-cycle-button');
    const cycleStatusDiv = document.getElementById('cycle-status');

    // Preview functionality
    if (previewButton && htmlInput && previewFrame) {
        previewButton.addEventListener('click', function () {
            const htmlContent = htmlInput.value;
            
            // Access the iframe's document
            const previewDoc = previewFrame.contentDocument || previewFrame.contentWindow.document;
            
            if (previewDoc) {
                // Find the container inside the iframe
                const contentContainer = previewDoc.getElementById('content-container');
                if (contentContainer) {
                    // Inject the HTML
                    contentContainer.innerHTML = htmlContent;
                } else {
                    console.error('Preview container #content-container not found in iframe.');
                }
            } else {
                console.error('Could not access preview frame document.');
            }
        });
    } else {
        console.error('One or more required elements for preview (button, input, or frame) not found.');
    }

    // Pipeline control functionality
    if (startCycleButton && cycleStatusDiv) {
        startCycleButton.addEventListener('click', async function () {
            cycleStatusDiv.textContent = 'Starting new cycle...';
            try {
                const response = await fetch('/api/cycle/start', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ mode: 'standard', template: 'blog-post-default.html' }) // Default values for now
                });
                const data = await response.json();

                if (response.ok) {
                    cycleStatusDiv.innerHTML = `Cycle started! Redirecting to <a href="${data.redirect_url}" class="text-blue-600 hover:underline">${data.redirect_url}</a>`;
                    // Optionally, redirect or update UI further
                } else {
                    cycleStatusDiv.textContent = `Error starting cycle: ${data.error || 'Unknown error'}`;
                    console.error('Error starting cycle:', data);
                }
            } catch (error) {
                cycleStatusDiv.textContent = `Network error: ${error.message}`;
                console.error('Network error:', error);
            }
        });
    } else {
        console.error('One or more required elements for pipeline control (start button or status div) not found.');
    }
});
