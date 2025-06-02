import React from 'react';

const Results = ({ modelResults, optimizedPrompt }) => {
  if (Object.keys(modelResults).length === 0) {
    return null; // Don't render if no results yet
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-4xl mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-6 text-white">Model Responses</h2>

      {optimizedPrompt && (
        <div className="mb-6 p-4 bg-gray-700 rounded-lg">
          <h3 className="text-lg font-medium text-indigo-300 mb-2">Optimized Prompt Used:</h3>
          <p className="text-gray-300 whitespace-pre-wrap font-mono text-sm">{optimizedPrompt}</p>
        </div>
      )}

      <div className="space-y-6">
        {Object.entries(modelResults).map(([modelName, result]) => (
          <div key={modelName} className="bg-gray-700 p-5 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-3 text-indigo-400">{modelName}</h3>
            {result.loading && (
              <div className="flex items-center justify-center h-24">
                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
                <p className="ml-3 text-gray-300">Loading response...</p>
              </div>
            )}
            {result.error && (
              <div className="p-3 bg-red-700 border border-red-900 rounded-md">
                <p className="text-sm text-white">
                  <span className="font-semibold">Error:</span> {result.error}
                </p>
              </div>
            )}
            {result.output && !result.loading && !result.error && (
              <div className="prose prose-sm prose-invert max-w-none text-gray-200 whitespace-pre-wrap">
                {result.output}
              </div>
            )}
             {!result.loading && !result.error && !result.output && (
              <p className="text-gray-500 italic">No output received or output was empty.</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Results;