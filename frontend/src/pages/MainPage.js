import React, { useState, useEffect } from 'react';
import PromptInput from '../components/PromptInput';
import Questionnaire from '../components/Questionnaire';
import ModelRecommendations from '../components/ModelRecommendations';
import ModelSelector from '../components/ModelSelector';
import Results from '../components/Results';
import * as api from '../services/api'; // Assuming api.js exports named functions

const MainPage = () => {
  // State variables
  const [basePrompt, setBasePrompt] = useState('');
  const [questions, setQuestions] = useState([]);
  // questionnaireAnswers are managed internally by Questionnaire component for now
  const [currentPromptId, setCurrentPromptId] = useState(null);
  const [recommendedModels, setRecommendedModels] = useState([]);
  // selectedModels are managed by ModelSelector, passed up on submit
  const [modelResults, setModelResults] = useState({}); // { modelName: { output, error, loading } }
  const [optimizedPromptForResults, setOptimizedPromptForResults] = useState('');

  // Loading states
  const [isGeneratingQuestions, setIsGeneratingQuestions] = useState(false);
  const [isSubmittingQuestionnaire, setIsSubmittingQuestionnaire] = useState(false);
  const [isRecommendingModels, setIsRecommendingModels] = useState(false);
  const [isFetchingModelResponses, setIsFetchingModelResponses] = useState(false); // Overall flag for any model response

  const [error, setError] = useState(null); // For general page errors

  // UI Flow Control
  const [currentStep, setCurrentStep] = useState(1); // 1: Prompt, 2: Questionnaire, 3: Models+Results

  const handlePromptSubmit = async (prompt) => {
    setIsGeneratingQuestions(true);
    setError(null);
    try {
      setBasePrompt(prompt);
      const data = await api.generateQuestionnaire(prompt);
      setQuestions(data.questions || []);
      setCurrentStep(2);
    } catch (err) {
      setError('Failed to generate questionnaire. Please try again. Details: ' + (err.response?.data?.detail || err.message));
      setQuestions([]); // Clear any old questions
    } finally {
      setIsGeneratingQuestions(false);
    }
  };

  const handleQuestionnaireSubmit = async (answers) => {
    setIsSubmittingQuestionnaire(true);
    setError(null);
    try {
      // The backend's /submit_questionnaire now creates the prompt.
      // It expects base_prompt and responses.
      const promptData = await api.submitQuestionnaire(basePrompt, answers);
      setCurrentPromptId(promptData.id);
      // After submitting questionnaire, get model recommendations
      // Pass basePrompt and answers to fetchRecommendations
      await fetchRecommendations(basePrompt, answers);
      setCurrentStep(3);
    } catch (err) {
      setError('Failed to submit questionnaire. Please try again. Details: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsSubmittingQuestionnaire(false);
    }
  };

  // Modified to accept basePrompt and answers directly
  const fetchRecommendations = async (currentBasePrompt, currentAnswers) => {
    setIsRecommendingModels(true);
    try {
      // api.recommendModels now expects (basePrompt, responses)
      const data = await api.recommendModels(currentBasePrompt, currentAnswers);
      setRecommendedModels(data.models || []);
    } catch (err) {
      // Non-critical error, so don't block UI, just log or show minor warning
      console.error('Failed to fetch model recommendations:', err);
      setRecommendedModels([]);
    } finally {
      setIsRecommendingModels(false);
    }
  };

  const handleModelSelectionSubmit = async (selectedModelFriendlyNames) => {
    if (!currentPromptId) {
      setError("Cannot get model responses without a submitted prompt ID.");
      return;
    }
    setIsFetchingModelResponses(true);
    setError(null);
    setOptimizedPromptForResults(''); // Clear previous optimized prompt

    // Initialize results state for selected models
    const initialResults = {};
    selectedModelFriendlyNames.forEach(name => {
      initialResults[name] = { output: null, error: null, loading: true };
    });
    setModelResults(initialResults);

    let firstSuccessfulOptimizedPrompt = '';

    for (const modelFriendlyName of selectedModelFriendlyNames) {
      try {
        // Updated payload for api.getModelResponse
        const payload = {
          prompt_id: currentPromptId,
          model_name: modelFriendlyName,
          // base_prompt and questionnaire_responses are optional if prompt_id is present,
          // as backend can re-fetch/re-optimize.
          // Not sending them simplifies frontend if prompt_id is the primary reference.
        };
        const response = await api.getModelResponse(payload);

        if (response.optimized_prompt_used && !firstSuccessfulOptimizedPrompt) {
            firstSuccessfulOptimizedPrompt = response.optimized_prompt_used;
            setOptimizedPromptForResults(firstSuccessfulOptimizedPrompt);
        }
        setModelResults(prev => ({
          ...prev,
          [modelFriendlyName]: { output: response.output, error: null, loading: false },
        }));
      } catch (err) {
        const errorMsg = err.response?.data?.detail || err.message || 'An unknown error occurred';
        setModelResults(prev => ({
          ...prev,
          [modelFriendlyName]: { output: null, error: errorMsg, loading: false },
        }));
      }
    }
    setIsFetchingModelResponses(false);
  };

  return (
    <div className="space-y-12">
      {error && (
        <div className="bg-red-800 border border-red-600 text-white p-4 rounded-md shadow-lg">
          <p className="font-semibold">An error occurred:</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {currentStep >= 1 && (
        <PromptInput onSubmit={handlePromptSubmit} isLoading={isGeneratingQuestions} />
      )}

      {currentStep >= 2 && questions.length > 0 && (
        <Questionnaire
          questions={questions}
          onSubmit={handleQuestionnaireSubmit}
          isLoading={isSubmittingQuestionnaire}
        />
      )}

      {currentStep >= 3 && (
        <>
          <ModelRecommendations
            recommendations={recommendedModels}
            isLoading={isRecommendingModels}
          />
          <ModelSelector
            onSelectModels={handleModelSelectionSubmit}
            isLoading={isFetchingModelResponses} // Disable while any model is fetching
            recommendedModels={recommendedModels} // To highlight them
          />
        </>
      )}

      {currentStep >=3 && Object.keys(modelResults).length > 0 && (
        <Results modelResults={modelResults} optimizedPrompt={optimizedPromptForResults} />
      )}
    </div>
  );
};

export default MainPage;
