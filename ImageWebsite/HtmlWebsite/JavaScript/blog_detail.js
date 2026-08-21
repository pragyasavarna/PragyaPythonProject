document.addEventListener("DOMContentLoaded", function () {
    const topBtn = document.getElementById("btnScrollTop");
    const bottomBtn = document.getElementById("btnScrollBottom");
    const btnContainer = document.querySelector(".floating-scroll-btns");

    // Function to check if the page is long enough to need scrolling
    function checkScrollability() {
        if (!btnContainer) return;

        // Compare total document height to the visible window height
        const isScrollable = document.documentElement.scrollHeight > window.innerHeight;

        if (isScrollable) {
            btnContainer.style.display = "flex";
        } else {
            btnContainer.style.display = "none";
        }
    }

    // Run the check when the page loads
    checkScrollability();

    // Re-run the check if the user resizes their window
    window.addEventListener("resize", checkScrollability);

    // Smooth Scroll to Top
    if (topBtn) {
        topBtn.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }

    // Smooth Scroll to Bottom
    if (bottomBtn) {
        bottomBtn.addEventListener("click", function () {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: "smooth"
            });
        });
    }
});