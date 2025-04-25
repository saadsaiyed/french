document.addEventListener('DOMContentLoaded', function () {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const aiResponse = document.getElementById('ai-response');
    const aiAudio = document.getElementById('ai-audio');

    sendButton.addEventListener('click', function () {
        const userText = userInput.value.trim();
        if (!userText) return;

        fetch('/ai_conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_text: userText }),
        })
        .then(response => response.json())
        .then(data => {
            aiResponse.textContent = data.response;
            aiAudio.src = data.audio_file;
            aiAudio.play();
        });
    });
});