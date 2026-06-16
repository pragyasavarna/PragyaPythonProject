document.addEventListener("DOMContentLoaded", function () {
    // 🔥 THE FIX: Just look for the class. No hardcoded HTML tags!
    const elements = document.querySelectorAll(".type-text");
    let currentElementIndex = 0;

    function typeHTML(element, speed, callback) {
        // Dynamically find the parent wrappers and fade them in
        const parentSection = element.closest('section');
        const parentCard = element.closest('.service-card, .project-card, .tech');

        if (parentSection) parentSection.style.opacity = '1';
        if (parentCard) parentCard.style.opacity = '1';

        let html = element.innerHTML.trim();
        
        // 🔥 FIX LAYOUT SHIFT: Lock the element's height before clearing it
        const computedHeight = window.getComputedStyle(element).height;
        if (computedHeight && computedHeight !== 'auto' && computedHeight !== '0px') {
            element.style.minHeight = computedHeight;
        } else {
            const rectHeight = element.getBoundingClientRect().height;
            if (rectHeight > 0) {
                element.style.minHeight = rectHeight + "px";
            }
        }

        element.innerHTML = "";
        element.style.visibility = "visible";
        let i = 0;
        let isTag = false;
        let text = "";

        function type() {
            if (i < html.length) {
                let char = html.charAt(i);
                text += char;

                if (char === '<') isTag = true;
                if (char === '>') isTag = false;

                element.innerHTML = text + (isTag ? "" : "<span class='cursor'>|</span>");
                i++;

                if (isTag) {
                    type();
                } else {
                    setTimeout(type, speed);
                }
            } else {
                element.innerHTML = html;
                if (callback) callback();
            }
        }
        type();
    }

    function processNextElement() {
        if (currentElementIndex < elements.length) {
            typeHTML(elements[currentElementIndex], 5, processNextElement);
            currentElementIndex++;
        }
    }

    processNextElement();
});