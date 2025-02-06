import React from "react";
import ReactDOM from "react-dom/client"; // Import createRoot for React 18
import App from "./App";
import "./index.css"; // Import Tailwind CSS
import { ChatProvider } from "./context/ChatContext";

const root = ReactDOM.createRoot(document.getElementById("root")); // Use createRoot instead of render

root.render(
  <React.StrictMode>
    <ChatProvider>
      <App />
    </ChatProvider>
  </React.StrictMode>
);
