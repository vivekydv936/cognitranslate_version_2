CogniTranslate 🤖✨
The soul of translation.
CogniTranslate is a modern, feature-rich translation service powered by Google's Gemini generative AI. It was built to demonstrate the practical application of Large Language Models (LLMs) in creating intelligent, beautiful, and user-friendly tools. The application features a stunning, animated user interface and a suite of advanced functionalities that go far beyond basic translation.

Live Demo: https://cognitranslate-app.vercel.app/

<img width="795" height="1030" alt="Image" src="https://github.com/user-attachments/assets/d92492fa-0cc0-4572-baef-b6fcba49e3dd" />

<img width="731" height="1036" alt="Image" src="https://github.com/user-attachments/assets/b34e1b0d-ca42-4ec4-803d-a3e7eb83c8f6" />

✨ Features
CogniTranslate is packed with advanced features designed for a seamless and intuitive user experience:-

🧠 AI-Powered Translations: Leverages the Gemini 1.5 Flash model for high-quality, nuanced translations that understand context and tone.

🎙️ Voice-to-Text Input: Speak directly into the app using the integrated Web Speech API. The microphone button provides clear visual feedback when listening.

🔍 Automatic Language Detection: No need to specify the source language. The application intelligently detects the input language and translates from it automatically.

📜 Translation History: Your five most recent translations are saved to your session and displayed in a clean history list for easy reference.

📋 Copy to Clipboard: A convenient one-click button to copy the translated text, with a tooltip for confirmation.

🎨 Animated & Responsive UI: A beautiful, "living" interface with a gently shifting gradient background, floating shapes for depth, and smooth, fluid animations on all interactive elements.

⚙️ Dynamic & Scalable: The language lists are dynamically populated from the backend, making it easy to add more languages in the future.

🛠️ Technology Stack
The project is built with a modern, robust technology stack:

Backend: Python 3, Flask (for routing and session management).

Frontend: HTML5, JavaScript, Custom CSS (for advanced animations and styling).

AI Service: Google Gemini API.

Speech Recognition: Web Speech API (browser-native).

Version Control: Git & GitHub.

Deployment: Vercel.

🚀 Getting Started
To run this project on your local machine, follow these steps:

Prerequisites
Python 3.x installed on your system.

A Google AI API Key. You can get one from Google AI Studio.

Installation & Setup
Clone the repository:

git clone [https://github.com/vivekydv936/cognitranslate-app.git](https://github.com/vivekydv936/cognitranslate-app.git)
cd cognitranslate-app

Create and activate a virtual environment (recommended):

python -m venv venv
# On Windows:
.\venv\Scripts\Activate
# On macOS/Linux:
source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Configuration
Open the app.py file and find the line API_KEY = "YOUR_API_KEY_HERE". Replace the placeholder with your actual Google AI API key.

Note: For a production deployment, it is critical to use environment variables instead of hardcoding the key.

Running the Application
With the dependencies installed and the API key configured, you can start the Flask development server:

python -m flask run

The application will be available at http://127.0.0.1:5000 in your web browser.

☁️ Deployment
This project is configured for easy deployment on Vercel. The vercel.json file contains the necessary build and routing configurations. To deploy, simply import the GitHub repository into Vercel and add your API_KEY as an environment variable in the project settings.
