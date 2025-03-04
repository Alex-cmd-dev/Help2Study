import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

function FileUploadForm() {
  const [loading, setLoading] = useState(false);
  const [topic, setTopic] = useState("");
  const [file, setFile] = useState(null);

  const createFlashcards = (e) => {
    setLoading(true);
    e.preventDefault();
    if (!file) {
      alert("Please upload a file.");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append("topic", topic);
    formData.append("file", file);

    api
      .post("/api/topics/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.status === 201) alert("Note created!");
        else alert("Failed to make note.");
      })
      .catch((err) => alert(err))
      .finally(() => setLoading(false));
  };

  return (
    <form
      className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-md"
      onSubmit={createFlashcards}
    >
      <h2 className="text-xl font-bold mb-4 text-blue-500">
        Submit Flashcard Content
      </h2>
      <div className="mb-4">
        <label
          htmlFor="topic"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Topic
        </label>
        <input
          id="topic"
          type="text"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          placeholder="Enter topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          required
        />
      </div>
      <div className="mb-4">
        <label
          htmlFor="file-upload"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Upload File
        </label>
        <input
          id="file-upload"
          type="file"
          value={file}
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          accept=".pdf,.txt,.docx"
        />
        <p className="mt-1 text-xs text-gray-500">
          Accepted file types: PDF, TXT, DOCX
        </p>
      </div>
      <button
        type="submit"
        className="w-full py-2 px-4 rounded-md text-white font-medium bg-blue-600 hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Submit
      </button>
    </form>
  );
}

export default FileUploadForm;
