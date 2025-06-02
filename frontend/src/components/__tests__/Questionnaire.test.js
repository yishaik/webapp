import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Questionnaire from '../Questionnaire';

describe('Questionnaire Component', () => {
  const mockQuestions = [
    "What is the primary goal?",
    "Who is the target audience?",
    "Any specific tone to use?"
  ];

  test('renders nothing if no questions are provided', () => {
    const { container } = render(<Questionnaire questions={[]} onSubmit={() => {}} isLoading={false} />);
    expect(container).toBeEmptyDOMElement();
  });

  test('renders questions and input fields', () => {
    render(<Questionnaire questions={mockQuestions} onSubmit={() => {}} isLoading={false} />);

    mockQuestions.forEach(q => {
      expect(screen.getByText(q)).toBeInTheDocument();
    });
    expect(screen.getAllByRole('textbox').length).toBe(mockQuestions.length);
    expect(screen.getByRole('button', { name: /Submit Answers & Get Recommendations/i })).toBeInTheDocument();
  });

  test('allows typing in answer fields', () => {
    render(<Questionnaire questions={mockQuestions} onSubmit={() => {}} isLoading={false} />);
    const firstInput = screen.getAllByRole('textbox')[0];
    fireEvent.change(firstInput, { target: { value: 'Achieve world peace.' } });
    expect(firstInput.value).toBe('Achieve world peace.');
  });

  test('calls onSubmit with formatted answers when form is submitted', () => {
    const mockOnSubmit = jest.fn();
    render(<Questionnaire questions={mockQuestions} onSubmit={mockOnSubmit} isLoading={false} />);

    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: 'Answer 1' } });
    fireEvent.change(inputs[1], { target: { value: 'Answer 2' } });
    // Leaving inputs[2] empty

    const submitButton = screen.getByRole('button', { name: /Submit Answers & Get Recommendations/i });
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith([
      { question: mockQuestions[0], answer: 'Answer 1' },
      { question: mockQuestions[1], answer: 'Answer 2' },
      { question: mockQuestions[2], answer: '' }, // Empty answer for the third question
    ]);
  });

  test('disables inputs and button when isLoading is true', () => {
    render(<Questionnaire questions={mockQuestions} onSubmit={() => {}} isLoading={true} />);

    screen.getAllByRole('textbox').forEach(input => {
      expect(input).toBeDisabled();
    });

    const button = screen.getByRole('button', { name: /Submitting.../i });
    expect(button).toBeDisabled();
  });

  test('shows "Submitting..." text on button when isLoading is true', () => {
    render(<Questionnaire questions={mockQuestions} onSubmit={() => {}} isLoading={true} />);
    expect(screen.getByRole('button', { name: /Submitting.../i })).toBeInTheDocument();
  });

  test('updates internal answers state correctly when questions prop changes', () => {
    const { rerender } = render(
      <Questionnaire questions={["Old question 1"]} onSubmit={() => {}} isLoading={false} />
    );
    let inputs = screen.getAllByRole('textbox');
    expect(inputs.length).toBe(1);
    fireEvent.change(inputs[0], { target: { value: 'Old answer' } });
    expect(inputs[0].value).toBe('Old answer');

    // Rerender with new questions
    const newMockQuestions = ["New question A", "New question B"];
    rerender(
      <Questionnaire questions={newMockQuestions} onSubmit={() => {}} isLoading={false} />
    );

    inputs = screen.getAllByRole('textbox');
    expect(inputs.length).toBe(2);
    expect(screen.getByText("New question A")).toBeInTheDocument();
    expect(screen.getByText("New question B")).toBeInTheDocument();
    // Check that answers are reset for new questions
    expect(inputs[0].value).toBe('');
    expect(inputs[1].value).toBe('');
  });
});
