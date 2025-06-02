import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Results from '../Results';

describe('Results Component', () => {
  const mockOptimizedPrompt = "This is the optimized prompt that was used.";

  test('renders nothing if modelResults is empty', () => {
    const { container } = render(<Results modelResults={{}} optimizedPrompt="" />);
    expect(container).toBeEmptyDOMElement();
  });

  test('renders optimized prompt if provided', () => {
    const modelResults = { "GPT-4.1": { output: "Test output", error: null, loading: false } };
    render(<Results modelResults={modelResults} optimizedPrompt={mockOptimizedPrompt} />);
    expect(screen.getByText('Optimized Prompt Used:')).toBeInTheDocument();
    expect(screen.getByText(mockOptimizedPrompt)).toBeInTheDocument();
  });

  test('does not render optimized prompt section if not provided', () => {
    const modelResults = { "GPT-4.1": { output: "Test output", error: null, loading: false } };
    render(<Results modelResults={modelResults} optimizedPrompt={null} />);
    expect(screen.queryByText('Optimized Prompt Used:')).not.toBeInTheDocument();
  });

  test('renders results for a single model successfully', () => {
    const modelResults = {
      "GPT-4.1": { output: "Successful response from GPT.", error: null, loading: false },
    };
    render(<Results modelResults={modelResults} optimizedPrompt={mockOptimizedPrompt} />);

    expect(screen.getByText('GPT-4.1')).toBeInTheDocument();
    expect(screen.getByText('Successful response from GPT.')).toBeInTheDocument();
    expect(screen.queryByText(/Loading response.../i)).not.toBeInTheDocument();
    expect(screen.queryByText(/Error:/i)).not.toBeInTheDocument();
  });

  test('renders results for multiple models', () => {
    const modelResults = {
      "GPT-4.1": { output: "GPT response.", error: null, loading: false },
      "Claude Sonnet 4": { output: "Claude response.", error: null, loading: false },
    };
    render(<Results modelResults={modelResults} optimizedPrompt={mockOptimizedPrompt} />);

    expect(screen.getByText('GPT-4.1')).toBeInTheDocument();
    expect(screen.getByText('GPT response.')).toBeInTheDocument();
    expect(screen.getByText('Claude Sonnet 4')).toBeInTheDocument();
    expect(screen.getByText('Claude response.')).toBeInTheDocument();
  });

  test('shows loading state for a model', () => {
    const modelResults = {
      "GPT-4.1": { output: null, error: null, loading: true },
    };
    render(<Results modelResults={modelResults} optimizedPrompt={mockOptimizedPrompt} />);

    expect(screen.getByText('GPT-4.1')).toBeInTheDocument();
    expect(screen.getByText(/Loading response.../i)).toBeInTheDocument();
  });

  test('shows error message for a model', () => {
    const modelResults = {
      "GPT-4.1": { output: null, error: "Network Error", loading: false },
    };
    render(<Results modelResults={modelResults} optimizedPrompt={mockOptimizedPrompt} />);

    expect(screen.getByText('GPT-4.1')).toBeInTheDocument();
    expect(screen.getByText(/Error: Network Error/i)).toBeInTheDocument();
  });

  test('handles mixed states (loading, error, success)', () => {
    const modelResults = {
      "GPT-4.1": { output: "GPT success.", error: null, loading: false },
      "Claude Sonnet 4": { output: null, error: "Claude failed.", loading: false },
      "Grok-3 Mini": { output: null, error: null, loading: true },
    };
    render(<Results modelResults={modelResults} optimizedPrompt={mockOptimizedPrompt} />);

    // GPT
    expect(screen.getByText('GPT-4.1')).toBeInTheDocument();
    expect(screen.getByText('GPT success.')).toBeInTheDocument();

    // Claude
    expect(screen.getByText('Claude Sonnet 4')).toBeInTheDocument();
    expect(screen.getByText(/Error: Claude failed./i)).toBeInTheDocument();

    // Grok
    expect(screen.getByText('Grok-3 Mini')).toBeInTheDocument();
    expect(screen.getByText(/Loading response.../i)).toBeInTheDocument();
  });

  test('renders "No output received" message if output is empty or null but no error and not loading', () => {
    const modelResults = {
      "GPT-4.1": { output: "", error: null, loading: false }, // Empty string output
      "Claude Sonnet 4": { output: null, error: null, loading: false } // Null output
    };
    render(<Results modelResults={modelResults} optimizedPrompt={mockOptimizedPrompt} />);

    // Check for GPT-4.1
    const gptResults = screen.getByText("GPT-4.1").closest('div');
    expect(gptResults).toHaveTextContent("No output received or output was empty.");

    // Check for Claude Sonnet 4
    const claudeResults = screen.getByText("Claude Sonnet 4").closest('div');
    expect(claudeResults).toHaveTextContent("No output received or output was empty.");
  });
});
