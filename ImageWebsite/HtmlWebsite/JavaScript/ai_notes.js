function summarizeNotes() {

    let text = document.getElementById("inputText").value;

    if (text.trim() === "") {
        alert("Please enter some text");
        return;
    }

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

        .then(response => response.json())

        .then(data => {

            document.getElementById("summaryResult").innerText = data.summary;

            document.getElementById("bulletResult").innerText = data.bullets;

            let keywordsHTML = "";

            if (data.keywords) {
                data.keywords.forEach(k => {
                    keywordsHTML += `<span class="keyword-tag">${k}</span>`;
                });
            }

            document.getElementById("keywordResult").innerHTML = keywordsHTML;

            document.getElementById("loader").style.display = "none";

        })

        .catch(error => {

            console.error(error);

            document.getElementById("loader").style.display = "none";

        });

}