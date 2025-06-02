import React, { useState, useEffect } from 'react';

const Questionnaire = ({ questions, onSubmit, isLoading }) => {
  const [answers, setAnswers] = useState({});

  // Initialize answers state when questions change
  useEffect(() => {
    const initialAnswers = {};
    questions.forEach((q, index) => {
      initialAnswers[`q${index}`] = '';
    });
    setAnswers(initialAnswers);
  }, [questions]);

  const handleChange = (questionIndex, value) => {
    setAnswers(prevAnswers => ({
      ...prevAnswers,
      [`q${questionIndex}`]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Transform answers into the required format: { question: string, answer: string }[]
    const formattedAnswers = questions.map((question, index) => ({
      question: question,
      answer: answers[`q${index}`] || '', // Ensure answer is empty string if not filled
    }));
    onSubmit(formattedAnswers);
  };

  if (!questions || questions.length === 0) {
    return null; // Don't render if no questions
  }

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-6 text-white">Answer these questions to refine your prompt:</h2>
      <form onSubmit={handleSubmit}>
        {questions.map((question, index) => (
          <div key={index} className="mb-6">
            <label htmlFor={`q${index}`} className="block text-sm font-medium text-gray-300 mb-2">
              {question}
            </label>
            <input
              type="text"
              id={`q${index}`}
              value={answers[`q${index}`] || ''}
              onChange={(e) => handleChange(index, e.target.value)}
              className="w-full px-4 py-3 border border-gray-700 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-150"
              disabled={isLoading}
            />
          </div>
        ))}
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 transition duration-150 disabled:opacity-50"
          disabled={isLoading}
        >
          {isLoading ? 'Submitting...' : 'Submit Answers & Get Recommendations'}
        </button>
      </form>
    </div>
  );
};

export default Questionnaire;
