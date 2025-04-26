import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch("http://localhost:8000/upload/", {
      method: "POST",
      body: formData,
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    setDownloadUrl(url);
  };

  return (
    <div>
      <h1>Music Genre Transfer</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={uploadFile}>Upload and Transform</button>
      {downloadUrl && (
        <a href={downloadUrl} download="transformed_song.wav">
          Download Transformed Song
        </a>
      )}
    </div>
  );
}

export default App;
