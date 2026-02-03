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
        read: builtinRead
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


// =======================================
//   SAVE EXECUTION TO DATABASE (POST)
// =======================================
function saveExecution(inputCode, outputText) {
    fetch("/save-execution/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `code_input=${encodeURIComponent(inputCode)}&code_output=${encodeURIComponent(outputText)}`
    })
        .then(res => res.json())
        .then(data => {
            console.log("Saved:", data);
        })
        .catch(err => {
            console.error("Save error:", err);
        });
}



// =======================================
//        CSRF TOKEN FETCHER
// =======================================
function getCSRFToken() {
    let name = "csrftoken=";
    let decodedCookies = decodeURIComponent(document.cookie).split(";");

    for (let cookie of decodedCookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name)) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
}
