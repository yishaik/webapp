import * as api from '../api'; // Import your API service
import { server } from '../../mocks/server'; // Import MSW server
import { http, HttpResponse } from 'msw'; // For overriding handlers if needed

// MSW server setup is in setupTests.js (beforeAll, afterEach, afterAll)

describe('API Service', () => {
  // Test generateQuestionnaire
  it('generateQuestionnaire successfully fetches questions', async () => {
    const basePrompt = "test prompt";
    const data = await api.generateQuestionnaire(basePrompt);
    // This assertion depends on the mock handler in src/mocks/handlers.js
    expect(data.questions).toEqual(['Mock question 1 based on: ' + basePrompt, 'Mock question 2?']);
  });

  it('generateQuestionnaire handles server error', async () => {
    server.use(
      http.post('http://localhost:8000/generate_questionnaire', () => {
        return HttpResponse.json({ detail: 'Internal server error' }, { status: 500 });
      })
    );
    await expect(api.generateQuestionnaire("any prompt")).rejects.toThrow();
    // More specific error checking can be done if your apiClient normalizes errors
  });

  // Test submitQuestionnaire
  it('submitQuestionnaire successfully posts data and gets prompt details', async () => {
    const basePrompt = "my base prompt";
    const responses = [{ question: "Q1", answer: "A1" }];
    const data = await api.submitQuestionnaire(basePrompt, responses);
    expect(data.id).toBe(123); // From mock handler
    expect(data.base_prompt).toBe(basePrompt);
    expect(data.questionnaire_responses[0].answer).toBe("A1");
  });

  // Test recommendModels
  it('recommendModels successfully fetches recommendations', async () => {
    const promptId = 123;
    const data = await api.recommendModels(promptId);
    expect(data.models).toEqual(['GPT-4.1 (Mock)', 'Claude Sonnet 4 (Mock)']);
  });

  // Test getModelResponse
  it('getModelResponse successfully fetches model output', async () => {
    const promptId = 123;
    const modelName = "TestModel";
    const data = await api.getModelResponse(promptId, modelName);
    expect(data.prompt_id).toBe(promptId);
    expect(data.model_name).toBe(modelName);
    expect(data.output).toContain("Mocked response from TestModel");
  });

  it('getModelResponse handles LLM error correctly', async () => {
     server.use(
      http.post('http://localhost:8000/get_model_response', () => {
        return HttpResponse.json({ detail: 'LLM API call failed: Error: Specific error' }, { status: 502 });
      })
    );
    await expect(api.getModelResponse(123, "ErrorModelFromTest")).rejects.toThrow();
  });

  // Test getHistoryPrompts
  it('getHistoryPrompts successfully fetches history', async () => {
    const data = await api.getHistoryPrompts();
    expect(data.length).toBe(2); // From mock handler
    expect(data[0].base_prompt).toBe('History prompt 1');
  });

  // Test getHistoryPromptDetails
  it('getHistoryPromptDetails successfully fetches details', async () => {
    const promptId = 456; // A non-error mock ID
    const data = await api.getHistoryPromptDetails(promptId);
    expect(data.id).toBe(promptId);
    expect(data.base_prompt).toBe(`Details for prompt ${promptId}`);
    expect(data.questionnaire_responses.length).toBe(1);
  });

  it('getHistoryPromptDetails handles 404 not found', async () => {
    // The default handler for /history/prompt/:promptId already returns 404 for id '999'
    // So we can test that.
    await expect(api.getHistoryPromptDetails('999')).rejects.toThrow();
    // This will throw because axios throws on non-2xx by default.
    // We can also check the error object if needed:
    // try {
    //   await api.getHistoryPromptDetails('999');
    // } catch (error) {
    //   expect(error.response.status).toBe(404);
    //   expect(error.response.data.detail).toBe('Prompt not found (mocked)');
    // }
  });


  // Example of testing authentication header (conceptual)
  // This requires more advanced spying on axios instance or MSW request details.
  // For simplicity, we assume the `apiClient` in api.js is configured correctly.
  // If direct testing of auth headers is needed, one might:
  // 1. Not use a global axios instance but pass one or configure it per call.
  // 2. Use msw's `req.headers.get('Authorization')` in a custom handler.
  it('requests include basic authentication header', async () => {
    // Override a handler to check for Authorization header
    let authHeader = null;
    server.use(
      http.get('http://localhost:8000/history/prompts', ({request}) => {
        authHeader = request.headers.get('Authorization');
        return HttpResponse.json([]); // Minimal valid response
      })
    );

    await api.getHistoryPrompts();

    // Basic auth format is "Basic base64(username:password)"
    // For admin:password123 -> Basic YWRtaW46cGFzc3dvcmQxMjM=
    expect(authHeader).toBe('Basic YWRtaW46cGFzc3dvcmQxMjM=');
  });

});
