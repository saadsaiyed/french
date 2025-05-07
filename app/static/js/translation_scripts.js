document.addEventListener('DOMContentLoaded', function () {
    const grammarSelect = document.getElementById('grammar-select');
    const generateButton = document.getElementById('generate-button');
    const audioElement = document.getElementById('audio');
    const revealButton = document.getElementById('reveal-button');
    const frenchSentenceElement = document.getElementById('french-sentence');
    const userTranslationInput = document.getElementById('user-translation');
    const submitButton = document.getElementById('submit-button');
    const feedbackElement = document.getElementById('feedback');
    let correctTranslation = '';

    generateButton.addEventListener('click', function () {
        console.log('Generate button clicked');
        const grammar = grammarSelect.value;

        fetch('/generate_translation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ grammar }),
        })
        .then(response => response.json())
        .then(data => {
            correctTranslation = data.french_sentence;

            // Append a unique query parameter to the audio file URL
            const uniqueAudioUrl = `${data.audio_file}?t=${new Date().getTime()}`;
            audioElement.src = uniqueAudioUrl;
            audioElement.play();

            frenchSentenceElement.textContent = data.french_sentence;
            frenchSentenceElement.style.display = 'none';
            feedbackElement.textContent = '';
            userTranslationInput.value = '';
        });
    });

    revealButton.addEventListener('click', function () {
        frenchSentenceElement.style.display = 'block';
    });

    submitButton.addEventListener('click', function () {
        console.log('Submit button clicked');
        const userTranslation = userTranslationInput.value.trim();

        fetch('/check_translation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_translation: userTranslation,
                correct_translation: correctTranslation,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.result === 'correct') {
                feedbackElement.textContent = '✅ Correct!';
                feedbackElement.style.color = 'green';
            } else {
                feedbackElement.textContent = `❌ Incorrect! Correct translation: ${data.correct_translation}`;
                feedbackElement.style.color = 'red';
            }
        });
    });
});