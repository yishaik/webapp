import React, { useState, useEffect } from 'react';
import { useParams, Link }
from 'react-router-dom';
import * as api from '../services/api'; // Adjust path as necessary

const HistoryDetailPage = () => {
  const { promptId } = useParams();
  const [promptDetails, setPromptDetails] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDetails = async () => {
      if (!promptId) return;
      setIsLoading(true);
      setError(null);
      try {
        const data = await api.getHistoryPromptDetails(promptId);
        setPromptDetails(data);
      } catch (err) {
        setError('Failed to fetch prompt details. Details: ' + (err.response?.data?.detail || err.message));
        setPromptDetails(null);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDetails();
  }, [promptId]);

  if (isLoading) {
    return (
      <div className="text-center py-10">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
        <p className="mt-4 text-lg text-gray-300">Loading prompt details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-800 border border-red-600 text-white p-4 rounded-md shadow-lg max-w-md mx-auto">
        <p className="font-semibold">Error loading details:</p>
        <p className="text-sm">{error}</p>
        <Link to="/history" className="mt-4 inline-block text-indigo-300 hover:text-indigo-400">
          &larr; Back to History
        </Link>
      </div>
    );
  }

  if (!promptDetails) {
    return (
      <div className="text-center py-10">
        <p className="text-xl text-gray-400">Prompt details not found.</p>
        <Link to="/history" className="mt-4 inline-block text-indigo-300 hover:text-indigo-400">
          &larr; Back to History
        </Link>
      </div>
    );
  }

  // Sort model outputs by timestamp (newest first) for consistency, if not already sorted by backend
  const sortedModelOutputs = promptDetails.model_outputs
    ? [...promptDetails.model_outputs].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    : [];

  return (
    <div className="max-w-4xl mx-auto space-y-8 text-white">
      <div>
        <Link to="/history" className="text-indigo-400 hover:text-indigo-300 transition-colors text-sm mb-4 inline-block">
          &larr; Back to History
        </Link>
        <h1 className="text-3xl font-bold text-indigo-400">Prompt Details</h1>
        <p className="text-xs text-gray-500 mt-1">ID: {promptDetails.id} &bull; Created: {new Date(promptDetails.timestamp).toLocaleString()}</p>
      </div>

      <div className="bg-gray-800 p-6 rounded-lg shadow-xl">
        <h2 className="text-xl font-semibold text-indigo-300 mb-3">Base Prompt</h2>
        <p className="text-gray-300 whitespace-pre-wrap">{promptDetails.base_prompt}</p>
      </div>

      {promptDetails.questionnaire_responses && promptDetails.questionnaire_responses.length > 0 && (
        <div className="bg-gray-800 p-6 rounded-lg shadow-xl">
          <h2 className="text-xl font-semibold text-indigo-300 mb-4">Questionnaire Responses</h2>
          <ul className="space-y-4">
            {promptDetails.questionnaire_responses.map(qr => (
              <li key={qr.id} className="p-4 bg-gray-700 rounded-md shadow">
                <p className="font-medium text-gray-400">{qr.question}</p>
                <p className="text-indigo-200 mt-1 whitespace-pre-wrap">{qr.answer || <em className="text-gray-500">No answer provided</em>}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {sortedModelOutputs.length > 0 && (
        <div className="bg-gray-800 p-6 rounded-lg shadow-xl">
          <h2 className="text-xl font-semibold text-indigo-300 mb-4">Model Outputs</h2>
          <div className="space-y-6">
            {sortedModelOutputs.map(output => (
              <div key={output.id} className="bg-gray-700 p-5 rounded-lg shadow-md">
                <h3 className="text-lg font-semibold text-indigo-400 mb-1">{output.model_name}</h3>
                <p className="text-xs text-gray-500 mb-3">Generated: {new Date(output.timestamp).toLocaleString()}</p>
                <div className="prose prose-sm prose-invert max-w-none text-gray-200 whitespace-pre-wrap">
                  {output.output}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
       {!promptDetails.model_outputs || sortedModelOutputs.length === 0 && (
         <div className="bg-gray-800 p-6 rounded-lg shadow-xl text-center">
            <p className="text-gray-500">No model outputs recorded for this prompt.</p>
         </div>
       )}
    </div>
  );
};

export default HistoryDetailPage;
