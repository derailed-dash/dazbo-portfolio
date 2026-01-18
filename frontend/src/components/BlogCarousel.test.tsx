import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import BlogCarousel from './BlogCarousel';
import * as contentService from '../services/contentService';

vi.mock('../services/contentService');

describe('BlogCarousel', () => {
  it('renders loading spinner then content', async () => {
    (contentService.getBlogs as any).mockResolvedValueOnce([
      { title: 'Test Blog', url: 'http://test.com', tags: ['tech'] }
    ]);

    render(<BlogCarousel />);
    
    expect(screen.getByRole('status')).toBeInTheDocument(); // Spinner

    await waitFor(() => {
      expect(screen.getAllByText('Test Blog').length).toBeGreaterThan(0);
    });
    expect(screen.queryByRole('status')).not.toBeInTheDocument();
  });

  it('renders error message on failure', async () => {
    (contentService.getBlogs as any).mockRejectedValueOnce(new Error('Fetch failed'));

    render(<BlogCarousel />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load blogs/i)).toBeInTheDocument();
    });
  });
});
