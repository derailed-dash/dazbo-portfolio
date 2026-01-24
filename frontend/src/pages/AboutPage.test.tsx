import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import AboutPage from './AboutPage';
import { getContentBySlug } from '../services/contentService';
import { MemoryRouter } from 'react-router-dom';
import type { Mock } from 'vitest';

// Mock the services
vi.mock('../services/contentService', () => ({
  getContentBySlug: vi.fn(),
}));

// Mock the SEO component to avoid layout issues in tests
vi.mock('../components/SEO', () => ({
  default: () => <div data-testid="seo-mock">SEO</div>,
}));

describe('AboutPage', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    (getContentBySlug as Mock).mockReturnValue(new Promise(() => {})); // Never resolves
    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders content when fetched successfully', async () => {
    const mockContent = {
      title: 'About Me',
      body: '# Professional Bio\nThis is my bio.',
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('About Darren: Professional Profile & Expertise')).toBeInTheDocument();
      expect(screen.getByText('Professional Bio')).toBeInTheDocument();
      expect(screen.getByText('This is my bio.')).toBeInTheDocument();
    });
  });

  it('renders error message on fetch failure', async () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    (getContentBySlug as Mock).mockRejectedValueOnce(new Error('Fetch failed'));

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Failed to load about page content/i)).toBeInTheDocument();
    });
    
    consoleSpy.mockRestore();
  });
});
