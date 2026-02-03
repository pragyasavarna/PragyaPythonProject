let skOutput = "";  // Holds output for THIS execution only

function outf(text) {
    skOutput += text;                       // collect output
    document.getElementById("outputBox").innerText += text;  // show output live
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
    let code = cleanIndentation(editor.value);
    editor.value = code;

    let outputBox = document.getElementById("outputBox");
    outputBox.innerText = "";   // clear old output
    skOutput = "";              // reset collected output

    Sk.configure({
        output: outf,
        read: builtinRead
    });

    Sk.misceval.asyncToPromise(() => {
        return Sk.importMainWithBody("<stdin>", false, code, true);
    })
        .then(() => {
            saveExecution(code, skOutput.trim());
        })
        .catch(err => {
            skOutput = err.toString();
            outputBox.innerText = skOutput;
            saveExecution(code, skOutput);
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
