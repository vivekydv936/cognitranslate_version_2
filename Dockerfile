# Use Python 3.10
FROM python:3.10-slim

# Install system dependencies (FFmpeg and eSpeak are crucial for TTS)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    espeak-ng \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up work directory
WORKDIR /app

# Copy requirements FIRST (for better caching)
COPY requirements.txt .

# Install Python dependencies
# Note: We use the CPU version of Torch by default for the Free Tier to save size.
# If you have a GPU Instance, change the index-url to 'cu121'
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the rest of the application
COPY . .

# Create a writable directory for temp files (Hugging Face requirement)
RUN mkdir -p /app/temp_files && chmod 777 /app/temp_files

# Expose port (Hugging Face uses 7860 by default)
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
