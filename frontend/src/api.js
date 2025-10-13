/**
 * HTTP CLIENT CONFIGURATION - The "Phone System" in our Restaurant
 *
 * This file configures Axios, our HTTP client for making API requests.
 * Every request to the backend goes through this configured client.
 *
 * 🔵 REQUEST JOURNEY - STEP 2: All API calls use this client
 *
 * KEY FEATURES:
 * - Automatically adds the backend URL to all requests
 * - Automatically adds JWT token for authentication
 * - Centralized error handling
 *
 * CONCEPTS: HTTP Client, Authentication Headers, Interceptors
 * RELATED: All components that make API calls use this
 */

import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

/**
 * Create an Axios instance with base configuration
 *
 * baseURL: Comes from .env file (VITE_API_URL)
 * This means we can use api.get('/topics/') instead of
 * api.get('http://localhost:8000/api/topics/')
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

/**
 * REQUEST INTERCEPTOR - Runs before every request
 *
 * This automatically adds the JWT token to the Authorization header
 * for every request, so we don't have to manually do it each time.
 *
 * FLOW:
 * 1. Component calls api.post('/topics/', data)
 * 2. Interceptor runs first
 * 3. Gets JWT token from localStorage
 * 4. Adds token to Authorization header
 * 5. Request sent to backend with authentication
 *
 * CONCEPT: Interceptors, JWT Authentication, Authorization Header
 *
 * LOGGING NOTE: The console.log statements below use %c for styling.
 * This is a browser feature that lets you add CSS to console messages!
 * - Blue color = Request being sent (Step 2)
 * - Styled font = Easy to spot in a busy console
 *
 * WHY LOG HERE:
 * - Presentations: Show audience when requests go out
 * - Debugging: Verify correct endpoints and auth tokens
 * - Learning: Understand interceptor execution order
 *
 * FUTURE USE: In production apps, you might:
 * - Log request timing for performance monitoring
 * - Send analytics events for user activity tracking
 * - Add correlation IDs for distributed tracing
 */
api.interceptors.request.use(
  (config) => {
    // 🔵 PRESENTATION MODE: Log outgoing requests with styled console output
    console.log('%c🔵 REQUEST JOURNEY - STEP 2: Sending HTTP Request', 'color: #4A90E2; font-weight: bold');
    console.log(`📤 ${config.method.toUpperCase()} ${config.baseURL}${config.url}`);

    // Get JWT token from browser storage
    const token = localStorage.getItem(ACCESS_TOKEN);

    if (token) {
      // Add to Authorization header as "Bearer <token>"
      // Backend will validate this token
      config.headers.Authorization = `Bearer ${token}`;
      console.log('🔐 JWT token attached to request');
    }

    if (config.data) {
      console.log('📦 Request payload:', config.data instanceof FormData ? 'FormData (file upload)' : config.data);
    }

    return config;
  },
  (error) => {
    // Handle any errors that occur before the request is sent
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);

/**
 * RESPONSE INTERCEPTOR - Runs after receiving response
 * Logs the response for presentation/debugging
 *
 * LOGGING NOTE: This interceptor runs AFTER the backend sends a response.
 * - Green color = Successful response received (Step 7)
 * - Red color = Error occurred
 *
 * WHY LOG HERE:
 * - Presentations: Show audience the data coming back from server
 * - Debugging: Verify correct data structure and status codes
 * - Learning: Understand HTTP status codes (200 = success, 404 = not found, etc.)
 *
 * BROWSER DEVTOOLS TIP:
 * Open the browser console (F12) and watch these logs appear in real-time
 * as you interact with the app. You can filter by color or by the 🔵 emoji!
 *
 * FUTURE USE: In production, you might:
 * - Log errors to a service like Sentry for monitoring
 * - Track API response times
 * - Cache responses for better performance
 */
api.interceptors.response.use(
  (response) => {
    // 🔵 PRESENTATION MODE: Log incoming responses with green styling
    console.log('%c🔵 REQUEST JOURNEY - STEP 7: Response Received', 'color: #28A745; font-weight: bold');
    console.log(`✅ Status: ${response.status} ${response.statusText}`);
    console.log('📥 Response data:', response.data);
    return response;
  },
  (error) => {
    // ❌ ERROR HANDLING: Log errors with red styling for visibility
    console.error('%c❌ REQUEST JOURNEY - ERROR', 'color: #DC3545; font-weight: bold');
    console.error('Status:', error.response?.status);
    console.error('Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * USAGE IN COMPONENTS:
 *
 * import api from './api';
 *
 * // GET request
 * const response = await api.get('/topics/');
 *
 * // POST request with data
 * const response = await api.post('/topics/', formData);
 *
 * // DELETE request
 * await api.delete(`/topic/delete/${id}`);
 */

export default api;
