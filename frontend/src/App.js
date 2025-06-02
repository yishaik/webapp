import React, { useState } from 'react';
import PromptInput from './components/PromptInput';
import ModelSelector from './components/ModelSelector';
import Results from './components/Results';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [promptData, setPromptData] = useState({
    basePrompt: '',
    responses: [],
    selectedModels: [],
    results: []
  });

  const nextStep = () => setCurrentStep(currentStep + 1);
  const prevStep = () => setCurrentStep(currentStep - 1);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Prompt Builder & Optimizer
        </h1>
        
        <div className="flex justify-center mb-8">
          <div className="flex items-center space-x-4">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  currentStep >= step ? 'bg-blue-500 text-white' : 'bg-gray-300 text-gray-600'
                }`}>
                  {step}
                </div>
                {step < 3 && <div className="w-8 h-1 bg-gray-300 mx-2"></div>}
              </div>
            ))}
          </div>
        </div>

        {currentStep === 1 && (
          <PromptInput 
            promptData={promptData} 
            setPromptData={setPromptData}
            nextStep={nextStep}
          />
        )}
        
        {currentStep === 2 && (
          <ModelSelector 
            promptData={promptData} 
            setPromptData={setPromptData}
            nextStep={nextStep}
            prevStep={prevStep}
          />
        )}
        
        {currentStep === 3 && (
          <Results 
            promptData={promptData} 
            setPromptData={setPromptData}
            prevStep={prevStep}
          />
        )}
      </div>
    </div>
  );
}

export default App;