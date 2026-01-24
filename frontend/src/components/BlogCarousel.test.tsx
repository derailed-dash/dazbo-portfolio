import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import BlogCarousel from './BlogCarousel';
import { getBlogs } from '../services/contentService';
import type { Mock } from 'vitest';

// Mock the services
vi.mock('../services/contentService', () => ({
  getBlogs: vi.fn(),
}));

// Mock ShowcaseCarousel to isolate BlogCarousel
vi.mock('./ShowcaseCarousel', () => ({
  default: ({ title, items }: { title: string; items: unknown[] }) => (
    <div data-testid="showcase-carousel">
      <h2>{title}</h2>
      <div data-testid="item-count">{items.length}</div>
    </div>
  ),
}));

describe('BlogCarousel', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    (getBlogs as Mock).mockReturnValue(new Promise(() => {})); // Never resolves
    render(<BlogCarousel />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders ShowcaseCarousel with blogs when fetched successfully', async () => {
    const mockBlogs = [
      { id: '1', title: 'Blog 1', url: 'https://test.com/1', platform: 'Medium' },
      { id: '2', title: 'Blog 2', url: 'https://test.com/2', platform: 'Dev.to' },
    ];
    (getBlogs as Mock).mockResolvedValue(mockBlogs);

    render(<BlogCarousel />);

    await waitFor(() => {
      expect(screen.getByTestId('showcase-carousel')).toBeInTheDocument();
      expect(screen.getByText('Latest Blog Posts')).toBeInTheDocument();
      expect(screen.getByTestId('item-count')).toHaveTextContent('2');
    });
  });
});
