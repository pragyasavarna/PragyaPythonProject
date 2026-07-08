// Auto-update footer copyright year
document.addEventListener('DOMContentLoaded', function () {
    // Find the span with the ID 'dynamic-year'
    const yearSpan = document.getElementById('dynamic-year');

    // If it exists on the page, set its text to the current year
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});