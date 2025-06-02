import React, { useState } from 'react';

const PromptInput = ({ onSubmit, isLoading }) => {
  const [basePrompt, setBasePrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (basePrompt.trim()) {
      onSubmit(basePrompt);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-2xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4 text-white">Enter Your Base Prompt</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <textarea
            value={basePrompt}
            onChange={(e) => setBasePrompt(e.target.value)}
            className="w-full px-4 py-3 border border-gray-700 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-150"
            rows="6"
            placeholder="e.g., Explain quantum computing in simple terms..."
            required
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 transition duration-150 disabled:opacity-50"
          disabled={isLoading}
        >
          {isLoading ? 'Loading...' : 'Generate Questionnaire'}
        </button>
      </form>
    </div>
  );
};

export default PromptInput;