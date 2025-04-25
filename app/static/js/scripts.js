document.addEventListener('DOMContentLoaded', function () {
    const audioElement = document.getElementById('audio');
    const userInput = document.getElementById('user-input');
    const feedback = document.getElementById('feedback');
    const scoreDisplay = document.getElementById('score');
    let currentNumber;

    function generateNumber() {
        fetch('/generate_number', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            currentNumber = data.number;
            audioElement.src = data.audio_file;
            audioElement.play();
        });
    }

    document.getElementById('submit-button').addEventListener('click', function () {
        const userAnswer = userInput.value.trim();
        fetch('/check_answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userAnswer }),
        })
        .then(response => response.json())
        .then(data => {
            feedback.textContent = data.result === 'correct' ? '✅ Correct!' : '❌ Incorrect!';
            scoreDisplay.textContent = `Score: ${data.score}`;
            if (data.result === 'correct') {
                generateNumber();
                userInput.value = '';
                userInput.focus();
            }
        });
    });

    document.getElementById('reveal-button').addEventListener('click', function () {
        feedback.textContent = `The correct number is: ${currentNumber}`;
    });

    generateNumber();
    audioElement.play();

});