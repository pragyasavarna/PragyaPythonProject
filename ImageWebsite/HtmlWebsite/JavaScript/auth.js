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

// Toggle password visibility function
document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eye-icon');

    // Only add the listener if all elements exist
    if (toggleButton && passwordInput && eyeIcon) {
        toggleButton.addEventListener('click', function () {
            // 1. Determine the new state
            const isPassword = passwordInput.type === 'password';

            // 2. Set the new input type
            passwordInput.type = isPassword ? 'text' : 'password';

            // 3. Set the new image path dynamically
            const iconUrl = `url('/Image/visibility_${isPassword ? 'off' : 'on'}.svg')`;

            // 4. Apply the CSS masks
            eyeIcon.style.maskImage = iconUrl;
            eyeIcon.style.setProperty('-webkit-mask-image', iconUrl);
        });
    }
});