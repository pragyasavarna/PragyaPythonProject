document.addEventListener('DOMContentLoaded', () => {
    const classSelect = document.getElementById('class-select');
    const form = document.getElementById('class-selector-form');

    if (classSelect && form) {
        classSelect.addEventListener('change', () => {
            // Re-fetch the page with the new class_id parameter
            form.submit();
        });
    }
});