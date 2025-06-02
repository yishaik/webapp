import React, { useState } from 'react';

const availableModels = [
  // OpenAI
  { id: "gpt-4.1", name: "GPT-4.1 (OpenAI)", category: "OpenAI" },
  { id: "gpt-4.1-mini", name: "GPT-4.1 Mini (OpenAI)", category: "OpenAI" },
  { id: "gpt-4.1-nano", name: "GPT-4.1 Nano (OpenAI)", category: "OpenAI" },
  // Anthropic
  { id: "claude-opus-4", name: "Claude Opus 4 (Anthropic)", category: "Anthropic" },
  { id: "claude-sonnet-4", name: "Claude Sonnet 4 (Anthropic)", category: "Anthropic" },
  // xAI
  { id: "grok-3", name: "Grok-3 (xAI)", category: "xAI" },
  { id: "grok-3-mini", name: "Grok-3 Mini (xAI)", category: "xAI" },
  // Google
  { id: "gemini-2.5-pro", name: "Gemini 2.5 Pro (Google)", category: "Google" },
  { id: "gemini-2.5-flash", name: "Gemini 2.5 Flash (Google)", category: "Google" },
];

const ModelSelector = ({ onSelectModels, isLoading, recommendedModels = [] }) => {
  const [selectedModels, setSelectedModels] = useState([]);

  const handleModelToggle = (modelId) => {
    setSelectedModels(prev =>
      prev.includes(modelId)
        ? prev.filter(id => id !== modelId)
        : [...prev, modelId]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedModels.length > 0) {
      onSelectModels(selectedModels);
    } else {
      // Optionally, provide feedback if no models are selected
      alert("Please select at least one model.");
    }
  };

  // Group models by category for better display
  const modelsByCategory = availableModels.reduce((acc, model) => {
    acc[model.category] = acc[model.category] || [];
    acc[model.category].push(model);
    return acc;
  }, {});

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-3xl mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-2 text-white">Select Models</h2>
      <p className="text-sm text-gray-400 mb-6">Choose which models you'd like to get responses from.</p>
      
      <form onSubmit={handleSubmit}>
        <div className="space-y-6 mb-6">
          {Object.entries(modelsByCategory).map(([category, models]) => (
            <div key={category}>
              <h3 className="text-lg font-medium text-indigo-400 mb-3">{category}</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {models.map((model) => (
                  <label
                    key={model.id}
                    className={`flex items-center p-4 rounded-lg transition-all duration-150 cursor-pointer
                                ${selectedModels.includes(model.id) ? 'bg-indigo-600 ring-2 ring-indigo-400' : 'bg-gray-700 hover:bg-gray-600'}
                                ${recommendedModels.includes(model.name) ? 'border-2 border-green-500' : 'border border-gray-600'}`}
                  >
                    <input
                      type="checkbox"
                      checked={selectedModels.includes(model.id)}
                      onChange={() => handleModelToggle(model.id)}
                      className="form-checkbox h-5 w-5 text-indigo-500 bg-gray-800 border-gray-600 rounded focus:ring-indigo-400 focus:ring-offset-0 mr-3"
                      disabled={isLoading}
                    />
                    <span className={`text-sm font-medium ${selectedModels.includes(model.id) ? 'text-white' : 'text-gray-200'}`}>
                      {model.name}
                      {recommendedModels.includes(model.name) && <span className="text-xs text-green-400 ml-2">(Recommended)</span>}
                    </span>
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>

        <button
          type="submit"
          className="w-full bg-green-600 text-white py-3 px-4 rounded-md hover:bg-green-700 transition duration-150 disabled:opacity-50"
          disabled={isLoading || selectedModels.length === 0}
        >
          {isLoading ? 'Processing...' : 'Get Model Responses'}
        </button>
      </form>
    </div>
  );
};

export default ModelSelector;