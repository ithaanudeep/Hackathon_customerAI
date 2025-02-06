import React, { useContext, useState } from "react";
import { ChatContext } from "../context/ChatContext";

const ChatBot = () => {
  const { chatHistory, addMessage, submitFeedback, loading } = useContext(ChatContext);
  const [message, setMessage] = useState("");

  const handleSend = async () => {
    if (!message.trim()) return;

    // Add user message and fetch AI response
    await addMessage(message, "general inquiry"); // Replace with appropriate category
    setMessage("");
  };

  const handleFeedback = async (id, query, answer) => {
    const feedbackScore = prompt("Rate this response (1-5):", "5");
    if (feedbackScore) {
      await submitFeedback(id, query, answer, parseInt(feedbackScore, 10), "general inquiry");
    }
  };

  return (
    <div className="w-full max-w-md p-4 mx-auto bg-gray-100 rounded-lg shadow-md">
      <div className="h-64 overflow-y-auto bg-white p-3 rounded">
        {loading ? (
          <p>Loading...</p>
        ) : (
          chatHistory.map((chat, index) => (
            <div key={index} className="mb-4">
              <p className="text-blue-600">User: {chat.user}</p>
              <p className="text-gray-700">Bot: {chat.bot}</p>
              <p className="text-green-500">Sentiment: {chat.sentiment}</p>
              <p className="text-purple-500">Intent: {chat.intent}</p>
              <button
                onClick={() => handleFeedback(chat.id, chat.user, chat.bot)}
                className="text-sm text-blue-500 underline mt-1"
              >
                Provide Feedback
              </button>
            </div>
          ))
        )}
      </div>
      <div className="flex mt-4">
        <input
          type="text"
          className="flex-1 p-2 border rounded-lg"
          placeholder="Type a message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={handleSend} className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg">
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBot;
