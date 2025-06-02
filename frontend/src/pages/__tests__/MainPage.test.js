import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import MainPage from '../MainPage';
import { server } from '../../mocks/server'; // MSW server
import { handlers } from '../../mocks/handlers'; // MSW handlers
import { http, HttpResponse } from 'msw'; // For overriding handlers

// MSW server setup is in setupTests.js

describe('MainPage Integration Tests', () => {
  beforeEach(() => {
    // Reset handlers to default before each test if any test overrides them
    server.resetHandlers(...handlers);
  });

  test('full user flow: submit prompt, answer questionnaire, select model, get response', async () => {
    render(<MainPage />);

    // 1. Submit base prompt
    const promptInput = screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...');
    fireEvent.change(promptInput, { target: { value: 'Test User Prompt' } });
    fireEvent.click(screen.getByRole('button', { name: /Generate Questionnaire/i }));

    // 2. Wait for questionnaire to appear (mocked API call)
    await waitFor(() => {
      expect(screen.getByText('Mock question 1 based on: Test User Prompt')).toBeInTheDocument();
    });
    expect(screen.getByText('Mock question 2?')).toBeInTheDocument();

    // 3. Answer questionnaire
    const answerInputs = screen.getAllByRole('textbox'); // two questions = two textboxes
    fireEvent.change(answerInputs[0], { target: { value: 'Answer to Q1' } });
    fireEvent.change(answerInputs[1], { target: { value: 'Answer to Q2' } });
    fireEvent.click(screen.getByRole('button', { name: /Submit Answers & Get Recommendations/i }));

    // 4. Wait for model recommendations and selector to appear
    await waitFor(() => {
      expect(screen.getByText('Model Recommendations')).toBeInTheDocument();
      expect(screen.getByText('GPT-4.1 (Mock)')).toBeInTheDocument(); // From mock recommendations
    });
    expect(screen.getByText('Model Selector')).toBeInTheDocument(); // Check if ModelSelector is rendered
    expect(screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i)).toBeInTheDocument(); // A model from selector

    // 5. Select a model
    const modelCheckbox = screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i);
    fireEvent.click(modelCheckbox);

    // 6. Submit model selection
    fireEvent.click(screen.getByRole('button', { name: /Get Model Responses/i }));

    // 7. Wait for results to appear
    await waitFor(() => {
      // Check for the model name in results, which comes from the ModelSelector's list.
      // The mock response uses the friendly name.
      expect(screen.getByText('GPT-4.1 (OpenAI)')).toBeInTheDocument();
    });
    // Check for the mocked output
    expect(screen.getByText('Mocked response from GPT-4.1 (OpenAI) for prompt ID 123')).toBeInTheDocument();
    // Check if optimized prompt is displayed
    expect(screen.getByText('Optimized Prompt Used:')).toBeInTheDocument();
    expect(screen.getByText('Optimized version of prompt for GPT-4.1 (OpenAI)')).toBeInTheDocument();
  });

  test('handles error when generating questionnaire', async () => {
    // Override MSW handler for this specific test
    server.use(
      http.post('http://localhost:8000/generate_questionnaire', () => {
        return HttpResponse.json({ detail: 'Mocked server error during questionnaire generation' }, { status: 500 });
      })
    );

    render(<MainPage />);
    const promptInput = screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...');
    fireEvent.change(promptInput, { target: { value: 'trigger error' } });
    fireEvent.click(screen.getByRole('button', { name: /Generate Questionnaire/i }));

    await waitFor(() => {
      expect(screen.getByText(/An error occurred:/i)).toBeInTheDocument();
      expect(screen.getByText(/Failed to generate questionnaire. Please try again./i)).toBeInTheDocument();
      expect(screen.getByText(/Mocked server error during questionnaire generation/i)).toBeInTheDocument();
    });
  });

  test('handles error when submitting questionnaire', async () => {
    render(<MainPage />);
    // Step 1: Submit prompt (success)
    fireEvent.change(screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...'), { target: { value: 'Good Prompt' } });
    fireEvent.click(screen.getByRole('button', { name: /Generate Questionnaire/i }));
    await screen.findByText('Mock question 1 based on: Good Prompt'); // Wait for questionnaire

    // Override handler for submit_questionnaire to simulate error
    server.use(
      http.post('http://localhost:8000/submit_questionnaire', () => {
        return HttpResponse.json({ detail: 'Mocked error submitting questionnaire' }, { status: 500 });
      })
    );

    // Step 2: Submit questionnaire (fail)
    fireEvent.click(screen.getByRole('button', { name: /Submit Answers & Get Recommendations/i }));

    await waitFor(() => {
      expect(screen.getByText(/Failed to submit questionnaire. Please try again./i)).toBeInTheDocument();
      expect(screen.getByText(/Mocked error submitting questionnaire/i)).toBeInTheDocument();
    });
  });

  test('handles error when fetching model response', async () => {
    render(<MainPage />);
    // Go through the flow to model selection
    fireEvent.change(screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...'), { target: { value: 'Prompt for model error' } });
    fireEvent.click(screen.getByRole('button', { name: /Generate Questionnaire/i }));
    await screen.findByText('Mock question 1 based on: Prompt for model error');
    fireEvent.click(screen.getByRole('button', { name: /Submit Answers & Get Recommendations/i }));
    await screen.findByText('Model Recommendations'); // Wait for next step

    // Select a model that will cause an error (using the mock handler's logic)
    const errorModelCheckbox = screen.getByLabelText(/GPT-4.1 Mini \(OpenAI\)/i); // Assuming this is a valid model in component
    fireEvent.click(errorModelCheckbox);

    // Override handler for get_model_response
    server.use(
      http.post('http://localhost:8000/get_model_response', async ({request}) => {
        const reqBody = await request.json();
        // Use the specific model name from ModelSelector which is "gpt-4.1-mini" for its id
        if (reqBody.model_name === 'gpt-4.1-mini') {
          return HttpResponse.json({ detail: 'LLM API call failed: Error: Mocked Mini Error' }, { status: 502 });
        }
        // Fallback to default mock for other models if any, though only one is selected here.
        return HttpResponse.json({ output: `Default mock for ${reqBody.model_name}` });
      })
    );

    fireEvent.click(screen.getByRole('button', { name: /Get Model Responses/i }));

    await waitFor(() => {
      // The Results component should display the error for the specific model
      expect(screen.getByText('GPT-4.1 Mini (OpenAI)')).toBeInTheDocument(); // Model title
      expect(screen.getByText(/Error: Mocked Mini Error/i)).toBeInTheDocument();
    });
  });

});
