console.log("script.js is loaded!");
let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById("record");
const stopButton = document.getElementById("stop");
const transcriptionBox = document.getElementById("transcription");

recordButton.addEventListener("click", async () => {
    console.log("Record button clicked");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.start();
    console.log("Recording started");
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
        console.log("Audio chunk available");
    };

    mediaRecorder.onstop = async () => {
        console.log("Recording stopped");
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("file", audioBlob, "audio.wav");

        console.log("Audio stopped, preparing to send...");
        try {
            console.log("Sending audio to backend...");  // Debug log before sending
            const response = await fetch("https://otter-transcriber-app-1.onrender.com/transcribe", {
                method: "POST",
                body: formData,
                headers: {
                    "Accept": "application/json"
                }
            });

            console.log("Response received from backend:", response);  // Debug log for the response object

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Transcription from backend:", data);  // Debug log for the transcription

            transcriptionBox.value = data.transcription || "Error in transcription";
        } catch (error) {
            console.error("Error during fetch:", error);  // Debug log for any errors during fetch
            transcriptionBox.value = `Fetch error: ${error.message}`;
        }
    };

    recordButton.style.display = "none";
    stopButton.style.display = "block";
});

stopButton.addEventListener("click", () => {
    console.log("Stop button clicked");
    mediaRecorder.stop();
    recordButton.style.display = "block";
    stopButton.style.display = "none";
});
