document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('run-c-btn');
    const codeEditor = document.getElementById('c-code-editor');
    const outputArea = document.getElementById('c-output');

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