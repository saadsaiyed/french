document.addEventListener('DOMContentLoaded', function () {
    const sentencesInput = document.getElementById('sentences-input');
    const generateButton = document.getElementById('generate-button');
    const audioList = document.getElementById('audio-list');
    const savedAudioList = document.getElementById('saved-audio-list');

    // Fetch and display saved sentences and audio files
    function loadSavedAudio() {
        fetch('/get_saved_listening_data')
            .then(response => response.json())
            .then(data => {
                savedAudioList.innerHTML = '';
                data.forEach(item => {
                    const audioItem = document.createElement('div');
                    audioItem.innerHTML = `
                        <p><strong>English:</strong> ${item.english}</p>
                        <p><strong>French:</strong> ${item.french}</p>
                        <audio controls loop>
                            <source src="${item.audio_file}" type="audio/mpeg">
                            Your browser does not support the audio element.
                        </audio>
                    `;
                    savedAudioList.appendChild(audioItem);
                });
            })
            .catch(error => {
                console.error('Error fetching saved audio:', error);
            });
    }

    generateButton.addEventListener('click', function () {
        const sentences = sentencesInput.value.trim().split('\n').filter(sentence => sentence);

        fetch('/generate_listening_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sentences }),
        })
        .then(response => response.json())
        .then(data => {
            audioList.innerHTML = '';
            data.forEach(item => {
                const audioItem = document.createElement('div');
                audioItem.innerHTML = `
                    <p><strong>English:</strong> ${item.sentence}</p>
                    <p><strong>French:</strong> ${item.french}</p>
                    <audio controls loop>
                        <source src="${item.audio_file}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                `;
                audioList.appendChild(audioItem);
            });

            // Reload saved audio after generating new ones
            loadSavedAudio();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Load saved audio on page load
    loadSavedAudio();
});