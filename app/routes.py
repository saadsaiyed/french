import logging
from flask import Flask, Blueprint, render_template, request, jsonify, send_file, session
import random
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import speech_recognition as sr
from os import getenv
from dotenv import load_dotenv
from mistralai import Mistral  # Assuming Mistral is installed
import time
import requests
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_random_number():
    number = random.randint(0, 99999)
    logging.debug(f"Generated random number: {number}")
    return number

def number_to_french(number):
    translator = GoogleTranslator(source='en', target='fr')
    translated = translator.translate(str(number))
    logging.debug(f"Translated number {number} to French: {translated}")
    return translated

app = Flask(__name__)
bp = Blueprint('routes', __name__)

# Route for the home page
@bp.route('/')
def index():
    logging.info("Rendering home page")
    return render_template('index.html')

# Route for the Numbers Section
@bp.route('/game', methods=['GET'])
def game():
    logging.info("Rendering Numbers Section")
    session['score'] = 0
    session['round'] = 1
    return render_template('game.html')

# Route to generate a random number and its French audio
@bp.route('/generate_number', methods=['POST'])
def generate_number():
    number = generate_random_number()
    french = number_to_french(number)
    audio_file = f"temp_{number}.mp3"
    tts = gTTS(french, lang='fr')
    audio_dir = os.path.join('app', 'static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    tts.save(os.path.join(audio_dir, audio_file))
    logging.debug(f"Generated audio file for number {number}: {audio_file}")

    session['current_number'] = number
    return jsonify({'number': number, 'audio_file': f"/static/audio/{audio_file}"})

# Route for the AI Practice Section
@bp.route('/ai_practice', methods=['GET'])
def ai_practice():
    logging.info("Rendering AI Practice Section")
    return render_template('ai_practice.html')

# Route to handle AI conversation
@bp.route('/ai_conversation', methods=['POST'])
def ai_conversation():
    user_text = request.json.get('user_text')
    logging.debug(f"Received user text for AI conversation: {user_text}")
    load_dotenv()
    
    model = "mistral-large-latest"
    client = Mistral(api_key=getenv('MISTRAL_API_KEY'))

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_text,
            },
        ]
    )
    ai_response = chat_response.choices[0].message.content
    logging.debug(f"AI response: {ai_response}")

    audio_file = "ai_response.mp3"
    tts = gTTS(ai_response, lang='fr')
    audio_dir = os.path.join('app', 'static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    tts.save(os.path.join(audio_dir, audio_file))
    logging.debug(f"Generated audio file for AI response: {audio_file}")

    return jsonify({'response': ai_response, 'audio_file': f"/static/audio/{audio_file}"})

# Route to handle audio-to-text conversion
@bp.route('/audio_to_text', methods=['POST'])
def audio_to_text():
    audio_file = request.files['audio']
    logging.debug(f"Received audio file for transcription: {audio_file.filename}")
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        user_text = recognizer.recognize_google(audio_data, language='fr-FR')
    logging.debug(f"Transcribed audio to text: {user_text}")

    return jsonify({'user_text': user_text})

# Route to serve audio files
@bp.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='audio/mpeg')
    return jsonify({'error': 'File not found'}), 404

# Route to check the user's answer
@bp.route('/check_answer', methods=['POST'])
def check_answer():
    user_input = request.json.get('user_input')
    correct_number = session.get('current_number')

    if user_input == str(correct_number):
        session['score'] += 1
        return jsonify({'result': 'correct', 'score': session['score']})
    else:
        return jsonify({'result': 'incorrect', 'score': session['score']})

# Cleanup route to delete temporary audio files
@bp.route('/cleanup', methods=['POST'])
def cleanup():
    for file in os.listdir():
        if file.startswith("temp_") and file.endswith(".mp3"):
            os.remove(file)
    return jsonify({'status': 'cleaned'})

# Route for the Translation Practice Section
@bp.route('/translation_practice', methods=['GET'])
def translation_practice():
    return render_template('translation_practice.html')

