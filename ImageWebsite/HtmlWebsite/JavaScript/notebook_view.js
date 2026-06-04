document.addEventListener("DOMContentLoaded", function () {
    const iframe = document.getElementById("notebook-iframe");
    const loader = document.getElementById("notebook-loader");

    if (iframe && loader) {
        iframe.addEventListener("load", function () {

            // Lock the scroll briefly to stop Jupyter's jump
            let scrollLock = setInterval(() => {
                window.scrollTo(0, 0);
            }, 10);

            setTimeout(() => {
                clearInterval(scrollLock);

                // --- NEW DYNAMIC HEIGHT CALCULATION ---
                // 1. Measure the exact height of the notebook content inside the iframe
                const contentHeight = iframe.contentWindow.document.documentElement.scrollHeight;

                // 2. Apply that exact height (plus a tiny bit of padding) to the iframe
                iframe.style.height = (contentHeight + 20) + "px";
                // --------------------------------------

                loader.style.display = "none";
                iframe.style.opacity = "1";

            }, 800);
        });
    }
});