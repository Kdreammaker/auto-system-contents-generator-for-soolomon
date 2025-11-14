document.addEventListener('DOMContentLoaded', function () {
    const previewButton = document.getElementById('preview-button');
    const htmlInput = document.getElementById('html-input');
    const previewFrame = document.getElementById('preview-frame');

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
        console.error('One or more required elements (button, input, or frame) not found.');
    }
});
