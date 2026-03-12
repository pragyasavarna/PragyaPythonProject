function typeWriter(elementId, text, speed = 20, callback = null) {
    let i = 0;
    const element = document.getElementById(elementId);
    element.innerHTML = "";
    function typing() {
        if (i < text.length) {
            const char = text.charAt(i);
            if (char === " ") {
                element.innerHTML += "&nbsp;";
            } else if (char === "\n") {
                element.innerHTML += "<br>";
            } else {
                element.innerHTML += char;
            }
            i++;
            setTimeout(typing, speed);
        } else {
            if (callback) callback();
        }
    }
    typing();
}

function summarizeNotes() {
    let text = document.getElementById("inputText").value;
    if (text.trim() === "") {
        alert("Please enter some text");
        return;
    }
    // Clear previous output
    document.getElementById("summaryResult").innerText = "";
    document.getElementById("bulletResult").innerText = "";
    document.getElementById("keywordResult").innerHTML = "";

    // Hide titles initially
    document.getElementById("summaryTitle").style.display = "none";
    document.getElementById("bulletTitle").style.display = "none";
    document.getElementById("keywordTitle").style.display = "none";

    // Show loader
    document.getElementById("loader").style.display = "block";
    fetch("/summarize-text/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Server error: " + response.status);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("loader").style.display = "none";
            // Summary typing
            let formattedSummary = data.summary.replace(/\.\s+/g, ".\n");
            // Show Summary heading
            document.getElementById("summaryTitle").style.display = "block";
            typeWriter("summaryResult", formattedSummary, 15, () => {
                // Bullet typing after summary finishes
                // Show Bullet heading
                document.getElementById("bulletTitle").style.display = "block";
                typeWriter("bulletResult", data.bullets, 10, () => {
                    // Keywords animation
                    // Show Keyword heading
                    document.getElementById("keywordTitle").style.display = "block";
                    const keywordContainer = document.getElementById("keywordResult");
                    if (data.keywords) {
                        data.keywords.forEach((k, index) => {
                            setTimeout(() => {
                                const tag = document.createElement("span");
                                tag.className = "keyword-tag";
                                tag.innerText = k;
                                keywordContainer.appendChild(tag);
                            }, index * 150);
                        });
                    }
                });
            });
        })
        .catch(error => {
            console.error(error);
            document.getElementById("loader").style.display = "none";
            alert("Something went wrong while generating summary.");
        });
} 