import azure.cognitiveservices.speech as speechsdk

def transcribe_audio(file_path):
    # Replace with your Azure Speech API key and region
    speech_config = speechsdk.SpeechConfig(
        subscription="7IkZNjCCi50CrGofofiXfJmv8AYjVKFwYPq7wgzDpTB7BF3ixXzKJQQJ99ALACmepeSXJ3w3AAAYACOG28JD",
        region="uksouth"
    )
    # Configure the audio input
    audio_input = speechsdk.AudioConfig(filename=file_path)

    # Initialize the recognizer
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_input
    )

    print("Transcribing audio...")
    result = recognizer.recognize_once()

    # Handle results
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Transcription:", result.text)
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Error:", cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details:", cancellation_details.error_details)
        return None

if __name__ == "__main__":
    # Replace with the path to your audio file
    audio_file_path = "sample_audio.wav"
    transcription = transcribe_audio(audio_file_path)
    if transcription:
        print("Final Transcription:", transcription)
