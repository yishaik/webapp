import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

// Basic Authentication credentials
// For development, you can set these here or, better, use environment variables.
// The backend is configured with default "testuser:testpass" if not set in backend/.env
// IMPORTANT: In a production app, never hardcode credentials.
// This token will be generated based on username/password for each request if not using axios default auth.
// However, axios default auth is simpler for this project setup.
const AUTH_USERNAME = process.env.REACT_APP_AUTH_USERNAME || 'testuser';
const AUTH_PASSWORD = process.env.REACT_APP_AUTH_PASSWORD || 'testpass';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  auth: { // Axios will automatically create the Basic Auth header
    username: AUTH_USERNAME,
    password: AUTH_PASSWORD,
  },
});

// Interceptor to log requests (optional, for debugging)
apiClient.interceptors.request.use(request => {
  console.log('Starting Request:', request.method ? request.method.toUpperCase() : '', request.url, request.data || '');
  return request;
});

// Interceptor to log responses (optional, for debugging)
apiClient.interceptors.response.use(response => {
  console.log('Response:', response.status, response.data);
  return response;
}, error => {
  console.error('API Error:', error.response ? { status: error.response.status, data: error.response.data, headers: error.response.headers } : error.message);
  return Promise.reject(error);
});

/**
 * Generates questionnaire based on a base prompt.
 * Corresponds to backend POST /generate_questionnaire
 * Request body: { base_prompt: string }
 * Response: { questions: Array<string> }
 */
export const generateQuestionnaire = async (basePrompt) => {
  const response = await apiClient.post('/generate_questionnaire', { base_prompt: basePrompt });
  return response.data;
};

/**
 * Submits the base prompt and questionnaire answers.
 * Corresponds to backend POST /submit_questionnaire
 * Request body: { base_prompt: string, responses: Array<{question: string, answer: string}> }
 * Response: PromptReadWithDetails schema
 */
export const submitQuestionnaire = async (basePrompt, responses) => {
  const payload = {
    base_prompt: basePrompt,
    responses: responses,
  };
  const response = await apiClient.post('/submit_questionnaire', payload);
  return response.data;
};

/**
 * Recommends models based on base prompt and questionnaire answers.
 * Corresponds to backend POST /recommend_models
 * Request body: { base_prompt: string, questionnaire_responses: Array<{question: string, answer: string}> }
 * Response: { models: Array<string> }
 */
export const recommendModels = async (basePrompt, responses) => {
  const payload = {
    base_prompt: basePrompt,
    questionnaire_responses: responses,
  };
  const response = await apiClient.post('/recommend_models', payload);
  return response.data;
};

/**
 * Optimizes a prompt based on base prompt, questionnaire answers, and target model.
 * Corresponds to backend POST /optimize_prompt
 * Request body: { base_prompt: string, questionnaire_responses: Array<{question: string, answer: string}>, target_model: string }
 * Response: { optimized_prompt: string }
 */
export const optimizePrompt = async (basePrompt, responses, targetModel) => {
  const payload = {
    base_prompt: basePrompt,
    questionnaire_responses: responses,
    target_model: targetModel,
  };
  const response = await apiClient.post('/optimize_prompt', payload);
  return response.data;
};

/**
 * Gets a response from a specified LLM.
 * Corresponds to backend POST /get_model_response
 * Request body: ModelInteractionRequest schema
 * Response: ModelInteractionResponse schema
 */
export const getModelResponse = async (payload) => {
  // Payload should match ModelInteractionRequest schema:
  // { prompt_id?: number, base_prompt?: string, questionnaire_responses?: Array<{q,a}>, model_name: string, optimized_prompt_override?: string }
  const response = await apiClient.post('/get_model_response', payload);
  return response.data;
};

/**
 * Fetches a list of all prompts from history.
 * Corresponds to backend GET /history/prompts
 * Response: List[PromptRead]
 */
export const getHistoryList = async (skip = 0, limit = 100) => {
  const response = await apiClient.get('/history/prompts', { params: { skip, limit } });
  return response.data;
};

/**
 * Fetches details for a specific prompt from history.
 * Corresponds to backend GET /history/prompt/{prompt_id}
 * Response: PromptReadWithDetails
 */
export const getHistoryDetail = async (promptId) => {
  const response = await apiClient.get(`/history/prompt/${promptId}`);
  return response.data;
};

// Exporting individual functions is often preferred for better tree-shaking and explicit usage.
// If 'default apiClient' was used, then it would be: import apiClient from './api'; apiClient.generateQuestionnaire(...);
// With named exports: import { generateQuestionnaire } from './api'; generateQuestionnaire(...);
