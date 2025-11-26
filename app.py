# app.py (version 9 - Final Fix)

import os
from flask import Flask, render_template, request, session, make_response
from dotenv import load_dotenv

# Load environment variables from .env file, if it exists.
load_dotenv() 

# --- Configure the Flask App ---
app = Flask(__name__)
# A secret key is required to use sessions in Flask
app.secret_key = os.urandom(24)

# --- Configure the Gemini API ---
import google.generativeai as genai

API_KEY = os.getenv("GOOGLE_API_KEY")
model = None # Initialize model as None

if not API_KEY:
    print("ERROR: GOOGLE_API_KEY not found in environment variables.")
else:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("Gemini API configured successfully.")
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")

# --- Centralized Language List ---
LANGUAGES = [
    "Arabic", "Bengali", "Chinese (Simplified)", "Dutch", "English",
    "French", "German", "Hindi", "Indonesian", "Italian", "Japanese",
    "Korean", "Polish", "Portuguese", "Russian", "Spanish", "Swedish",
    "Turkish", "Vietnamese"
]

# --- Route to handle favicon.ico requests ---
@app.route('/favicon.ico')
def favicon():
    return make_response('', 204)

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        original_text = request.form.get('text_to_translate')
        target_language = request.form.get('target_language')
        source_language_form = request.form.get('source_language')
        
        translation_result = ""
        detected_language_display = ""
        final_source_language = source_language_form

        try:
            if not model:
                 raise ValueError("AI Model is not configured. Check API Key.")

            if source_language_form == 'Detect Language':
                if original_text and original_text.strip():
                    detection_prompt = f"""Detect the language of the following text. Return only the name of the language. Text: "{original_text}" """
                    detection_response = model.generate_content(detection_prompt)
                    detected_language_name = detection_response.text.strip()
                    final_source_language = detected_language_name
                    detected_language_display = f"Detected: {detected_language_name}"

            if original_text and original_text.strip():
                translation_prompt = f"""Translate the following text from {final_source_language} to {target_language}. Only return the final translated text. Text: "{original_text}" """
                translation_response = model.generate_content(translation_prompt)
                translation_result = translation_response.text.strip()

                history_item = {
                    'original': original_text, 'translation': translation_result,
                    'source': final_source_language, 'target': target_language
                }
                session['history'].insert(0, history_item)
                session['history'] = session['history'][:5]
                session.modified = True
            
        except Exception as e:
            translation_result = f"An error occurred: {e}"

        return render_template('index.html',
                               translation=translation_result, original_text=original_text,
                               selected_target_language=target_language, selected_source_language=source_language_form,
                               detected_language=detected_language_display, history=session['history'],
                               languages=LANGUAGES)
    else:
        # Initial page load
        return render_template('index.html',
                               translation="", original_text="",
                               selected_target_language="Spanish", selected_source_language="Detect Language",
                               detected_language="", history=session['history'],
                               languages=LANGUAGES)

# --- Voice Cloning & Audio Translation Route ---
import requests
import base64
import json

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.route('/translate_audio', methods=['POST'])
def translate_audio():
    if not model:
        return {"error": "Gemini Model not configured"}, 500
    if not ELEVENLABS_API_KEY:
        return {"error": "ElevenLabs API Key not configured"}, 500

    audio_file = request.files.get('audio_data')
    target_language = request.form.get('target_language')
    
    if not audio_file:
        return {"error": "No audio file provided"}, 400

    try:
        # 1. Speech-to-Text (STT) using Gemini
        # We can send the audio bytes directly to Gemini 1.5 Flash
        audio_bytes = audio_file.read()
        
        stt_prompt = "Transcribe the following audio exactly as spoken. Return only the text."
        
        # Prepare the content parts
        # Note: Check if the current SDK version supports inline data for 'audio/wav' or 'audio/mp3'
        # Assuming the frontend sends a blob that we can treat as audio/wav or similar.
        # We'll try to use the standard generate_content with inline data.
        
        response = model.generate_content([
            stt_prompt,
            {
                "mime_type": "audio/mp3", # Assuming MP3 or WAV, Gemini is flexible
                "data": audio_bytes
            }
        ])
        
        original_text = response.text.strip()
        print(f"Transcribed Text: {original_text}")

        # 2. Translate Text
        translation_prompt = f"""Translate the following text to {target_language}. Only return the final translated text. Text: "{original_text}" """
        translation_response = model.generate_content(translation_prompt)
        translated_text = translation_response.text.strip()
        print(f"Translated Text: {translated_text}")

        # 3. Voice Cloning & TTS (ElevenLabs)
        # A. Add Voice
        add_voice_url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        
        # Reset file pointer to read again for ElevenLabs
        audio_file.seek(0)
        
        files = {
            'files': ('sample.mp3', audio_file, 'audio/mpeg'),
            'name': (None, 'Temp User Voice')
        }
        
        voice_response = requests.post(add_voice_url, headers=headers, files=files)
        
        voice_id = ""
        is_cloned = False

        if voice_response.status_code == 200:
            voice_id = voice_response.json()['voice_id']
            is_cloned = True
            print(f"Voice ID (Cloned): {voice_id}")
        else:
             # Fallback: Use a standard pre-made voice (e.g., 'Rachel' - a common default)
             # You can find more IDs in ElevenLabs docs or list them via API
             print(f"Voice Cloning Failed: {voice_response.text}")
             print("Falling back to standard voice.")
             voice_id = "21m00Tcm4TlvDq8ikWAM" # Rachel
             is_cloned = False

        # B. Generate Audio
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        tts_headers = {
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        tts_data = {
            "text": translated_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        audio_response = requests.post(tts_url, headers=tts_headers, json=tts_data)
        
        if audio_response.status_code == 200:
            audio_base64 = base64.b64encode(audio_response.content).decode('utf-8')
        else:
            audio_base64 = None
            print(f"TTS Failed: {audio_response.text}")

        # C. Delete Voice (Cleanup) - Only if we created one
        if is_cloned:
            delete_url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
            requests.delete(delete_url, headers=headers)

        # Update Session History
        if 'history' not in session:
            session['history'] = []
        
        history_item = {
            'original': original_text, 'translation': translated_text,
            'source': 'Voice', 'target': target_language
        }
        session['history'].insert(0, history_item)
        session['history'] = session['history'][:5]
        session.modified = True

        return {
            "original_text": original_text,
            "translation": translated_text,
            "audio_base64": audio_base64
        }

    except Exception as e:
        print(f"Error in translate_audio: {e}")
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
