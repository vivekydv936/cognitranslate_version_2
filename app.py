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
    "Arabic", "Chinese (Simplified)", "Czech", "Dutch", "English",
    "French", "German", "Hindi", "Hungarian", "Italian", "Japanese",
    "Korean", "Polish", "Portuguese", "Russian", "Spanish", "Turkish"
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
import base64
import json
import uuid
import os

# Auto-accept Coqui TTS license (required for headless/Docker environments)
os.environ["COQUI_TOS_AGREED"] = "1"

from TTS.api import TTS

# Initialize Coqui TTS
# Based on your working example: tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
# We will try to use GPU if available, else CPU, but using the exact model path you verified.
print("⏳ Loading Coqui TTS Model...")
try:
    # Try GPU first
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
    print("✅ Coqui TTS Model Loaded on GPU!")
except Exception as e:
    print(f"⚠️ GPU Load failed: {e}. Falling back to CPU (gpu=False) as per your test.")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    print("✅ Coqui TTS Model Loaded on CPU.")

@app.route('/translate_audio', methods=['POST'])
def translate_audio():
    if not model:
        return {"error": "Gemini Model not configured"}, 500

    audio_file = request.files.get('audio_data')
    target_language = request.form.get('target_language')
    
    if not audio_file:
        return {"error": "No audio file provided"}, 400

    try:
        # 1. Speech-to-Text (STT) using Gemini
        audio_bytes = audio_file.read()
        
        stt_prompt = "Transcribe the following audio exactly as spoken. Return only the text."
        
        response = model.generate_content([
            stt_prompt,
            {
                "mime_type": "audio/webm",
                "data": audio_bytes
            }
        ])
        
        # Handle empty/blocked response
        if not response.candidates or not response.candidates[0].content.parts:
            print("⚠️ Gemini STT returned empty response (audio may be unclear or too noisy)")
            return {"error": "Could not transcribe audio. Please speak clearly and try again."}, 400
        
        original_text = response.text.strip()
        if not original_text:
            return {"error": "No speech detected. Please try again."}, 400
        print(f"Transcribed Text: {original_text}")

        # 2. Translate Text
        translation_prompt = f"""Translate the following text to {target_language}. Only return the final translated text. Text: "{original_text}" """
        translation_response = model.generate_content(translation_prompt)
        
        if not translation_response.candidates or not translation_response.candidates[0].content.parts:
            return {"error": "Translation failed. Please try again."}, 400
        
        translated_text = translation_response.text.strip()
        print(f"Translated Text: {translated_text}")

        # 3. Local Voice Cloning (Coqui TTS)
        # Save the user's audio to a temp file for cloning
        input_audio_path = f"temp_input_{uuid.uuid4()}.webm"
        cloning_source_path = f"temp_source_{uuid.uuid4()}.wav"
        
        with open(input_audio_path, "wb") as f:
            f.write(audio_bytes)
        
        # Check if audio file has actual content
        file_size = os.path.getsize(input_audio_path)
        print(f"📦 Audio file size: {file_size} bytes")
        if file_size < 1000:
            return {"error": "Recording too short or microphone not capturing audio. Please check your mic and try again."}, 400

        # Explicitly convert to WAV using FFmpeg to ensure compatibility
        import subprocess
        import shutil

        if not shutil.which("ffmpeg"):
            print("❌ ERROR: FFmpeg not found in PATH. Please install FFmpeg correctly.")
            return {"error": "FFmpeg not found on server"}, 500

        try:
            # Convert WebM to WAV (16kHz, mono is usually best for TTS)
            command = [
                "ffmpeg", "-y", "-i", input_audio_path, 
                "-vn", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "22050", 
                cloning_source_path
            ]
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            wav_size = os.path.getsize(cloning_source_path)
            print(f"✅ Converted audio to WAV: {cloning_source_path} ({wav_size} bytes)")
            if wav_size < 1000:
                print("⚠️ WAV file is too small - audio may be silent")
                return {"error": "Audio appears to be silent. Please speak clearly into your microphone."}, 400
        except Exception as e:
            print(f"❌ FFmpeg conversion failed: {e}")
            return {"error": "Failed to process audio format"}, 500
        
        output_filename = f"output_{uuid.uuid4()}.wav"
        
        # Map full language names to codes (XTTS supports specific codes)
        # XTTS v2 supports: en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko
        lang_map = {
            "English": "en", "Spanish": "es", "French": "fr", "German": "de", 
            "Italian": "it", "Portuguese": "pt", "Polish": "pl", "Turkish": "tr", 
            "Russian": "ru", "Dutch": "nl", "Czech": "cs", "Arabic": "ar", 
            "Chinese (Simplified)": "zh-cn", "Japanese": "ja", "Hungarian": "hu", 
            "Korean": "ko", "Hindi": "hi"
        }
        
        target_lang_code = lang_map.get(target_language, "en") # Default to English if not found

        print(f"🎙️ Generating Audio in {target_lang_code}...")
        
        tts.tts_to_file(
            text=translated_text,
            speaker_wav=cloning_source_path, # Use the clean WAV file
            language=target_lang_code,
            file_path=output_filename
        )
        
        # Read the generated audio
        with open(output_filename, "rb") as f:
            generated_audio_bytes = f.read()
            
        audio_base64 = base64.b64encode(generated_audio_bytes).decode('utf-8')

        # Cleanup temp files
        try:
            os.remove(input_audio_path)
            os.remove(cloning_source_path)
            os.remove(output_filename)
        except:
            pass

        # Update Session History
        if 'history' not in session:
            session['history'] = []
        
        history_item = {
            'original': original_text, 'translation': translated_text,
            'source': 'Voice (Local)', 'target': target_language
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
