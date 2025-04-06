export function showLoadingOverlay() {
    const existingOverlay = document.getElementById('loading-overlay');
    if (!existingOverlay) {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.innerHTML = `
            <div class="spinner"></div>
            <h2>Processing your payment...</h2>
        `;
        overlay.classList.add('loading-overlay');
        document.body.appendChild(overlay);
    }
}

export function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

