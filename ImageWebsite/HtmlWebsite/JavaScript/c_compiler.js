document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('run-c-btn');
    const codeEditor = document.getElementById('c-code-editor');
    const outputArea = document.getElementById('c-output');

    // ==========================================
    // MODAL WARNING LOGIC (Theme Matched)
    // ==========================================
    const modal = document.getElementById("comingSoonModal");
    const modalText = document.getElementById("modalMessageText");

    function showCustomModal(message) {
        modalText.innerText = message;
        modal.classList.add("show");

        setTimeout(() => {
            modal.classList.remove("show");
        }, 2000); // Auto-close after 2 seconds
    }

    // Click anywhere on backdrop to close early
    modal.addEventListener("click", () => {
        modal.classList.remove("show");
    });

    // ==========================================
    // BULLETPROOF ANTI-PASTE (Desktop & Mobile)
    // ==========================================

    function blockAction(e, message) {
        e.preventDefault();
        codeEditor.blur();
        showCustomModal(message);
    }

    // 1. Block Standard Desktop Actions
    codeEditor.addEventListener('copy', (e) => blockAction(e, "No copying allowed! Focus on building your own logic. 🧠✨"));
    codeEditor.addEventListener('cut', (e) => blockAction(e, "No cutting corners! Use backspace to edit your code. ✂️🚫"));
    codeEditor.addEventListener('paste', (e) => blockAction(e, "No shortcuts! Typing the code manually builds muscle memory. 💻🔥"));

    // 2. Block Mobile Keyboard Injections (Gboard, SwiftKey, etc.)
    codeEditor.addEventListener('beforeinput', function (e) {
        if (e.inputType === 'insertFromPaste' || e.inputType === 'insertFromDrop') {
            blockAction(e, "No shortcuts! Typing the code manually builds muscle memory. 💻🔥");
        }
        // If a mobile keyboard injects a string with new lines, or longer than 15 characters, block it.
        else if (e.inputType === 'insertText' && e.data) {
            if (e.data.includes('\n') || e.data.length > 15) {
                blockAction(e, "No shortcuts! Typing the code manually builds muscle memory. 💻🔥");
            }
        }
    });

    // 3. Ultimate Fallback: The Rollback Mechanism
    // If a keyboard somehow bypasses the above, we detect the sudden jump in text and reverse it.
    let previousValue = codeEditor.value;

    // Keep track of the code state during normal typing and auto-indenting
    codeEditor.addEventListener('keyup', () => previousValue = codeEditor.value);
    codeEditor.addEventListener('keydown', () => setTimeout(() => previousValue = codeEditor.value, 10));

    codeEditor.addEventListener('input', function (e) {
        // Allow users to safely use Undo/Redo without triggering the warning
        if (e.inputType === 'historyUndo' || e.inputType === 'historyRedo') {
            previousValue = codeEditor.value;
            return;
        }

        // If the text suddenly grows by more than 15 characters instantly, it is a paste.
        if (codeEditor.value.length - previousValue.length > 15) {
            codeEditor.value = previousValue; // Roll the text back to exactly what it was before the paste
            codeEditor.blur(); // Hide the keyboard
            showCustomModal("No shortcuts! Typing the code manually builds muscle memory. 💻🔥");
        } else {
            previousValue = codeEditor.value; // Update tracker for normal typing
        }
    });

    // ==========================================
    // AUTO-INDENTATION LOGIC FOR C COMPILER
    // ==========================================
    codeEditor.addEventListener("keydown", function (e) {
        const textarea = this;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const text = textarea.value;

        // 1. Handle "Enter" key for auto-indenting inside blocks
        if (e.key === "Enter") {
            e.preventDefault();

            // Get start of current line
            const lineStart = text.lastIndexOf("\n", start - 1) + 1;
            const currentLine = text.substring(lineStart, start);

            // Count leading spaces of the current line
            const indentMatch = currentLine.match(/^\s*/);
            let newIndent = indentMatch ? indentMatch[0] : "";

            // In C, if the previous line ends with an opening brace '{', add indentation
            if (currentLine.trim().endsWith("{")) {
                newIndent += "    "; // Add 4 spaces
            }

            // Insert new line with correct indentation
            textarea.value =
                text.substring(0, start) +
                "\n" + newIndent +
                text.substring(end);

            // Move cursor correctly
            textarea.selectionStart = textarea.selectionEnd = start + 1 + newIndent.length;
        }

        // 2. Handle "}" key for auto-outdenting closing blocks
        else if (e.key === "}") {
            // Get start of current line
            const lineStart = text.lastIndexOf("\n", start - 1) + 1;
            const currentLine = text.substring(lineStart, start);

            // If the current line leading up to the cursor is ONLY whitespace
            if (/^\s*$/.test(currentLine) && currentLine.length > 0) {
                e.preventDefault();

                // Calculate how many spaces to remove (up to 4)
                const spacesToRemove = currentLine.length % 4 === 0 ? 4 : currentLine.length % 4;
                const newIndent = currentLine.substring(0, currentLine.length - spacesToRemove);

                // Insert the reduced indentation and the closing brace
                textarea.value =
                    text.substring(0, lineStart) +
                    newIndent + "}" +
                    text.substring(end);

                // Move cursor correctly right after the '}'
                textarea.selectionStart = textarea.selectionEnd = lineStart + newIndent.length + 1;
            }
        }
    });

    // ==========================================
    // EXECUTION LOGIC
    // ==========================================
    runBtn.addEventListener('click', async () => {
        const code = codeEditor.value;

        outputArea.value = 'Compiling and running...';
        runBtn.disabled = true;

        try {
            const response = await fetch('/ai-tutor/c-compiler/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ code: code })
            });

            const data = await response.json();
            outputArea.value = data.output;

        } catch (error) {
            outputArea.value = 'Error connecting to the server.';
        } finally {
            runBtn.disabled = false;
        }
    });

    // Helper to retrieve CSRF token from cookies for Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});