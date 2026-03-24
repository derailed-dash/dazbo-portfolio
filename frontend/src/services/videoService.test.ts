import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from './api';
import { getVideos } from './videoService';

vi.mock('./api');

describe('videoService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('getVideos should fetch and return videos', async () => {
    const mockVideos = [
      {
        id: 'youtube:123',
        title: 'Test Video',
        description: 'Desc',
        video_url: 'https://youtube.com/watch?v=123',
        is_manual: true,
        source_platform: 'youtube'
      }
    ];

    vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockVideos });

    const result = await getVideos();

    expect(apiClient.get).toHaveBeenCalledWith('/api/videos');
    expect(result).toEqual(mockVideos);
  });
});
