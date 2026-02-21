export interface QueryRequest {
  query: string;
  language?: string;
  region?: string;
  season?: string;
  lat?: number;
  lon?: number;
}

export interface QueryResponse {
  answer: string;
  source: string;
  category?: string;
}

export interface FeedbackRequest {
  query: string;
  answer: string;
  feedback: 'positive' | 'negative';
}

export interface AppFeedbackRequest {
  message: string;
  rating?: number;
  page?: string;
}

export interface AppFeedbackItem {
  id: number;
  rating: number | null;
  message: string;
  page: string | null;
  created_at: string;
}

export interface ImageAnalysisRequest {
  image: File;
  language?: string;
  query?: string;
}

// In dev: /api is proxied to localhost:8000. In prod: use backend URL.
const API_BASE_URL = import.meta.env.VITE_API_URL ?? (import.meta.env.DEV ? '/api' : 'http://localhost:8000');

export const apiService = {
  async askQuestion(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: request.query,
          language: request.language || 'en',
          region: request.region,
          season: request.season,
          lat: request.lat,
          lon: request.lon,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network response was not ok' }));
        throw new Error(errorData.detail || 'Network response was not ok');
      }

      const data: QueryResponse = await response.json();
      return data;
    } catch (error) {
      console.error('API Error:', error);
      const msg = String(error instanceof Error ? error.message : '');
      if (msg.includes('fetch') || msg.includes('NetworkError') || msg.includes('Failed to fetch'))
        throw new Error('Cannot reach the backend. Please start it: cd backend && python main.py');
      throw error;
    }
  },

  async submitFeedback(feedback: FeedbackRequest): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: feedback.query,
          answer: feedback.answer,
          feedback: feedback.feedback,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit feedback');
      }
    } catch (error) {
      console.error('Feedback Error:', error);
      throw error;
    }
  },

  async submitAppFeedback(payload: AppFeedbackRequest): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/app-feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Failed to submit app feedback' }));
      throw new Error(errorData.detail || 'Failed to submit app feedback');
    }
  },

  async getRecentAppFeedback(limit: number = 20): Promise<AppFeedbackItem[]> {
    const response = await fetch(`${API_BASE_URL}/app-feedback?limit=${encodeURIComponent(String(limit))}`);
    if (!response.ok) {
      return [];
    }
    const data = await response.json().catch(() => ({ items: [] }));
    return Array.isArray(data.items) ? data.items : [];
  },

  async analyzeImage(request: ImageAnalysisRequest): Promise<QueryResponse> {
    try {
      const formData = new FormData();
      formData.append('image', request.image);
      formData.append('language', request.language || 'en');
      if (request.query) {
        formData.append('query', request.query);
      }

      const response = await fetch(`${API_BASE_URL}/analyze-image`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Network response was not ok' }));
        throw new Error(errorData.detail || 'Failed to analyze image');
      }

      const data: QueryResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Image Analysis Error:', error);
      throw error;
    }
  },

  async getRecentQueries(limit: number = 10): Promise<any[]> {
    // This would require a new endpoint on backend
    // For now, return empty array as offline cache handles this
    return [];
  },
};
