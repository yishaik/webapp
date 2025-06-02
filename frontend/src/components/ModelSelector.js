import React, { useState } from 'react';

const ModelSelector = ({ promptData, setPromptData, nextStep, prevStep }) => {
  const [selectedModels, setSelectedModels] = useState(promptData.selectedModels);

  const models = [
    { id: 'openai-gpt4', name: 'OpenAI GPT-4.1', description: 'Advanced reasoning and analysis' },
    { id: 'anthropic-claude', name: 'Anthropic Claude Sonnet 4', description: 'Hybrid reasoning and coding' },
    { id: 'xai-grok', name: 'xAI Grok-3', description: 'Advanced reasoning with Think mode' },
    { id: 'google-gemini', name: 'Google Gemini 2.5 Pro', description: 'Multimodal with Deep Think' }
  ];

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
      setPromptData({ ...promptData, selectedModels });
      nextStep();
    }
  };

  return (
    <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-semibold mb-4">Select Language Models</h2>
      <p className="text-gray-600 mb-6">Choose which models you'd like to optimize your prompt for:</p>
      
      <form onSubmit={handleSubmit}>
        <div className="space-y-4 mb-6">
          {models.map((model) => (
            <div key={model.id} className="border rounded-lg p-4">
              <label className="flex items-start cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedModels.includes(model.id)}
                  onChange={() => handleModelToggle(model.id)}
                  className="mt-1 mr-3"
                />
                <div>
                  <h3 className="font-medium text-gray-900">{model.name}</h3>
                  <p className="text-sm text-gray-600">{model.description}</p>
                </div>
              </label>
            </div>
          ))}
        </div>

        <div className="flex space-x-4">
          <button
            type="button"
            onClick={prevStep}
            className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition duration-200"
          >
            Back
          </button>
          <button
            type="submit"
            disabled={selectedModels.length === 0}
            className="flex-1 bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-gray-300 transition duration-200"
          >
            Generate Optimized Prompts
          </button>
        </div>
      </form>
    </div>
  );
};

export default ModelSelector;