import React, { createContext, useState } from "react";
import { sendQuery, sendFeedback } from "../api/chatService";

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const addMessage = async (userMessage, category) => {
    try {
      setLoading(true);

      // Generate a unique ID for the query
      const queryId = `${Date.now()}-${Math.random().toString(36).substring(7)}`;

      // Send the query to the backend
      const response = await sendQuery(queryId, userMessage, category);

      // Add the user message and AI response to the chat history
      setChatHistory((prevHistory) => [
        ...prevHistory,
        {
          id: queryId,
          user: userMessage,
          bot: response.answer,
          sentiment: response.sentiment,
          intent: response.intent,
        },
      ]);
    } catch (error) {
      console.error("Error adding message:", error);
    } finally {
      setLoading(false);
    }
  };

  const submitFeedback = async (id, query, answer, feedbackScore, category) => {
    try {
      await sendFeedback(id, query, answer, feedbackScore, category);
    } catch (error) {
      console.error("Error submitting feedback:", error);
    }
  };

  return (
    <ChatContext.Provider value={{ chatHistory, addMessage, submitFeedback, loading }}>
      {children}
    </ChatContext.Provider>
  );
};
