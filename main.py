# main.py

import os
import google.generativeai as genai

# Load API key from .env file (same as app.py)
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the library with your key
genai.configure(api_key=API_KEY)

# Initialize the generative model
# We are using the 'gemini-1.5-flash' model which is fast and powerful
model = genai.GenerativeModel('gemini-2.5-flash')

# --- Let's define our translation task ---
text_to_translate = "Hello, world! This is a test of my new AI translator."
source_language = "English"
target_language = "French"
context = "a casual conversation"

# This is our "prompt engineering". We give the AI clear instructions.
prompt = f"""
You are an expert translator. Your task is to translate the given text from {source_language} to {target_language}.
Please maintain the original tone and context, which is '{context}'.

Text to translate:
---
{text_to_translate}
---
"""

print("🤖 Sending request to AI... Please wait.")

# Send the prompt to the model to get the translation
response = model.generate_content(prompt)

print("\n Translation Complete!")
print("------------------------")
# The translated text is in the 'text' attribute of the response
print(response.text)
print("------------------------")