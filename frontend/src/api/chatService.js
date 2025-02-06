import axios from "axios";

// Backend base URL
const BASE_URL = "http://localhost:8000"; // Replace with your backend URL

/**
 * Send a query to the backend and receive an AI-generated response.
 * @param {string} id - A unique ID for the query.
 * @param {string} query - The user's query.
 * @param {string} category - The category of the query.
 * @returns {Promise<Object>} - The response containing answer, sentiment, and intent.
 */
export const sendQuery = async (id, query, category) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/query`,
      { id, query, category },
      {
        headers: {
          "Content-Type": "application/json", // Set Content-Type header
        },
      }
    );
    return response.data; // { answer, sentiment, intent }
  } catch (error) {
    console.error("Error sending query:", error);
    throw error;
  }
};

/**
 * Send feedback for a specific query.
 * @param {string} id - The unique ID for the query.
 * @param {string} query - The user's query.
 * @param {string} answer - The AI-generated answer.
 * @param {number} feedbackScore - User feedback score (1-5).
 * @param {string} category - The category of the query.
 * @returns {Promise<Object>} - The backend's response.
 */
export const sendFeedback = async (id, query, answer, feedbackScore, category) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/feedback`,
      { id, query, answer, feedback_score: feedbackScore, category },
      {
        headers: {
          "Content-Type": "application/json", // Set Content-Type header
        },
      }
    );
    return response.data; // { message, improved_answer (if feedback is low) }
  } catch (error) {
    console.error("Error sending feedback:", error);
    throw error;
  }
};
