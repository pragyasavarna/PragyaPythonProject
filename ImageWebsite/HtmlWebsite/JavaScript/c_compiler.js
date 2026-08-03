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
        // Hide keyboard on mobile, keep focus on desktop
        if (window.innerWidth <= 768) {
            codeEditor.blur();
        } else {
            // codeEditor.focus();
        }
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
    // SAVE & LOAD LOGIC
    // ==========================================
    const saveBtn = document.getElementById('btn-save');
    const loadBtn = document.getElementById('btn-load');

    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            if (saveBtn.classList.contains('locked')) {
                showCustomModal("Please login to save your code! 🔒");
                return;
            }

            const originalText = saveBtn.innerText;
            saveBtn.innerText = "Saving...";
            try {
                const response = await fetch('/ai-tutor/save-code/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ code: codeEditor.value })
                });

                if (response.ok) {
                    showCustomModal("Code saved successfully! 💾✨");
                } else {
                    showCustomModal("Error saving code. ❌");
                }
            } catch (error) {
                showCustomModal("Network error connecting to server. ❌");
            } finally {
                saveBtn.innerText = originalText;
            }
        });
    }

    if (loadBtn) {
        loadBtn.addEventListener('click', async () => {
            if (loadBtn.classList.contains('locked')) {
                showCustomModal("Please login to load your code! 🔒");
                return;
            }

            const originalText = loadBtn.innerText;
            loadBtn.innerText = "Loading...";
            try {
                const response = await fetch('/ai-tutor/load-code/');
                if (response.ok) {
                    const data = await response.json();
                    if (data.code) {
                        codeEditor.value = data.code;
                        previousValue = codeEditor.value; // CRITICAL: Updates anti-paste tracker so it doesn't trigger a warning
                        showCustomModal("Saved code loaded! 📂✨");
                    } else {
                        showCustomModal("No saved code found. 📝");
                    }
                } else {
                    showCustomModal("Error loading code. ❌");
                }
            } catch (error) {
                showCustomModal("Network error connecting to server. ❌");
            } finally {
                loadBtn.innerText = originalText;
            }
        });
    }

    // ==========================================
    // CUSTOM JAVASCRIPT UNDO / REDO (Modern Approach)
    // ==========================================
    const undoBtn = document.getElementById('btn-undo');
    const redoBtn = document.getElementById('btn-redo');

    // Create a custom history stack to store the code states
    let codeHistory = [codeEditor.value];
    let historyStep = 0;
    let historyTimeout;

    // Save the editor state whenever the user types (with a slight delay to group keystrokes)
    codeEditor.addEventListener('input', (e) => {
        // Skip saving if the browser is handling native Ctrl+Z / Ctrl+Y
        if (e.inputType === 'historyUndo' || e.inputType === 'historyRedo') return;

        clearTimeout(historyTimeout);
        historyTimeout = setTimeout(() => {
            if (codeHistory[historyStep] !== codeEditor.value) {
                // If they typed something new, erase any "Redo" futures
                codeHistory = codeHistory.slice(0, historyStep + 1);
                codeHistory.push(codeEditor.value);

                // Keep memory clean by only saving the last 50 actions
                if (codeHistory.length > 50) {
                    codeHistory.shift();
                } else {
                    historyStep++;
                }
            }
        }, 400); // Wait 400ms after they stop typing to save the snapshot
    });

    if (undoBtn) {
        undoBtn.addEventListener('click', () => {
            if (historyStep > 0) {
                historyStep--;
                codeEditor.value = codeHistory[historyStep];
                previousValue = codeEditor.value; // CRITICAL: Syncs with your Anti-Paste rule
                // Hide keyboard on mobile, keep focus on desktop
                if (window.innerWidth <= 768) {
                    codeEditor.blur();
                } else {
                    codeEditor.focus();
                }
            }
        });
    }

    if (redoBtn) {
        redoBtn.addEventListener('click', () => {
            if (historyStep < codeHistory.length - 1) {
                historyStep++;
                codeEditor.value = codeHistory[historyStep];
                previousValue = codeEditor.value; // CRITICAL: Syncs with your Anti-Paste rule
                // Hide keyboard on mobile, keep focus on desktop
                if (window.innerWidth <= 768) {
                    codeEditor.blur();
                } else {
                    codeEditor.focus();
                }
            }
        });
    }

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