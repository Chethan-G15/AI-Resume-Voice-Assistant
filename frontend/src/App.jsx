import { useState } from "react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const [listening, setListening] = useState(false);
  const [voiceText, setVoiceText] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setUploadMessage("");
  };

  const uploadResume = async () => {
    if (!selectedFile) {
      setUploadMessage("Please select a PDF resume.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setUploading(true);
    setUploadMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/resumes/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();

      console.log("Upload response:", data);

      setUploadMessage(
        data.message || "Resume uploaded successfully."
      );

      setSelectedFile(null);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadMessage("Could not upload the resume.");
    } finally {
      setUploading(false);
    }
  };

  const sendQuery = async (text) => {
    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/query/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to connect to backend");
      }

      const data = await response.json();

      console.log("Backend response:", data);

      setAnswer(data.answer || "No answer received.");
    } catch (error) {
      console.error("Query error:", error);
      setAnswer("Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  };

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Speech recognition is not supported in this browser."
      );
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setListening(true);
    };

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;

      setVoiceText(text);

      sendQuery(text);
    };

    recognition.onerror = (event) => {
      console.error(
        "Speech recognition error:",
        event.error
      );
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  };

  return (
    <div className="app">
      <h1>AI Resume Voice Agent</h1>

      <p className="subtitle">
        Upload resumes and ask questions using your voice.
      </p>

      {/* Resume Upload */}

      <div className="upload-box">
        <h2>Upload Resume</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
        />

        {selectedFile && (
          <p>
            Selected file: <strong>{selectedFile.name}</strong>
          </p>
        )}

        <button
          className="upload-button"
          onClick={uploadResume}
          disabled={uploading}
        >
          {uploading ? "Uploading..." : "Upload Resume"}
        </button>

        {uploadMessage && (
          <p className="upload-message">
            {uploadMessage}
          </p>
        )}
      </div>

      {/* Voice Section */}

      <div className="voice-box">
        <h2>Ask About a Resume</h2>

        <button
          className="mic-button"
          onClick={startListening}
        >
          🎤
        </button>

        <p>
          {listening
            ? "Listening..."
            : "Click the microphone to ask a question"}
        </p>
      </div>

      {/* Conversation */}

      {voiceText && (
        <div className="conversation">
          <div className="user-message">
            <strong>You:</strong>
            <p>{voiceText}</p>
          </div>

          <div className="agent-message">
            <strong>AI Resume Agent:</strong>

            <p>
              {loading
                ? "Getting answer..."
                : answer || "Waiting for answer..."}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;