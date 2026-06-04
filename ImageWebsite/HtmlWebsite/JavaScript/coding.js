document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("fileSearch");
    const listItems = document.querySelectorAll(".list-item");

    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            let filter = searchInput.value.toLowerCase();

            listItems.forEach(function (item) {
                // Prevent filtering out the 'Go Back' button
                if (item.classList.contains("parent-dir")) {
                    return;
                }

                let text = item.textContent || item.innerText;

                // Show or hide based on search match
                if (text.toLowerCase().indexOf(filter) > -1) {
                    item.style.display = "flex";
                } else {
                    item.style.display = "none";
                }
            });
        });
    }
});