const output = document.getElementById("output");
const btn = document.getElementById("record_btn");

// Browser support check
const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
    output.innerText = "❌ Speech Recognition not supported in this browser";
} else {
    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;

    btn.onclick = () => {
        output.innerText = "🎙 Listening...";
        recognition.start();
    };

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        output.innerText = "🗣 You said: " + text;

        // Send text to Django
        fetch("/process-text/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        })
            .then(res => res.json())
            .then(data => {
                if (data.reply) {
                    output.innerText += "\n🤖 AI: " + data.reply;
                }
            });
    };

    recognition.onerror = (e) => {
        output.innerText = "❌ Error: " + e.error;
    };
}

