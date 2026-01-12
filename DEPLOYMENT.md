# Deployment Guide for CogniTranslate

This guide explains how to save your code to **GitHub** and deploy your AI app to **Hugging Face Spaces**.

---

## Part 1: Saving to GitHub (Version Control)

### 1. Initialize Git
Run these commands in your project terminal (`d:\Me\Project\cognitranslate copy testing\cognitranslate-app`):

```bash
git init
git add .
git commit -m "Initial commit - Voice Cloning working"
```

### 2. Create a GitHub Repository
1.  Go to [GitHub.com](https://github.com/new).
2.  Create a new repository named `cognitranslate-ai`.
3.  **Do not** check "Add README" or ".gitignore" (you already have them).
4.  Copy the commands under **"…or push an existing repository from the command line"**.

### 3. Push Code
Paste those commands into your terminal. They usually look like:
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cognitranslater-ai.git
git push -u origin main
```

---

## Part 2: Deploying to Hugging Face (Simultaneous Deployment)

**Yes! You can connect to BOTH GitHub and Hugging Face.**
Git allows multiple "remotes". We will call GitHub `origin` and Hugging Face `space`.

### 1. Add Hugging Face Remote
```bash
git remote add space https://huggingface.co/spaces/YOUR_NAME/cognitranslate-app
```

### 2. Push to Both
*   **To Save Code (GitHub):** `git push origin main`
*   **To Deploy App (Hugging Face):** `git push space main`

---

## Part 3: Hugging Face Configuration

**Critical Note:** Your app requires a GPU (or a strong CPU) and Python 3.10. Standard free web hosts (Vercel, Netlify) **cannot** run this.

### Best Option: Hugging Face Spaces (Free CPU / Paid GPU)
Hugging Face is designed for AI apps.

#### 1. Create a "Space"
1.  Go to [Hugging Face Spaces](https://huggingface.co/new-space).
2.  Name: `cognitranslate-app`.
3.  SDK: **Docker** (Recommended for full control) or **Gradio** (Simpler, but requires UI Rewrite). stick with **Docker** to keep your current UI.
4.  Hardware: **Free CPU Basic** (Slow cloning) or **ZeroGPU / Nvidia T4** (Fast cloning, may cost $).

#### 2. Create a `Dockerfile`
Create a file named `Dockerfile` in your project folder with this content:

```dockerfile
# Use Python 3.10
FROM python:3.10-slim

# Install system dependencies (FFmpeg is crucial!)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    espeak-ng \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set up work directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Critical: Install Coqui TTS and PyTorch (CPU version for Free Tier, CUDA for GPU Tier)
# For Free CPU Tier:
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY . .

# Expose port (Hugging Face uses 7860)
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
```

#### 3. Push to Hugging Face
1.  Hugging Face gives you a Git URL for your space.
2.  `git remote add space https://huggingface.co/spaces/YOUR_NAME/cognitranslate-app`
3.  `git push space main`

#### 4. Configure Secrets
1.  Go to your Space's **Settings** tab.
2.  Scroll to **Repository secrets**.
3.  Add `GOOGLE_API_KEY` and your key.

---

## Limitations of Free Hosting
*   **Speed**: On a Free CPU tier, voice cloning might take **30-60 seconds**. On your local RTX 4050, it takes ~3 seconds.
*   **Memory**: The model is 3GB. Free tiers might crash if RAM is low (< 16GB).

**Conclusion**: For now, running **Locally** (as you are doing) is the best experience. Deploy only if you need to share it with others.
