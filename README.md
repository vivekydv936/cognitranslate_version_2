

# 🎙️ CogniTranslate - AI Voice Cloning & Translation

**Imagine speaking in English, and hearing yourself instantly speak back in Spanish, Japanese, or Hindi!** 

CogniTranslate is an incredibly cool AI project that does exactly that. It's a web application that listens to your voice, translates what you said into one of 17 languages, and then **clones your voice** to speak the translation out loud!

---

## 💡 Why This Matters 

Imagine a scenario: **A Manager sitting in the UK is on a video call with an Employee in India.** 
If they use standard text subtitles or a robotic AI voice to translate, the *human connection* is completely lost. The employee won't know if the manager is excited, stressed, or serious because standard translation removes all mood and tone.

**CogniTranslate solves this.** Because it clones the speaker's exact vocal characteristics, the manager can speak naturally in English, and the employee will hear the translation in Hindi—but **with the manager's actual voice and tone preserved.** It breaks down language barriers while keeping the emotion intact!

---

## 🧐 How Does it Work? (For Beginners)

When you click the microphone and speak into the app, this is what happens behind the scenes:

1. **Hearing (Speech-to-Text):** The app records your voice and sends it to Google's super-smart AI (**Gemini**). Gemini listens to the audio and turns it into text.
2. **Translating:** Next, Gemini takes that text and translates it into the language you chose (like French or Hindi).
3. **Voice Cloning (Text-to-Speech):** Finally, an amazing open-source AI called **Coqui XTTS v2** kicks in. It takes the translated text and the recording of your voice. It learns what you sound like, and generates a brand new audio clip of "you" speaking the new language!

---

## ✨ Features

- **🗣️ Real-time Voice Cloning:** Hear translations in your exact voice!
- **🌍 17 Supported Languages:** English, Spanish, French, German, Italian, Portuguese, Polish, Turkish, Russian, Dutch, Czech, Arabic, Chinese, Japanese, Hungarian, Korean, and Hindi.
- **⚡ Super Fast (with a GPU):** If you have an NVIDIA Graphics Card (like an RTX series), translations happen in just a few seconds.
- **🎨 Beautiful UI:** A clean, easy-to-use web interface built with HTML and Tailwind CSS.

---

## 🛠️ Technology Stack (What we used)

- **Python & Flask:** The backend engine that runs the server.
- **Google Gemini API:** The brain for understanding and translating text.
- **Coqui XTTS v2:** The AI model that clones your voice.
- **FFmpeg:** A behind-the-scenes tool that converts audio files so the AI can understand them.
- **HTML, JavaScript, Tailwind CSS:** The frontend web page you interact with.

---

## 🚀 How to Run It on Your Computer

If you want to try this out yourself, follow these steps! Don't worry, take it one step at a time.

### Step 1: Get the Prerequisites
1. **Install Python 3.10**: Make sure you have Python 3.10 installed on your computer.
2. **Install FFmpeg**: This is required for handling audio.
   - *Windows shortcut:* Open Terminal/Command Prompt and type: `winget install Gyan.FFmpeg`
   - After installing, **restart your computer** (or terminal) so it recognizes FFmpeg.
3. **Get a Google Gemini API Key**: Go to [Google AI Studio](https://aistudio.google.com/) and grab a free API key.

### Step 2: Download the Code
Open your terminal and download this project:
```bash
git clone https://github.com/vivekydv936/cognitranslate-app.git
cd cognitranslate-app
```

### Step 3: Setup the Environment
It's best to create a "virtual environment" so the project's files don't mess with your computer.
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 4: Install the Libraries
Now, install all the AI brains and tools:
```bash
pip install -r requirements.txt
```
*(Note: Coqui XTTS v2 is a huge AI model. The first time you run the app, it will download about 3GB of data. Be patient!)*

### Step 5: Add Your API Key
Create a file named `.env` in the main folder and add your Gemini key like this:
```
GOOGLE_API_KEY=your_api_key_here
```

### Step 6: Start the App!
Run the Python server:
```bash
python app.py
```
Open your web browser and go to `http://127.0.0.1:5000`. Click the mic, speak, and hear the magic!

---

## ⚠️ Important Note about Hardware
Voice cloning is heavy work for a computer! 
- If you have an **NVIDIA GPU** (like an RTX 4050 or better), it will take about **3-5 seconds**.
- If you only have a **CPU** (standard computer processor), it might take **30-60 seconds** to generate the audio. The code is smart enough to detect what you have and use it automatically!



![alt text](<Screenshot 2026-04-28 003408.png>)
