import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PromptInput from '../PromptInput';

describe('PromptInput Component', () => {
  test('renders textarea and button', () => {
    render(<PromptInput onSubmit={() => {}} isLoading={false} />);
    expect(screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Generate Questionnaire/i })).toBeInTheDocument();
  });

  test('allows typing in textarea', () => {
    render(<PromptInput onSubmit={() => {}} isLoading={false} />);
    const textarea = screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...');
    fireEvent.change(textarea, { target: { value: 'Test prompt' } });
    expect(textarea.value).toBe('Test prompt');
  });

  test('calls onSubmit prop with prompt value when form is submitted', () => {
    const mockOnSubmit = jest.fn();
    render(<PromptInput onSubmit={mockOnSubmit} isLoading={false} />);

    const textarea = screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...');
    fireEvent.change(textarea, { target: { value: 'A valid prompt' } });

    const button = screen.getByRole('button', { name: /Generate Questionnaire/i });
    fireEvent.click(button);

    expect(mockOnSubmit).toHaveBeenCalledWith('A valid prompt');
  });

  test('does not call onSubmit if prompt is empty or only whitespace', () => {
    const mockOnSubmit = jest.fn();
    render(<PromptInput onSubmit={mockOnSubmit} isLoading={false} />);

    const button = screen.getByRole('button', { name: /Generate Questionnaire/i });
    fireEvent.click(button); // Submit with empty prompt
    expect(mockOnSubmit).not.toHaveBeenCalled();

    const textarea = screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...');
    fireEvent.change(textarea, { target: { value: '   ' } }); // Submit with whitespace
    fireEvent.click(button);
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('disables textarea and button when isLoading is true', () => {
    render(<PromptInput onSubmit={() => {}} isLoading={true} />);

    const textarea = screen.getByPlaceholderText('e.g., Explain quantum computing in simple terms...');
    expect(textarea).toBeDisabled();

    const button = screen.getByRole('button', { name: /Loading.../i });
    expect(button).toBeDisabled();
  });

  test('shows "Loading..." text on button when isLoading is true', () => {
    render(<PromptInput onSubmit={() => {}} isLoading={true} />);
    expect(screen.getByRole('button', { name: /Loading.../i })).toBeInTheDocument();
  });
});
