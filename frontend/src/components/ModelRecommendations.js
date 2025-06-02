import React from 'react';

const ModelRecommendations = ({ recommendations, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-2xl mx-auto mt-8">
        <h2 className="text-xl font-semibold mb-4 text-white">Model Recommendations</h2>
        <div className="flex items-center">
          <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-indigo-500 mr-3"></div>
          <p className="text-gray-400">Loading recommendations...</p>
        </div>
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return null; // Don't render if no recommendations
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-2xl mx-auto mt-8">
      <h2 className="text-xl font-semibold mb-4 text-white">Model Recommendations</h2>
      <ul className="space-y-2">
        {recommendations.map((modelName, index) => (
          <li key={index} className="p-3 bg-gray-700 rounded-md text-gray-200 shadow">
            <span className="font-medium text-indigo-300">{modelName}</span>
          </li>
        ))}
      </ul>
      <p className="text-xs text-gray-500 mt-4">
        These are suggestions. You can select any model(s) you prefer.
      </p>
    </div>
  );
};

export default ModelRecommendations;
