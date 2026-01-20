import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import apiClient from './api';
import MockAdapter from 'axios-mock-adapter';

describe('API Client Interceptor', () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(apiClient);
    vi.spyOn(console, 'warn').mockImplementation(() => {});
  });

  afterEach(() => {
    mock.restore();
    vi.restoreAllMocks();
  });

  it('logs a warning on 429 response', async () => {
    mock.onGet('/test-429').reply(429);

    try {
      await apiClient.get('/test-429');
    } catch (error) {
      // Ignore error
    }

    expect(console.warn).toHaveBeenCalledWith(
      expect.stringContaining('You are sending requests too fast')
    );
  });
});
