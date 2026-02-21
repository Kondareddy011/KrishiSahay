import { QueryRequest, QueryResponse } from './api';

const CACHE_KEY = 'krishisahay_offline_cache';
const MAX_CACHE_SIZE = 10;

interface CacheEntry {
  query: string;
  language: string;
  response: QueryResponse;
  timestamp: number;
}

export const offlineCache = {
  save(request: QueryRequest, response: QueryResponse): void {
    try {
      const cache = this.getAll();
      const newEntry: CacheEntry = {
        query: request.query.toLowerCase().trim(),
        language: request.language || 'en',
        response,
        timestamp: Date.now(),
      };

      const existingIndex = cache.findIndex(
        (entry) => entry.query === newEntry.query && entry.language === newEntry.language
      );

      if (existingIndex !== -1) {
        cache[existingIndex] = newEntry;
      } else {
        cache.unshift(newEntry);
        if (cache.length > MAX_CACHE_SIZE) {
          cache.pop();
        }
      }

      localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
    } catch (error) {
      console.error('Error saving to offline cache:', error);
    }
  },

  get(request: QueryRequest): QueryResponse | null {
    try {
      const cache = this.getAll();
      const queryKey = request.query.toLowerCase().trim();
      const language = request.language || 'en';

      const entry = cache.find(
        (item) => item.query === queryKey && item.language === language
      );

      if (entry) {
        return { ...entry.response, source: 'offline' };
      }

      return null;
    } catch (error) {
      console.error('Error retrieving from offline cache:', error);
      return null;
    }
  },

  getAll(): CacheEntry[] {
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      return cached ? JSON.parse(cached) : [];
    } catch (error) {
      console.error('Error reading offline cache:', error);
      return [];
    }
  },

  clear(): void {
    try {
      localStorage.removeItem(CACHE_KEY);
    } catch (error) {
      console.error('Error clearing offline cache:', error);
    }
  },
};
