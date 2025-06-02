import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import * as api from '../services/api'; // Adjust path as necessary

const HistoryView = () => {
  const [prompts, setPrompts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await api.getHistoryPrompts();
        setPrompts(data || []);
      } catch (err) {
        setError('Failed to fetch history. Details: ' + (err.response?.data?.detail || err.message));
        setPrompts([]);
      } finally {
        setIsLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (isLoading) {
    return (
      <div className="text-center py-10">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
        <p className="mt-4 text-lg text-gray-300">Loading history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-800 border border-red-600 text-white p-4 rounded-md shadow-lg max-w-md mx-auto">
        <p className="font-semibold">Error loading history:</p>
        <p className="text-sm">{error}</p>
      </div>
    );
  }

  if (prompts.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="text-xl text-gray-400">No history found.</p>
        <p className="text-sm text-gray-500 mt-2">Start by creating some prompts on the Forge page!</p>
        <Link to="/" className="mt-4 inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded transition-colors">
          Go to Forge
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-center text-indigo-400">Prompt History</h1>
      <div className="space-y-4">
        {prompts.map(prompt => (
          <Link
            key={prompt.id}
            to={`/history/${prompt.id}`}
            className="block bg-gray-800 hover:bg-gray-700 p-5 rounded-lg shadow-lg transition-all duration-150 ease-in-out transform hover:scale-105"
          >
            <div className="flex justify-between items-center">
              <p className="text-lg font-semibold text-indigo-300 truncate" title={prompt.base_prompt}>
                {prompt.base_prompt.substring(0, 100)}{prompt.base_prompt.length > 100 ? '...' : ''}
              </p>
              <span className="text-xs text-gray-500 ml-4 whitespace-nowrap">
                ID: {prompt.id}
              </span>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              {new Date(prompt.timestamp).toLocaleString()}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default HistoryView;
