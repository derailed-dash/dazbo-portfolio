import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import VideoCarousel from './VideoCarousel';
import { getVideos } from '../services/videoService';
import type { Mock } from 'vitest';

// Mock the services
vi.mock('../services/videoService', () => ({
  getVideos: vi.fn(),
}));

// Mock ShowcaseCarousel to isolate VideoCarousel
vi.mock('./ShowcaseCarousel', () => ({
  default: ({ title, items }: { title: string; items: unknown[] }) => (
    <div data-testid="showcase-carousel">
      <h2>{title}</h2>
      <div data-testid="item-count">{items.length}</div>
    </div>
  ),
}));

describe('VideoCarousel', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    (getVideos as Mock).mockReturnValue(new Promise(() => {})); // Never resolves
    render(<VideoCarousel />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders ShowcaseCarousel with videos when fetched successfully', async () => {
    const mockVideos = [
      { id: 'youtube:1', title: 'Video 1', video_url: 'https://youtube.com/1', source_platform: 'youtube', is_manual: true },
      { id: 'youtube:2', title: 'Video 2', video_url: 'https://youtube.com/2', source_platform: 'youtube', is_manual: true },
    ];
    (getVideos as Mock).mockResolvedValue(mockVideos);

    render(<VideoCarousel />);

    await waitFor(() => {
      expect(screen.getByTestId('showcase-carousel')).toBeInTheDocument();
      expect(screen.getByText('Videos & Presentations')).toBeInTheDocument();
      expect(screen.getByTestId('item-count')).toHaveTextContent('2');
    });
  });

  it('renders error message when fetch fails', async () => {
    (getVideos as Mock).mockRejectedValue(new Error('Fetch failed'));
    
    render(<VideoCarousel />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load videos.')).toBeInTheDocument();
    });
  });
});
