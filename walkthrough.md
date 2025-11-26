# Verification: Voice Cloning Feature

## Prerequisite
Ensure your `.env` file has valid keys:
```env
GOOGLE_API_KEY=...
ELEVENLABS_API_KEY=...
```

## Manual Test Steps

1.  **Start the Application**:
    Run the following command in your terminal:
    ```bash
    python app.py
    ```

2.  **Open in Browser**:
    Navigate to `http://127.0.0.1:5000`.

3.  **Test Voice Cloning**:
    -   Select a **Target Language** (e.g., Spanish).
    -   Click the **Microphone Icon**.
    -   **Speak** a sentence clearly (e.g., "Hello, this is a test of my AI voice.").
    -   Click the **Microphone Icon** again to stop recording.

4.  **Verify Results**:
    -   **Status**: The text area should show "Uploading and Cloning Voice...".
    -   **Transcription**: Your spoken text should appear in the input box.
    -   **Translation**: The translated text should appear below.
    -   **Audio**: An audio player should appear. Click **Play**.
    -   **Success Criteria**: The audio should speak the *translated text*.
        -   *Note*: If you are on the ElevenLabs Free Tier, it may use a standard high-quality voice ("Rachel") instead of your exact clone. This is normal behavior.

## Troubleshooting
-   **"Microphone access denied"**: Allow microphone permissions in your browser.
-   **"Voice cloning failed"**: Check your ElevenLabs API key. If on Free Tier, the app will automatically fallback to a standard voice.
-   **No Audio**: Check your computer volume.
