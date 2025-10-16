/**
 * TOPIC SERVICE - API calls for flashcard topics
 *
 * This service encapsulates all API calls related to topics.
 * Components import this service instead of calling the API directly.
 *
 * EDUCATIONAL NOTE - SERVICE LAYER:
 * Notice we extracted API calls from components into this separate file!
 * This is the "Service Layer Pattern" - a common pattern in web development.
 *
 * WHY CREATE A SERVICE LAYER:
 * 1. DRY PRINCIPLE: Don't repeat API calls in multiple components
 * 2. SINGLE SOURCE OF TRUTH: All topic-related API logic in one place
 * 3. EASIER TESTING: Mock the service instead of API calls in components
 * 4. EASIER MAINTENANCE: Change API endpoint once, not in 5 components
 * 5. CLEARER COMPONENTS: Components focus on UI, not network logic
 *
 * BEFORE (scattered in components):
 *   Component A: api.get('/api/topics/')
 *   Component B: api.get('/api/topics/')
 *   Component C: api.post('/api/topics/', data)
 *   → Hard to maintain, duplicated code
 *
 * AFTER (centralized in service):
 *   topicService.getAllTopics()
 *   topicService.createTopic(data)
 *   → Clean, reusable, maintainable
 *
 * CONCEPTS: Service Layer, Separation of Concerns, DRY Principle
 * RELATED: flashcardService.js (similar pattern), api.js (HTTP client)
 */

import api from "../api";

/**
 * Fetch all topics for the current user
 *
 * @returns {Promise<Array>} Array of topic objects
 * @throws {Error} If API call fails
 *
 * EXAMPLE USAGE:
 *   const topics = await topicService.getAllTopics();
 *   console.log(topics); // [{ id: 1, name: "Math", created_at: "..." }, ...]
 */
export const getAllTopics = async () => {
  const response = await api.get("/api/topics/");
  return response.data;
};

/**
 * Create a new topic with flashcards from uploaded file
 *
 * @param {FormData} formData - Contains 'name' (topic name) and 'file' (uploaded document)
 * @returns {Promise<Object>} Created topic object
 * @throws {Error} If API call fails or validation fails
 *
 * EXAMPLE USAGE:
 *   const formData = new FormData();
 *   formData.append('name', 'Biology Chapter 1');
 *   formData.append('file', fileObject);
 *   const newTopic = await topicService.createTopic(formData);
 *
 * EDUCATIONAL NOTE - FormData:
 * FormData is used for file uploads. It creates multipart/form-data format
 * which is required for sending files over HTTP.
 */
export const createTopic = async (formData) => {
  const response = await api.post("/api/topics/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

/**
 * Delete a topic and all its flashcards
 *
 * @param {number} topicId - ID of the topic to delete
 * @returns {Promise<void>}
 * @throws {Error} If API call fails
 *
 * EXAMPLE USAGE:
 *   await topicService.deleteTopic(5);
 *   console.log('Topic deleted!');
 *
 * EDUCATIONAL NOTE - CASCADE DELETE:
 * Deleting a topic automatically deletes all its flashcards.
 * This is configured in the backend (models.py) with on_delete=CASCADE
 */
export const deleteTopic = async (topicId) => {
  await api.delete(`/api/topic/delete/${topicId}`);
};

/**
 * Default export - import all functions as a single object
 *
 * USAGE OPTION 1 (Named imports):
 *   import { getAllTopics, createTopic } from './services/topicService';
 *   const topics = await getAllTopics();
 *
 * USAGE OPTION 2 (Default import):
 *   import topicService from './services/topicService';
 *   const topics = await topicService.getAllTopics();
 *
 * Both work! Named imports are more explicit, default import is cleaner.
 */
export default {
  getAllTopics,
  createTopic,
  deleteTopic,
};

/**
 * NEXT STEPS FOR LEARNING:
 *
 * Once you're comfortable with this service:
 *
 * 1. ADD ERROR HANDLING:
 *    - Catch specific error codes (401 = unauthorized, 404 = not found)
 *    - Return user-friendly error messages
 *    - Implement retry logic for network failures
 *
 * 2. ADD CACHING:
 *    - Cache topic list to avoid repeated API calls
 *    - Implement cache invalidation when topics change
 *    - Use libraries like React Query or SWR
 *
 * 3. ADD OPTIMISTIC UPDATES:
 *    - Update UI before API call completes
 *    - Rollback if API call fails
 *    - Better user experience (feels instant!)
 *
 * See ADVANCED_PATTERNS.md for detailed explanations!
 */
