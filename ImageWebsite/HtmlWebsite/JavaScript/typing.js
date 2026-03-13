document.addEventListener("DOMContentLoaded", function () {
    const elements = document.querySelectorAll("#home h2, #home h3, #home p, #home li, #home .tech span");
    let currentElementIndex = 0;

    function typeHTML(element, speed, callback) {
        // Reveal the parent background containers just before typing starts
        const parentSection = element.closest('.section');
        const parentCard = element.closest('.project-card');
        const parentTech = element.closest('.tech');

        if (parentSection) parentSection.style.opacity = '1';
        if (parentCard) parentCard.style.opacity = '1';
        if (parentTech) parentTech.style.opacity = '1';

        let html = element.innerHTML.trim();
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