function outf(text) {
    const outputBox = document.getElementById("outputBox");
    outputBox.innerHTML += text;
}

function builtinRead(x) {
    if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined) {
        throw "File not found: '" + x + "'";
    }
    return Sk.builtinFiles["files"][x];
}

function cleanIndentation(code) {
    const lines = code.split("\n");

    // Remove ONLY leading blank lines
    while (lines.length && lines[0].trim() === "") {
        lines.shift();
    }

    if (lines.length === 0) return "";

    // Detect minimum indentation of real code
    const indents = lines
        .filter(line => line.trim() !== "")
        .map(line => line.match(/^\s*/)[0].length);

    const minIndent = Math.min(...indents);

    // Remove only that minimum indent
    const cleaned = lines.map(line => line.slice(minIndent)).join("\n");

    return cleaned;
}
// ========== INPUT HANDLER FOR input() ==========
let inputResolve = null;

function inputHandler(prompt) {
    // Show input area
    document.getElementById("inputArea").style.display = "flex";
    outf(prompt);  // print prompt inside output box
    return new Promise((resolve) => {
        inputResolve = resolve;
    });
}

// expose globally (important)
window.inputHandler = inputHandler;

// Submit Input button
document.getElementById("submitInputBtn").addEventListener("click", function () {
    if (inputResolve) {
        const val = document.getElementById("userInput").value;
        document.getElementById("userInput").value = "";
        // Hide input area after submitting
        document.getElementById("inputArea").style.display = "none";
        inputResolve(val);
        inputResolve = null;
    }
});

document.getElementById("runCodeBtn").addEventListener("click", function () {
    let editor = document.getElementById("codeEditor");
    let code = editor.value;

    // Clean indentation (remove leading spaces)
    let cleaned = cleanIndentation(code);

    editor.value = cleaned;

    let outputBox = document.getElementById("outputBox");
    outputBox.innerHTML = ""; // Clear previous output

    Sk.configure({
        output: outf,
        read: builtinRead,
        inputfun: window.inputHandler,  // <-- added
        inputfunTakesPrompt: true
    });

    Sk.misceval.asyncToPromise(() => {
        return Sk.importMainWithBody("<stdin>", false, cleaned, true);
    })
        .then(() => {
            saveExecution(cleaned, outputBox.innerText);
        })
        .catch(err => {
            outputBox.innerHTML = err.toString();
            saveExecution(cleaned, err.toString());
        });
});


function saveExecution(inputCode, outputText) {
    let formData = new FormData();
    formData.append("code_input", inputCode);
    formData.append("code_output", outputText);

    fetch("/save-execution/", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => console.log("Saved:", data))
        .catch(err => console.error("Save error:", err));
}
