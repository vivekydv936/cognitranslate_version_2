import os
import shutil
import subprocess
import glob

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

# 1. Delete .git folder (Forcefully)
if os.path.exists(".git"):
    print("Deleting .git folder...")
    try:
        shutil.rmtree(".git", ignore_errors=True)
    except Exception as e:
        print(f"Failed to delete .git: {e}")

# 2. Delete Binary Files
files_to_delete = [
    "Synopsis report.pdf",
    "Recording_wav.wav"
]
# Add all temp wavs
files_to_delete.extend(glob.glob("temp_*.wav"))
files_to_delete.extend(glob.glob("output_*.wav"))

for file in files_to_delete:
    if os.path.exists(file):
        print(f"Deleting {file}...")
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

# 3. Re-Initialize Git
run_command("git init")
run_command("git add .")
run_command('git commit -m "Deploy Clean v4"')
run_command("git remote add space https://huggingface.co/spaces/vivekydv936/cognitranslate")

print("\nDONE! You can now run: git push -f space master")
