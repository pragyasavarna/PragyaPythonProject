document.addEventListener("DOMContentLoaded", function () {
    const authForm = document.querySelector(".auth-form");

    if (authForm) {
        // Grab the submit button inside this specific form
        const submitBtn = authForm.querySelector(".btn-submit");

        authForm.addEventListener("submit", function (event) {
            // 1. Check reCAPTCHA first
            const recaptchaResponse = grecaptcha.getResponse();

            if (recaptchaResponse.length === 0) {
                event.preventDefault();
                alert("Please check the 'I am not a robot' box before submitting.");
                return; // Stop execution here so the button doesn't get disabled
            }

            // 2. If reCAPTCHA is checked and form fields are valid, prevent double-click
            if (authForm.checkValidity()) {
                submitBtn.innerText = "Sending...";
                submitBtn.style.opacity = "0.7";
                submitBtn.style.cursor = "not-allowed";
                submitBtn.style.pointerEvents = "none";
            }
        });
    }
});