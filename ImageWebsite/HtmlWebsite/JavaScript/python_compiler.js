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

document.getElementById("runCodeBtn").addEventListener("click", function () {
    let code = document.getElementById("codeEditor").value;
    let outputBox = document.getElementById("outputBox");
    outputBox.innerHTML = ""; // Clear output before running

    Sk.configure({
        output: outf,
        read: builtinRead
    });

    Sk.misceval.asyncToPromise(function () {
        return Sk.importMainWithBody("<stdin>", false, code, true);
    }).catch(function (err) {
        outputBox.innerHTML = err.toString();
    });
});
