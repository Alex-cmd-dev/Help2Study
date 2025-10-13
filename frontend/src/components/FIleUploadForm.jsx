/**
 * FILE UPLOAD FORM - The "Order Form" in our Restaurant
 *
 * This component handles document uploads and flashcard creation.
 * It demonstrates the complete frontend flow: user interaction → API call → UI update
 *
 * 🔵 REQUEST JOURNEY - STEP 1: This is where the upload journey begins!
 *
 * CONCEPTS: React Component, State Management, Event Handling, Async/Await, Form Data
 * RELATED: api.js (HTTP client), backend/api/views.py (receives this request)
 */

import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

function FileUploadForm() {
  /**
   * STATE MANAGEMENT - Tracking component data
   *
   * useState creates reactive data - when state changes, React re-renders the component
   * This is how the UI stays in sync with data
   *
   * CONCEPT: State Management, React Hooks
   */
  const [loading, setLoading] = useState(false);     // Is API call in progress?
  const [topic, setTopic] = useState("");            // Topic name from input
  const [file, setFile] = useState(null);            // Selected file
  const [apicall, setAPIcall] = useState(false);     // Was upload successful?
  const navigate = useNavigate();                     // For navigation after success

  /**
   * EVENT HANDLER - Handles form submission
   *
   * 🔵 REQUEST JOURNEY - STEP 1: User clicks submit → This function runs
   *
   * FLOW:
   * 1. User clicks "Submit" button
   * 2. This function captures the event
   * 3. Validates input
   * 4. Prepares data (FormData)
   * 5. Sends HTTP POST request
   * 6. Handles response
   * 7. Updates UI
   *
   * CONCEPTS: Event Handling, FormData, Async Operations, HTTP POST
   */
  const createFlashcards = (e) => {
    setLoading(true);             // Show loading spinner
    e.preventDefault();           // Prevent page refresh (default form behavior)

    // Validate file was selected
    if (!file) {
      alert("Please upload a file.");
      setLoading(false);
      return;
    }

    /**
     * FormData - For file uploads
     *
     * FormData is used to send files over HTTP
     * It creates multipart/form-data format
     */
    const formData = new FormData();
    formData.append("name", topic);   // Add topic name
    formData.append("file", file);    // Add selected file
    setAPIcall(false);

    /**
     * 🔵 REQUEST JOURNEY - STEP 2: Making the API call
     *
     * api.post() sends HTTP POST request to backend
     * This is ASYNCHRONOUS - doesn't block the UI
     *
     * CONCEPTS: HTTP Request, Asynchronous JavaScript, Promises
     */
    api
      .post("/api/topics/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",  // Tell server it's a file
        },
      })
      .then((res) => {
        // 🔵 REQUEST JOURNEY - STEP 7: Response received!
        if (res.status === 201) {              // 201 = Created (success)
          alert("Flashcards created");
          setAPIcall(true);                    // Triggers UI update to show "View" button
        } else alert("Failed to make flashcards.");
      })
      .catch((err) => alert(err))              // Handle any errors
      .finally(() => setLoading(false));       // Hide loading spinner
  };
  const viewFlashcards = (e) => {
    e.preventDefault();
    navigate("/topics");  // Navigate to topics page
  };

  /**
   * CONDITIONAL RENDERING - Different UI based on state
   *
   * React re-renders when state changes, showing different views:
   * 1. If apicall === true: Show "View Flashcards" button
   * 2. If loading === true: Show loading spinner
   * 3. Otherwise: Show upload form
   *
   * CONCEPT: Conditional Rendering, Component Re-rendering
   */

  // Show success screen after upload completes
  if (apicall) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <button className="btn btn-wid bg-blue-950" onClick={viewFlashcards}>
          View Flashcards
        </button>
      </div>
    );
  }

  // Show loading spinner while waiting for API response
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

  /**
   * MAIN FORM - The upload interface
   *
   * CONCEPTS: JSX, Event Handling, Controlled Components
   *
   * KEY ATTRIBUTES:
   * - value={topic}: Makes input "controlled" by React state
   * - onChange={(e) => setTopic(e.target.value)}: Updates state on typing
   * - onSubmit={createFlashcards}: Calls handler when form submitted
   */
  return (
    <form
      className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-md"
      onSubmit={createFlashcards}  // 🔵 Form submission triggers API call
    >
      <h2 className="text-xl font-bold mb-4 text-blue-950">
        Submit Flashcard Content
      </h2>

      {/* Topic input - controlled component */}
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
          value={topic}                              // Controlled by state
          onChange={(e) => setTopic(e.target.value)} // Updates state on change
          required
        />
      </div>

      {/* File input */}
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
            onChange={(e) => setFile(e.target.files[0])}  // Store selected file
            accept=".pdf,.txt,.docx"                       // Restrict file types
          />
          <label className="fieldset-label text-black">
            Accepted file types: PDF, TXT, DOCX
          </label>
        </fieldset>
      </div>

      {/* Submit button */}
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
