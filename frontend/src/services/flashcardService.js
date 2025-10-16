/**
 * FLASHCARD SERVICE - API calls for flashcards
 *
 * This service encapsulates all API calls related to flashcards.
 * Components import this service instead of calling the API directly.
 *
 * EDUCATIONAL NOTE - SERVICE LAYER:
 * This follows the same pattern as topicService.js!
 * By creating separate services for different resources (topics, flashcards),
 * we organize our API calls logically.
 *
 * WHY SEPARATE SERVICES:
 * 1. ORGANIZATION: Each service handles one resource type
 * 2. SCALABILITY: Easy to add more services (users, settings, etc.)
 * 3. TEAM COLLABORATION: Different developers can work on different services
 * 4. MODULARITY: Import only what you need
 *
 * CONCEPTS: Service Layer, Resource-Based Organization, Modular Design
 * RELATED: topicService.js (similar pattern), api.js (HTTP client)
 */

import api from "../api";

/**
 * Fetch all flashcards for a specific topic
 *
 * @param {number} topicId - ID of the topic
 * @returns {Promise<Array>} Array of flashcard objects
 * @throws {Error} If API call fails
 *
 * EXAMPLE USAGE:
 *   const flashcards = await flashcardService.getFlashcardsByTopic(5);
 *   console.log(flashcards); // [{ id: 1, question: "...", answer: "..." }, ...]
 *
 * EDUCATIONAL NOTE - REST API:
 * The endpoint /api/flashcards/:id follows RESTful convention:
 * - Resource: flashcards
 * - Identifier: :id (topic ID)
 * - Action: GET (read)
 */
export const getFlashcardsByTopic = async (topicId) => {
  const response = await api.get(`/api/flashcards/${topicId}/`);
  return response.data;
};

/**
 * Delete a single flashcard
 *
 * @param {number} flashcardId - ID of the flashcard to delete
 * @returns {Promise<void>}
 * @throws {Error} If API call fails
 *
 * EXAMPLE USAGE:
 *   await flashcardService.deleteFlashcard(42);
 *   console.log('Flashcard deleted!');
 */
export const deleteFlashcard = async (flashcardId) => {
  await api.delete(`/api/flashcards/${flashcardId}/`);
};

/**
 * Create a manual flashcard (not AI-generated)
 *
 * @param {Object} flashcardData - Flashcard data
 * @param {number} flashcardData.topicId - Topic to add flashcard to
 * @param {string} flashcardData.question - Question text
 * @param {string} flashcardData.answer - Answer text
 * @returns {Promise<Object>} Created flashcard object
 * @throws {Error} If API call fails
 *
 * EXAMPLE USAGE:
 *   const newCard = await flashcardService.createFlashcard({
 *     topicId: 5,
 *     question: "What is 2+2?",
 *     answer: "4"
 *   });
 *
 * EDUCATIONAL NOTE:
 * This is rarely used because most flashcards are AI-generated.
 * But it's useful for:
 * - Adding custom cards
 * - Editing existing cards (delete + create new)
 * - Testing without AI API
 */
export const createFlashcard = async (flashcardData) => {
  const response = await api.post("/api/flashcards/", flashcardData);
  return response.data;
};

/**
 * Default export - import all functions as a single object
 */
export default {
  getFlashcardsByTopic,
  deleteFlashcard,
  createFlashcard,
};

/**
 * FUTURE ENHANCEMENTS:
 *
 * As the app grows, you might add:
 *
 * 1. UPDATE FLASHCARD:
 *    export const updateFlashcard = async (id, updates) => {
 *      await api.patch(`/api/flashcards/${id}/`, updates);
 *    };
 *
 * 2. MARK AS STUDIED:
 *    export const markAsStudied = async (id) => {
 *      await api.post(`/api/flashcards/${id}/studied/`);
 *    };
 *
 * 3. GET STUDY STATISTICS:
 *    export const getStudyStats = async (topicId) => {
 *      const response = await api.get(`/api/topics/${topicId}/stats/`);
 *      return response.data;
 *    };
 *
 * The service pattern makes it easy to add these features!
 */
