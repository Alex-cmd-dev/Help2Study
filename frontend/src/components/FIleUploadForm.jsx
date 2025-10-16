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
import topicService from "../services/topicService";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Upload, Check } from "lucide-react";

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
  const createFlashcards = async (e) => {
    console.log('%c🔵 REQUEST JOURNEY - STEP 1: User Action', 'color: #9B59B6; font-weight: bold');
    console.log('👤 User clicked "Create Flashcards" button');

    setLoading(true);             // Show loading spinner
    e.preventDefault();           // Prevent page refresh (default form behavior)

    // Validate file was selected
    if (!file) {
      console.warn('⚠️ Validation failed: No file selected');
      alert("Please upload a file.");
      setLoading(false);
      return;
    }

    console.log('📝 Form data collected:', { topic, fileName: file.name, fileType: file.type });

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

    console.log('📦 FormData prepared for upload');

    /**
     * 🔵 REQUEST JOURNEY - STEP 2: Making the API call
     *
     * Using topicService.createTopic() instead of calling API directly
     * This is ASYNCHRONOUS - doesn't block the UI
     *
     * CONCEPTS: HTTP Request, Asynchronous JavaScript, Service Layer
     */
    try {
      await topicService.createTopic(formData);
      // 🔵 REQUEST JOURNEY - STEP 8: UI Update
      console.log('%c🔵 REQUEST JOURNEY - STEP 8: Updating UI', 'color: #F39C12; font-weight: bold');
      console.log('✅ Flashcards created successfully!');
      console.log('🔄 Triggering React state update...');
      alert("Flashcards created");
      setAPIcall(true);  // Triggers UI update to show "View" button
    } catch (err) {
      console.error('❌ Error creating flashcards:', err);
      alert("Failed to create flashcards. Please try again.");
    } finally {
      setLoading(false);
      console.log('🏁 Request journey complete');
    }
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
      <Card className="w-full max-w-md">
        <CardContent className="pt-6 flex flex-col items-center gap-4">
          <div className="rounded-full bg-primary/10 p-4">
            <Check className="h-8 w-8 text-primary" />
          </div>
          <div className="text-center">
            <h3 className="text-xl font-semibold mb-2">Flashcards Created!</h3>
            <p className="text-muted-foreground mb-4">
              Your flashcards are ready to study.
            </p>
          </div>
          <Button onClick={viewFlashcards} className="w-full" size="lg">
            View Flashcards
          </Button>
        </CardContent>
      </Card>
    );
  }

  // Show loading spinner while waiting for API response
  if (loading) {
    return (
      <Card className="w-full max-w-md">
        <CardContent className="pt-6 flex flex-col items-center gap-4">
          <Loader2 className="h-12 w-12 animate-spin text-primary" />
          <div className="text-center">
            <h3 className="text-lg font-semibold">Creating Flashcards</h3>
            <p className="text-sm text-muted-foreground mt-1">
              Processing your document...
            </p>
          </div>
        </CardContent>
      </Card>
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
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Create Flashcards</CardTitle>
        <CardDescription>
          Upload a document to automatically generate flashcards
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={createFlashcards} className="space-y-4">
          {/* Topic input - controlled component */}
          <div className="space-y-2">
            <Label htmlFor="topic">Topic</Label>
            <Input
              id="topic"
              type="text"
              placeholder="e.g., Biology Chapter 1"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              required
            />
          </div>

          {/* File input */}
          <div className="space-y-2">
            <Label htmlFor="file-upload">Upload Document</Label>
            <div className="grid w-full items-center gap-1.5">
              <Input
                id="file-upload"
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                accept=".pdf,.txt,.docx"
                className="cursor-pointer"
              />
              <p className="text-xs text-muted-foreground">
                Accepted formats: PDF, TXT, DOCX
              </p>
            </div>
          </div>

          {/* Submit button */}
          <Button type="submit" className="w-full" size="lg">
            <Upload className="mr-2 h-4 w-4" />
            Create Flashcards
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

export default FileUploadForm;
