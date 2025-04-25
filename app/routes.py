from flask import Flask, Blueprint, render_template, request, jsonify, send_file, session
import random
from gtts import gTTS
from deep_translator import GoogleTranslator
import os
import speech_recognition as sr
from os import getenv
from dotenv import load_dotenv
from mistralai import Mistral  # Assuming Mistral is installed

def generate_random_number():
    return random.randint(0, 99999)

def number_to_french(number):
    translator = GoogleTranslator(source='en', target='fr')
    translated = translator.translate(str(number))
    return translated

app = Flask(__name__)
bp = Blueprint('routes', __name__)

# Route for the home page
@bp.route('/')
def index():
    return render_template('index.html')

# Route for the Numbers Section
@bp.route('/game', methods=['GET'])
def game():
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

    session['current_number'] = number
    return jsonify({'number': number, 'audio_file': f"/static/audio/{audio_file}"})

# Route for the AI Practice Section
@bp.route('/ai_practice', methods=['GET'])
def ai_practice():
    return render_template('ai_practice.html')

# Route to handle AI conversation
@bp.route('/ai_conversation', methods=['POST'])
def ai_conversation():
    user_text = request.json.get('user_text')
    load_dotenv()
    
    model = "mistral-large-latest"

    # Initialize the Mistral client
    client = Mistral(api_key=getenv('MISTRAL_API_KEY'))

    # Use the correct method to interact with Mistral
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": user_text,
            },
        ]
    )

    # Extract the AI's response
    ai_response = chat_response.choices[0].message.content

    # Convert AI response to audio
    audio_file = "ai_response.mp3"
    tts = gTTS(ai_response, lang='fr')
    audio_dir = os.path.join('app', 'static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    tts.save(os.path.join(audio_dir, audio_file))

    return jsonify({'response': ai_response, 'audio_file': f"/static/audio/{audio_file}"})

# Route to handle audio-to-text conversion
@bp.route('/audio_to_text', methods=['POST'])
def audio_to_text():
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        user_text = recognizer.recognize_google(audio_data, language='fr-FR')

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
    grammar = request.json.get('grammar')  # Grammar selected by the user
    load_dotenv()
    api_key = getenv('MISTRAL_API_KEY')
    model = "mistral-large-latest"

    # Initialize the Mistral client
    client = Mistral(api_key=api_key)

    # Generate a sentence/question based on the selected grammar
    prompt = f"Generate a simple sentence or question in French using the grammar: {grammar}. Keep it beginner-friendly."
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

    # Convert the French sentence to audio
    audio_file = "translation_practice.mp3"
    tts = gTTS(french_sentence, lang='fr')
    audio_dir = os.path.join('app', 'static', 'audio')
    os.makedirs(audio_dir, exist_ok=True)
    tts.save(os.path.join(audio_dir, audio_file))

    return jsonify({'french_sentence': french_sentence, 'audio_file': f"/static/audio/{audio_file}"})

# Route to check the user's translation
@bp.route('/check_translation', methods=['POST'])
def check_translation():
    user_translation = request.json.get('user_translation')
    correct_translation = request.json.get('correct_translation')

    # Use Google Translator to check the translation
    translator = GoogleTranslator(source='fr', target='en')
    correct_translation_in_english = translator.translate(correct_translation)

    if user_translation.strip().lower() == correct_translation_in_english.strip().lower():
        return jsonify({'result': 'correct'})
    else:
        return jsonify({
            'result': 'incorrect',
            'correct_translation': correct_translation_in_english
        })

app.register_blueprint(bp)