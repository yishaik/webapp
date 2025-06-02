import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ModelSelector from '../ModelSelector';

const mockAvailableModels = [
  // Copied from ModelSelector.js for consistency in tests, or could be imported if exported
  { id: "gpt-4.1", name: "GPT-4.1 (OpenAI)", category: "OpenAI" },
  { id: "claude-opus-4", name: "Claude Opus 4 (Anthropic)", category: "Anthropic" },
  { id: "grok-3", name: "Grok-3 (xAI)", category: "xAI" },
  { id: "gemini-2.5-pro", name: "Gemini 2.5 Pro (Google)", category: "Google" },
];


describe('ModelSelector Component', () => {
  test('renders categories and model checkboxes', () => {
    render(<ModelSelector onSelectModels={() => {}} isLoading={false} recommendedModels={[]} />);

    expect(screen.getByText('OpenAI')).toBeInTheDocument();
    expect(screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i)).toBeInTheDocument();

    expect(screen.getByText('Anthropic')).toBeInTheDocument();
    expect(screen.getByLabelText(/Claude Opus 4 \(Anthropic\)/i)).toBeInTheDocument();

    expect(screen.getByText('xAI')).toBeInTheDocument();
    expect(screen.getByLabelText(/Grok-3 \(xAI\)/i)).toBeInTheDocument();

    expect(screen.getByText('Google')).toBeInTheDocument();
    expect(screen.getByLabelText(/Gemini 2.5 Pro \(Google\)/i)).toBeInTheDocument();

    expect(screen.getByRole('button', { name: /Get Model Responses/i })).toBeInTheDocument();
  });

  test('allows selecting and deselecting models', () => {
    render(<ModelSelector onSelectModels={() => {}} isLoading={false} recommendedModels={[]} />);
    const gptCheckbox = screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i);
    const claudeCheckbox = screen.getByLabelText(/Claude Opus 4 \(Anthropic\)/i);

    fireEvent.click(gptCheckbox);
    expect(gptCheckbox).toBeChecked();
    fireEvent.click(claudeCheckbox);
    expect(claudeCheckbox).toBeChecked();

    fireEvent.click(gptCheckbox);
    expect(gptCheckbox).not.toBeChecked();
  });

  test('calls onSelectModels with selected model IDs when form is submitted', () => {
    const mockOnSelectModels = jest.fn();
    render(<ModelSelector onSelectModels={mockOnSelectModels} isLoading={false} recommendedModels={[]} />);

    const gptCheckbox = screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i);
    const grokCheckbox = screen.getByLabelText(/Grok-3 \(xAI\)/i);
    fireEvent.click(gptCheckbox); // Select GPT-4.1
    fireEvent.click(grokCheckbox); // Select Grok-3

    const submitButton = screen.getByRole('button', { name: /Get Model Responses/i });
    fireEvent.click(submitButton);

    // The component passes the 'id' of the model
    expect(mockOnSelectModels).toHaveBeenCalledWith(['gpt-4.1', 'grok-3']);
  });

  test('submit button is disabled if no models are selected', () => {
    render(<ModelSelector onSelectModels={() => {}} isLoading={false} recommendedModels={[]} />);
    const submitButton = screen.getByRole('button', { name: /Get Model Responses/i });
    expect(submitButton).toBeDisabled();

    const gptCheckbox = screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i);
    fireEvent.click(gptCheckbox); // Select one
    expect(submitButton).not.toBeDisabled();

    fireEvent.click(gptCheckbox); // Deselect
    expect(submitButton).toBeDisabled();
  });

  test('shows alert if trying to submit with no models (optional, based on current implementation)', () => {
    // Current implementation has an alert. If removed, this test needs adjustment.
    const mockAlert = jest.spyOn(window, 'alert').mockImplementation(() => {});
    render(<ModelSelector onSelectModels={() => {}} isLoading={false} recommendedModels={[]} />);

    const submitButton = screen.getByRole('button', { name: /Get Model Responses/i });
    fireEvent.click(submitButton); // Click while disabled (or enable then click with none)

    // If button is truly disabled, it won't submit. Test the alert part if it can be submitted.
    // The current ModelSelector enables button once a model is selected.
    // If we ensure it can be clicked (e.g. by not disabling it initially), then alert would be called.
    // For this test, let's assume the button is clickable for the sake of testing the alert path.
    // Or, better, test that onSelectModels is NOT called.
    const mockOnSelect = jest.fn();
    render(<ModelSelector onSelectModels={mockOnSelect} isLoading={false} recommendedModels={[]} />);
    fireEvent.click(screen.getByRole('button', { name: /Get Model Responses/i }));
    expect(mockAlert).toHaveBeenCalledWith("Please select at least one model.");
    expect(mockOnSelect).not.toHaveBeenCalled();
    mockAlert.mockRestore();

  });


  test('disables checkboxes and button when isLoading is true', () => {
    render(<ModelSelector onSelectModels={() => {}} isLoading={true} recommendedModels={[]} />);

    const gptCheckbox = screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i);
    expect(gptCheckbox).toBeDisabled();

    const submitButton = screen.getByRole('button', { name: /Processing.../i });
    expect(submitButton).toBeDisabled();
  });

  test('highlights recommended models', () => {
    const recommendations = ["GPT-4.1 (OpenAI)", "Grok-3 (xAI)"];
    render(<ModelSelector onSelectModels={() => {}} isLoading={false} recommendedModels={recommendations} />);

    const gptLabel = screen.getByLabelText(/GPT-4.1 \(OpenAI\)/i).closest('label');
    expect(gptLabel).toHaveClass('border-green-500');
    expect(screen.getByText("(Recommended)", { selector: 'span.text-green-400', exact: false })).toBeInTheDocument();

    const claudeLabel = screen.getByLabelText(/Claude Opus 4 \(Anthropic\)/i).closest('label');
    expect(claudeLabel).not.toHaveClass('border-green-500');

    const grokLabel = screen.getByLabelText(/Grok-3 \(xAI\)/i).closest('label');
    expect(grokLabel).toHaveClass('border-green-500');
  });
});
