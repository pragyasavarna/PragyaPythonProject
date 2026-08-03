// Wait for the HTML structure to fully load before running the script
document.addEventListener('DOMContentLoaded', function () {

    const dobInput = document.getElementById('dob');

    // Make sure the element exists before adding the listener
    if (dobInput) {
        if (window.innerWidth <= 768) {
            // Get today's date and format it strictly as YYYY-MM-DD
            const today = new Date().toISOString().split('T')[0];
            dobInput.value = today; // Set the default value
        }
        dobInput.addEventListener('click', function () {
            // Check if the browser supports showPicker()
            if (this.showPicker) {
                this.showPicker();
            }
        });
    }

});