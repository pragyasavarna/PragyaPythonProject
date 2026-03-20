// Wait for the HTML structure to fully load before running the script
document.addEventListener('DOMContentLoaded', function () {

    const dobInput = document.getElementById('dob');

    // Make sure the element exists before adding the listener
    if (dobInput) {
        dobInput.addEventListener('click', function () {
            // Check if the browser supports showPicker()
            if (this.showPicker) {
                this.showPicker();
            }
        });
    }

});