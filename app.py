from flask_cors import CORS

from flask import Flask, request, jsonify
import azure.cognitiveservices.speech as speechsdk
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Function to transcribe audio using Azure Speech Services
def transcribe_audio(audio_file):
    # Convert the audio file to the required format using ffmpeg
    converted_file = "./temp_converted_audio.wav"
    command = [
        "ffmpeg", "-y", "-i", audio_file, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", converted_file
    ]
    subprocess.run(command, check=True)

    # Configure Azure Speech
    speech_config = speechsdk.SpeechConfig(
        subscription="7IkZNjCCi50CrGofofiXfJmv8AYjVKFwYPq7wgzDpTB7BF3ixXzKJQQJ99ALACmepeSXJ3w3AAAYACOG28JD",
        region="uksouth"
    )
    audio_config = speechsdk.AudioConfig(filename=converted_file)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Transcribe the audio
    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech recognized."
    else:
        return "Error in transcription."

# Flask endpoint to handle audio file uploads and transcribe them
@app.route("/transcribe", methods=["POST", "OPTIONS"])
def transcribe():
    if request.method == "OPTIONS":
        # Just respond with an OK and CORS headers (Flask-Cors should handle headers automatically)
        return jsonify({}), 200
    
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    # Save the uploaded audio file
    audio_file = request.files["file"]
    file_path = "./temp_audio.wav"
    audio_file.save(file_path)

    # Try to transcribe the file and handle any errors
    try:
        transcription = transcribe_audio(file_path)
        print("Returning response:", "Transcription:", transcription)
        return jsonify({"transcription": transcription})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Audio conversion failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# A simple test endpoint to ensure the server is running
@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!"

if __name__ == "__main__":
    app.run(debug=True)
