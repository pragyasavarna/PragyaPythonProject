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
  const errorMessage = document.getElementById("error-message");

  preview.innerHTML = "";

  if (errorMessage) {
    errorMessage.style.display = "none";
    errorMessage.textContent = "";
  }

  const file = event.target.files[0];

  if (file) {
    console.log("File selected:", file.name);
    console.log("File type:", file.type);

    // robust validation: check mime type and extension
    const validMimeTypes = ["image/png", "image/jpeg", "image/jpg"];
    const validExtensions = ["png", "jpg", "jpeg"];

    const fileExtension = file.name.split('.').pop().toLowerCase();
    const isValidMime = validMimeTypes.includes(file.type);
    const isValidExt = validExtensions.includes(fileExtension);

    // If mime type is empty (sometimes happens), rely on extension. 
    // If mime type is present, it must be valid.
    let isValid = false;

    if (file.type === "") {
      isValid = isValidExt;
    } else {
      isValid = isValidMime;
    }

    if (!isValid) {
      console.log("Invalid file. Type:", file.type, "Extension:", fileExtension);
      if (errorMessage) {
        errorMessage.textContent = "Please select a PNG, JPG, or JPEG image.";
        errorMessage.style.display = "block";
      } else {
        alert("Please select a PNG, JPG, or JPEG image."); // Fallback
      }
      event.target.value = ""; // Clear the input
      return;
    }

    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    img.onload = () => URL.revokeObjectURL(img.src);
    preview.appendChild(img);
    // 👉 CLEAR prediction div whenever a new image is chosen
    document.querySelector(".prediction").textContent = "";
  }
}

/* ===========================
   📱 MOBILE MENU TOGGLE
=========================== */
function toggleMenu() {
  const menu = document.getElementById('nav-menu');
  const body = document.body;
  // 1. Toggle the menu visibility
  menu.classList.toggle('active');
  // 2. Toggle the "Body Scroll Lock"
  // This adds/removes the class 'no-scroll' from the <body> tag
  body.classList.toggle('no-scroll');
}

/* ===========================
   🔹 NEW: CLOSE MENU ON OUTSIDE CLICK
   (Paste this at the bottom of your script.js)
=========================== */
document.addEventListener('click', function (event) {
  const menu = document.getElementById('nav-menu');
  const hamburger = document.querySelector('.hamburger');
  const body = document.body;

  // 1. Check if the menu is actually OPEN
  if (menu.classList.contains('active')) {

    // 2. Check if the click was NOT inside the menu AND NOT on the hamburger icon
    if (!menu.contains(event.target) && !hamburger.contains(event.target)) {

      // 3. Close the menu and unfreeze the body
      menu.classList.remove('active');
      body.classList.remove('no-scroll');
    }
  }
});