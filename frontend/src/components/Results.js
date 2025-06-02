import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Results = ({ promptData, setPromptData, prevStep }) => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  useEffect(() => {
    generateOptimizedPrompts();
  }, []);

  const generateOptimizedPrompts = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/optimize-prompts', {
        base_prompt: promptData.basePrompt,
        selected_models: promptData.selectedModels
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error generating prompts:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-6">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p>Generating optimized prompts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-semibold mb-4">Optimized Prompts & Results</h2>
        <div className="bg-gray-50 p-4 rounded-lg mb-4">
          <h3 className="font-medium text-gray-700 mb-2">Original Prompt:</h3>
          <p className="text-gray-900">{promptData.basePrompt}</p>
        </div>
      </div>

      <div className="grid gap-6">
        {results.map((result, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4 text-blue-600">
              {result.model_name}
            </h3>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Optimized Prompt:</h4>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-gray-900">{result.optimized_prompt}</p>
                </div>
              </div>
              {result.output && (
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Model Output:</h4>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-900">{result.output}</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 flex justify-center">
        <button
          onClick={prevStep}
          className="bg-gray-300 text-gray-700 py-2 px-6 rounded-md hover:bg-gray-400 transition duration-200"
        >
          Back to Model Selection
        </button>
      </div>
    </div>
  );
};

export default Results;