# Route to generate a sentence/question for translation practice
@bp.route('/generate_translation', methods=['POST'])
def generate_translation():
    grammar = request.json.get('grammar')
    logging.debug(f"Grammar selected for translation practice: {grammar}")
    load_dotenv()
    api_key = getenv('MISTRAL_API_KEY')
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)
    prompt = f"Generate a single question in French using the grammar: {grammar}. The response should be a single sentence in french and nothing else."
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    french_sentence = chat_response.choices[0].message.content.strip()
    logging.debug(f"Generated French sentence: {french_sentence}")

    audio_file = "translation_practice.mp3"
    tts = gTTS(french_sentence, lang='fr')
    audio_dir = os.path.join('app', 'static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    tts.save(os.path.join(audio_dir, audio_file))
    logging.debug(f"Generated audio file for translation practice: {audio_file}")

    return jsonify({'french_sentence': french_sentence, 'audio_file': f"/static/audio/{audio_file}"})

# Route to check the user's translation
@bp.route('/check_translation', methods=['POST'])
def check_translation():
    user_translation = request.json.get('user_translation')
    correct_translation = request.json.get('correct_translation')
    logging.debug(f"User translation: {user_translation}")
    logging.debug(f"Correct translation: {correct_translation}")

    translator = GoogleTranslator(source='fr', target='en')
    correct_translation_in_english = translator.translate(correct_translation)
    logging.debug(f"Correct translation in English: {correct_translation_in_english}")

    if user_translation.strip().lower() == correct_translation_in_english.strip().lower():
        logging.info("User translation is correct")
        return jsonify({'result': 'correct'})
    else:
        logging.info("User translation is incorrect")
        return jsonify({
            'result': 'incorrect',
            'correct_translation': correct_translation_in_english
        })

# Eleven Labs API configuration
ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')
# ELEVEN_LABS_VOICE_ID = "IPgYtHTNLjC7Bq7IPHrm"  # Replace with your Eleven Labs voice ID
ELEVEN_LABS_VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"  # Replace with your Eleven Labs voice ID

# Route for Listening Practice Section
@bp.route('/listening_practice', methods=['GET'])
def listening_practice():
    return render_template('listening_practice.html')

# Route to process English sentences and generate French audio
@bp.route('/generate_listening_audio', methods=['POST'])
def generate_listening_audio():
    sentences = request.json.get('sentences', [])
    enable_translation = request.json.get('enable_translation')  # Default to True
    audio_files = []

    for sentence in sentences:
        if enable_translation:
            # Translate English to French
            translator = GoogleTranslator(source='en', target='fr')
            french_sentence = translator.translate(sentence)
        else:
            # Use the input sentence directly as the French sentence
            sentences = GoogleTranslator(source='fr', target='en').translate(sentence)
            french_sentence = sentence

        # Generate audio using Eleven Labs API
        timestamp = int(time.time())
        audio_file = f"listening_{timestamp}.mp3"
        audio_dir = os.path.join('app', 'static', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        audio_path = os.path.join(audio_dir, audio_file)

        logging.debug(f"Generating audio for sentence: {french_sentence}")
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_LABS_VOICE_ID}",
            headers={
                "Content-Type": "application/json",
                "xi-api-key": ELEVEN_LABS_API_KEY,
            },
            json={
                "text": french_sentence,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"speed": 0.8},
            },
        )
        if response.status_code == 200:
            with open(audio_path, "wb") as f:
                f.write(response.content)
            # Save metadata as JSON
            metadata_file = audio_path.replace(".mp3", ".json")
            with open(metadata_file, "w") as f:
                json.dump({"english": sentence, "french": french_sentence}, f)

            audio_files.append({"sentence": sentence, "french": french_sentence, "audio_file": f"/static/audio/{audio_file}"})
        else:
            logging.error(f"Failed to generate audio: {response.status_code} - {response.text}")
            return jsonify({"error": "Failed to generate audio"}), 500

    return jsonify(audio_files)

# Route to get saved listening data
@bp.route('/get_saved_listening_data', methods=['GET'])
def get_saved_listening_data():
    audio_dir = os.path.join('app', 'static', 'audio')
    saved_data = []

    if os.path.exists(audio_dir):
        for file_name in os.listdir(audio_dir):
            if file_name.startswith("listening_") and file_name.endswith(".mp3"):
                # Extract the English and French sentences from the file name
                file_path = os.path.join(audio_dir, file_name)
                json_file_path = file_path.replace(".mp3", ".json")

                if os.path.exists(json_file_path):  # Check if the .json file exists
                    with open(json_file_path, "r") as f:
                        sentence_data = json.load(f)
                    saved_data.append({
                        "english": sentence_data["english"],
                        "french": sentence_data["french"],
                        "audio_file": f"/static/audio/{file_name}"
                    })
                else:
                    logging.warning(f"Metadata file missing for audio: {file_name}")

    return jsonify(saved_data)

# Cleanup route to remove orphaned audio files
@bp.route('/cleanup_audio', methods=['POST'])
def cleanup_audio():
    audio_dir = os.path.join('app', 'static', 'audio')
    if os.path.exists(audio_dir):
        for file_name in os.listdir(audio_dir):
            if file_name.endswith(".mp3"):
                json_file_path = os.path.join(audio_dir, file_name.replace(".mp3", ".json"))
                if not os.path.exists(json_file_path):
                    os.remove(os.path.join(audio_dir, file_name))
                    logging.info(f"Removed orphaned audio file: {file_name}")
    return jsonify({"status": "cleanup complete"})

app.register_blueprint(bp)