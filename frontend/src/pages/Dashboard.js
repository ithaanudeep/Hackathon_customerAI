import React from "react";

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
        Dashboard
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Placeholder for Analytics Data */}
        <div className="p-4 bg-white shadow-md rounded-lg">
          <h2 className="text-xl font-semibold mb-4">Chat Analytics</h2>
          <p>Number of chats processed: <span className="font-bold">42</span></p>
          <p>Active users: <span className="font-bold">10</span></p>
        </div>

        {/* Placeholder for User Engagement */}
        <div className="p-4 bg-white shadow-md rounded-lg">
          <h2 className="text-xl font-semibold mb-4">User Engagement</h2>
          <p>Average response time: <span className="font-bold">1.2 sec</span></p>
          <p>Satisfaction score: <span className="font-bold">92%</span></p>
        </div>

        {/* Placeholder for Additional Stats */}
        <div className="p-4 bg-white shadow-md rounded-lg">
          <h2 className="text-xl font-semibold mb-4">Custom Metrics</h2>
          <p>Custom metric #1: <span className="font-bold">Value</span></p>
          <p>Custom metric #2: <span className="font-bold">Value</span></p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
