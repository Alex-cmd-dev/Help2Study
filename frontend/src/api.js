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
 */
api.interceptors.request.use(
  (config) => {
    // Get JWT token from browser storage
    const token = localStorage.getItem(ACCESS_TOKEN);

    if (token) {
      // Add to Authorization header as "Bearer <token>"
      // Backend will validate this token
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    // Handle any errors that occur before the request is sent
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
