import { http, HttpResponse } from 'msw';

// Define the base URL for your API, ensure it matches what your app uses in tests
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const handlers = [
  // Handler for generating questionnaire
  http.post(`${API_BASE_URL}/generate_questionnaire`, async ({ request }) => {
    const reqBody = await request.json();
    if (reqBody.base_prompt === 'error_prompt') {
      return HttpResponse.json({ detail: 'Failed to generate questionnaire (mocked error)' }, { status: 500 });
    }
    return HttpResponse.json({
      questions: ['Mock question 1 based on: ' + reqBody.base_prompt, 'Mock question 2?'],
    });
  }),

  // Handler for submitting questionnaire
  http.post(`${API_BASE_URL}/submit_questionnaire`, async ({ request }) => {
    const reqBody = await request.json();
    return HttpResponse.json({
      id: 123, // Mocked prompt ID
      base_prompt: reqBody.base_prompt,
      questionnaire_responses: reqBody.responses.map((r, i) => ({ ...r, id: i + 1, prompt_id: 123 })),
      model_outputs: [],
      timestamp: new Date().toISOString(),
      user_id: null,
    });
  }),

  // Handler for recommending models
  http.post(`${API_BASE_URL}/recommend_models`, async ({ request }) => {
    const reqBody = await request.json();
    if (reqBody.prompt_id === 999) { // Simulate error for a specific prompt ID
        return HttpResponse.json({ detail: 'Failed to recommend models (mocked error)' }, { status: 500 });
    }
    return HttpResponse.json({
      models: ['GPT-4.1 (Mock)', 'Claude Sonnet 4 (Mock)'],
    });
  }),

  // Handler for getting a model response
  http.post(`${API_BASE_URL}/get_model_response`, async ({ request }) => {
    const reqBody = await request.json();
    if (reqBody.model_name === 'ErrorModel') {
      return HttpResponse.json({ detail: 'LLM API call failed: Error: Mocked error from ErrorModel' }, { status: 502 });
    }
    return HttpResponse.json({
      prompt_id: reqBody.prompt_id,
      model_name: reqBody.model_name,
      output: `Mocked response from ${reqBody.model_name} for prompt ID ${reqBody.prompt_id}`,
      optimized_prompt_used: `Optimized version of prompt for ${reqBody.model_name}`,
    });
  }),

  // Handler for getting history prompts
  http.get(`${API_BASE_URL}/history/prompts`, () => {
    return HttpResponse.json([
      { id: 1, base_prompt: 'History prompt 1', timestamp: new Date().toISOString(), user_id: null },
      { id: 2, base_prompt: 'History prompt 2', timestamp: new Date().toISOString(), user_id: null },
    ]);
  }),

  // Handler for getting history prompt details
  http.get(`${API_BASE_URL}/history/prompt/:promptId`, ({ params }) => {
    const { promptId } = params;
    if (promptId === '999') {
      return HttpResponse.json({ detail: 'Prompt not found (mocked)' }, { status: 404 });
    }
    return HttpResponse.json({
      id: parseInt(promptId),
      base_prompt: `Details for prompt ${promptId}`,
      timestamp: new Date().toISOString(),
      user_id: null,
      questionnaire_responses: [
        { id: 1, prompt_id: parseInt(promptId), question: 'Mock Q1', answer: 'Mock A1' },
      ],
      model_outputs: [
        { id: 1, prompt_id: parseInt(promptId), model_name: 'GPT-4.1 (Mock)', output: 'Output for prompt ' + promptId, timestamp: new Date().toISOString() },
      ],
    });
  }),

  // Catch-all for unhandled requests to warn during tests (optional)
  // http.all(`${API_BASE_URL}/*`, ({request}) => {
  //   console.warn(`Unhandled request in MSW: ${request.method} ${request.url}`);
  //   return HttpResponse.json({ error: 'Unhandled request' }, { status: 501 });
  // }),
];
