import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import { getBlogs, getProjects } from './contentService';

vi.mock('axios');

describe('contentService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('getBlogs fetches data from /blogs', async () => {
    const mockData = [{ id: '1', title: 'Blog 1' }];
    (axios.get as any).mockResolvedValueOnce({ data: mockData });

    const result = await getBlogs();
    expect(axios.get).toHaveBeenCalledWith('/blogs');
    expect(result).toEqual(mockData);
  });

  it('getProjects fetches data from /projects', async () => {
    const mockData = [{ id: '1', title: 'Project 1' }];
    (axios.get as any).mockResolvedValueOnce({ data: mockData });

    const result = await getProjects();
    expect(axios.get).toHaveBeenCalledWith('/projects');
    expect(result).toEqual(mockData);
  });
});
