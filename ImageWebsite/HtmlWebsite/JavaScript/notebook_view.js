document.addEventListener("DOMContentLoaded", function () {
    const iframe = document.getElementById("notebook-iframe");
    const loader = document.getElementById("notebook-loader");

    if (iframe && loader) {
        iframe.addEventListener("load", function () {

            let scrollLock = setInterval(() => {
                window.scrollTo(0, 0);
            }, 10);

            setTimeout(() => {
                clearInterval(scrollLock);

                // --- MOBILE TOUCH SWIPE FIX ---
                try {
                    const iframeDoc = iframe.contentWindow.document;

                    // 1. Strict Viewport (Prevents zoom-breaking)
                    if (!iframeDoc.querySelector('meta[name="viewport"]')) {
                        const meta = iframeDoc.createElement('meta');
                        meta.name = "viewport";
                        meta.content = "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
                        iframeDoc.head.appendChild(meta);
                    }

                    // 2. Inject CSS directly into the Notebook
                    const style = iframeDoc.createElement('style');
                    style.innerHTML = `
                        /* Stop the whole notebook from wobbling left/right */
                        body { 
                            overflow-x: hidden !important; 
                            touch-action: pan-y !important; 
                        }
                        
                        /* Force code blocks to accept horizontal thumb swipes */
                        div.input_area, div.output_subarea, pre, .CodeMirror {
                            overflow-x: auto !important;
                            -webkit-overflow-scrolling: touch !important;
                            touch-action: pan-x pan-y !important; 
                        }
                    `;
                    iframeDoc.head.appendChild(style);

                } catch (e) {
                    console.warn("Could not inject mobile fixes.");
                }
                // --------------------------------

                // Measure height and apply it
                const contentHeight = iframe.contentWindow.document.documentElement.scrollHeight;
                iframe.style.height = (contentHeight + 20) + "px";

                loader.style.display = "none";
                iframe.style.opacity = "1";

            }, 800);
        });
    }
});