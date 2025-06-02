import React, { useState } from 'react';

const PromptInput = ({ promptData, setPromptData, nextStep }) => {
  const [basePrompt, setBasePrompt] = useState(promptData.basePrompt);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (basePrompt.trim()) {
      setPromptData({ ...promptData, basePrompt });
      nextStep();
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-semibold mb-4">Enter Your Base Prompt</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            What would you like to accomplish?
          </label>
          <textarea
            value={basePrompt}
            onChange={(e) => setBasePrompt(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="6"
            placeholder="Describe your task or the type of response you're looking for..."
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 transition duration-200"
        >
          Continue to Model Selection
        </button>
      </form>
    </div>
  );
};

export default PromptInput;