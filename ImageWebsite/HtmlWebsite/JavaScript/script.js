/* =========================================
   🟢 DYNAMIC LAYOUT ADJUSTER
   (Handles Fixed Header & Fixed Footer spacing)
========================================= */
function adjustLayout() {
  const header = document.querySelector('header');
  const footer = document.querySelector('footer');
  const main = document.querySelector('main');

  // Safety check: Ensure elements exist
  if (!main) return;

  // --- 1. HEADER ADJUSTMENT (Top Spacing) ---
  if (header) {
    let headerHeight = header.offsetHeight;
    if (window.innerWidth <= 768) {
      // Reduce the height by 70%
      headerHeight = headerHeight - (headerHeight * 0.70);
    }
    const currentTop = parseFloat(main.style.paddingTop) || 0;

    // Only update if size changed significantly (>1px)
    if (Math.abs(headerHeight - currentTop) > 1) {
      main.style.paddingTop = headerHeight + 'px';
    }
  }

  // --- 2. FOOTER ADJUSTMENT (Bottom Spacing) ---
  // ⚠️ Only keeps content from hiding behind a FIXED footer
  if (footer) {
    // Check if footer is actually fixed before applying padding
    const footerStyle = window.getComputedStyle(footer);

    if (footerStyle.position === 'fixed') {
      const footerHeight = footer.offsetHeight;
      const currentBottom = parseFloat(main.style.paddingBottom) || 0;

      if (Math.abs(footerHeight - currentBottom) > 1) {
        main.style.paddingBottom = footerHeight + 'px';
      }
    } else {
      // If footer is NOT fixed, reset padding to avoid huge gaps
      main.style.paddingBottom = '0px';
    }
  }
}

// Run on load and resize
let resizeTimer;

window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(adjustLayout, 100);
});

// Run immediately to prevent FOUC (layout shift) on first paint
adjustLayout();

document.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector('header');

  if (header && 'ResizeObserver' in window) {
    const observer = new ResizeObserver(adjustLayout);
    observer.observe(header);
  }

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
    const prediction = document.querySelector(".prediction");
    if (prediction) {
      prediction.textContent = "";
    }
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

  if (!menu || !hamburger) return;

  if (
    menu.classList.contains('active') &&
    !menu.contains(event.target) &&
    !hamburger.contains(event.target)
  ) {
    menu.classList.remove('active');
    document.body.classList.remove('no-scroll');
  }
});