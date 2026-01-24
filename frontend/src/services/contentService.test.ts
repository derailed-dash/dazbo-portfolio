import { describe, it, expect, vi, beforeEach } from 'vitest';
import { getBlogs, getProjects, getContentBySlug } from './contentService';
import apiClient from './api';
import type { Mock } from 'vitest';

// Mock the api module
vi.mock('./api', () => ({
  default: {
    get: vi.fn(),
  },
}));

describe('contentService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('getBlogs fetches data from /blogs', async () => {
    const mockData = [{ id: '1', title: 'Blog 1' }];
    (apiClient.get as Mock).mockResolvedValueOnce({ data: mockData });

    const result = await getBlogs();
    expect(apiClient.get).toHaveBeenCalledWith('/api/blogs');
    expect(result).toEqual(mockData);
  });

  it('getProjects fetches data from /projects', async () => {
    const mockData = [{ id: '1', title: 'Project 1' }];
    (apiClient.get as Mock).mockResolvedValueOnce({ data: mockData });

    const result = await getProjects();
    expect(apiClient.get).toHaveBeenCalledWith('/api/projects');
    expect(result).toEqual(mockData);
  });

  it('getContentBySlug fetches data from /content/:slug', async () => {
    const mockData = { id: 'about', title: 'About Me', body: 'Body' };
    (apiClient.get as Mock).mockResolvedValueOnce({ data: mockData });

    const result = await getContentBySlug('about');
    expect(apiClient.get).toHaveBeenCalledWith('/api/content/about');
    expect(result).toEqual(mockData);
  });
});