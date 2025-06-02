import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'; // Default to localhost:8000

// Basic Authentication credentials (hardcoded for now as per subtask instructions)
const AUTH_USERNAME = 'admin';
const AUTH_PASSWORD = 'password123';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  auth: {
    username: AUTH_USERNAME,
    password: AUTH_PASSWORD,
  },
});

// Interceptor to log requests and responses (optional, for debugging)
apiClient.interceptors.request.use(request => {
  console.log('Starting Request:', request.method.toUpperCase(), request.url, request.data || '');
  return request;
});

apiClient.interceptors.response.use(response => {
  console.log('Response:', response.status, response.data);
  return response;
}, error => {
  console.error('API Error:', error.response || error.message);
  // Return a consistent error object structure if possible, or just re-throw
  // For this project, we'll let the calling code handle the error structure from Axios directly.
  return Promise.reject(error);
});


// API functions
export const generateQuestionnaire = async (basePrompt) => {
  const response = await apiClient.post('/generate_questionnaire', { base_prompt: basePrompt });
  return response.data; // Expects { questions: ["q1", "q2"] }
};

export const submitQuestionnaire = async (basePrompt, responses) // promptId is created by backend now
 => {
  const payload = {
    base_prompt: basePrompt,
    responses: responses, // responses should be: [{ question: string, answer: string }]
  };
  const response = await apiClient.post('/submit_questionnaire', payload);
  return response.data; // Expects PromptReadWithDetails schema (includes id, base_prompt, responses, etc.)
};

export const recommendModels = async (promptId) => {
  const response = await apiClient.post('/recommend_models', { prompt_id: promptId });
  return response.data; // Expects { models: ["model1", "model2"] }
};

export const getModelResponse = async (promptId, modelName) => {
  const response = await apiClient.post('/get_model_response', {
    prompt_id: promptId,
    model_name: modelName,
  });
  return response.data; // Expects { prompt_id, model_name, output, optimized_prompt_used }
};

export const getHistoryPrompts = async (skip = 0, limit = 100) => {
  const response = await apiClient.get('/history/prompts', { params: { skip, limit } });
  return response.data; // Expects List[PromptRead]
};

export const getHistoryPromptDetails = async (promptId) => {
  const response = await apiClient.get(`/history/prompt/${promptId}`);
  return response.data; // Expects PromptReadWithDetails
};

export default apiClient; // Can also export individual functions if preferred.
