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

  if (loading) {
    return (
      <div
        className="flex justify-center items-center min-h-screen"
        data-theme="night"
      >
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }
  return (
    <form
      className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-md"
      onSubmit={createFlashcards}
    >
      <h2 className="text-xl font-bold mb-4 text-blue-950">
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
        <fieldset className="fieldset  ">
          <input
            id="file-upload"
            type="file"
            className="file-input  text-white"
            onChange={(e) => setFile(e.target.files[0])}
            accept=".pdf,.txt,.docx"
          />
          <label className="fieldset-label text-black">
            Accepted file types: PDF, TXT, DOCX
          </label>
        </fieldset>
      </div>
      <button
        type="submit"
        className="w-full py-2 px-4 rounded-md text-white font-medium bg-blue-950 hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Submit
      </button>
    </form>
  );
}

export default FileUploadForm;
