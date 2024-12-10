import subprocess

try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("FFmpeg is installed and accessible!")
except FileNotFoundError:
    print("FFmpeg is not installed or not in PATH.")
