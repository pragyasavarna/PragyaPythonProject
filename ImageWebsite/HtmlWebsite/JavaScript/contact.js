document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.querySelector(".contact-form");

    if (contactForm) {
        contactForm.addEventListener("submit", function (event) {
            const recaptchaResponse = grecaptcha.getResponse();

            if (recaptchaResponse.length === 0) {
                event.preventDefault();
                alert("Please check the 'I am not a robot' box before submitting.");
            }
        });
    }
});