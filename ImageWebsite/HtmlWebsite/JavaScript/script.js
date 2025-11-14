document.addEventListener("DOMContentLoaded", function () {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll("nav a");

  navLinks.forEach(link => {
    const linkPath = link.getAttribute("href");

    if (
      (currentPath === "/" && linkPath === "/") ||
      (currentPath.startsWith(linkPath) && linkPath !== "/")
    ) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });
});

function previewImage(event) {
      const preview = document.getElementById("preview");
      preview.innerHTML = "";
      const file = event.target.files[0];
      if (file) {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.onload = () => URL.revokeObjectURL(img.src);
        preview.appendChild(img);
      }
    }