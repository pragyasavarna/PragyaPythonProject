document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("comingSoonModal");

    // Add click events to coming soon cards
    document.querySelectorAll(".coming-soon .ai-card-link").forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            showComingSoon();
        });
    });

    function showComingSoon() {
        modal.classList.add("show");

        setTimeout(() => {
            modal.classList.remove("show");
        }, 800);
    }

    // Click anywhere to close early
    modal.addEventListener("click", () => {
        modal.classList.remove("show");
    });
});