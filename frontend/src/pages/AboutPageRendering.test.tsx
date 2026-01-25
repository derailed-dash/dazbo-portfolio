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

// Mock the SEO component
vi.mock('../components/SEO', () => ({
  default: () => <div data-testid="seo-mock">SEO</div>,
}));

describe('AboutPage Rendering', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders markdown as HTML elements', async () => {
    const mockContent = {
      title: 'About Me',
      body: '# Heading 1\n**Bold Text**\n- List Item',
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      const heading = screen.getByRole('heading', { level: 1, name: 'Heading 1' });
      expect(heading).toBeInTheDocument();
      const boldText = screen.getByText('Bold Text');
      expect(boldText.tagName).toBe('STRONG');
      const listItem = screen.getByText('List Item');
      expect(listItem.tagName).toBe('LI');
    });
  });

  it('renders tables correctly (GFM)', async () => {
    const mockContent = {
      title: 'About Me',
      body: '| Col 1 | Col 2 |\n| --- | --- |\n| Val 1 | Val 2 |',
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      const row = screen.getByRole('row', { name: /Val 1/i });
      expect(row).toBeInTheDocument();
    });
  });

  it('renders user specific content correctly', async () => {
    const mockContent = {
      title: 'About Me',
      body: 'Enterprise Cloud Architect | Google Cloud | Strategist\n\nHi folks. My name is Darren, aka _Dazbo_.',
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Enterprise Cloud Architect/)).toBeInTheDocument();
      const em = screen.getByText('Dazbo');
      expect(em.tagName).toBe('EM');
    });
  });

  it('renders raw syntax if newlines are missing', async () => {
    const mockContent = {
      title: 'About Me',
      body: 'Intro text. ## My USP The convergence of:', // Missing newline before ##
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      // Expect H2 to NOT be present
      const heading = screen.queryByRole('heading', { level: 2, name: /My USP/ });
      expect(heading).not.toBeInTheDocument();
      // Expect raw text
      expect(screen.getByText(/## My USP/)).toBeInTheDocument();
    });
  });

  it('processes literal newlines correctly', async () => {
    const mockContent = {
      title: 'About Me',
      // Simulating Firestore console input where \n might be literal characters
      body: '# Heading\\nContent',
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      // Should find the Heading
      const heading = screen.getByRole('heading', { level: 1, name: 'Heading' });
      expect(heading).toBeInTheDocument();
      // Should find the text in a paragraph (or just text)
      expect(screen.getByText('Content')).toBeInTheDocument();
    });
  });

  it('renders raw HTML correctly', async () => {
    const mockContent = {
      title: 'About Me',
      body: '<img src="test.jpg" alt="Test Image" />',
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      // Expect Image element
      const img = screen.getByRole('img', { name: 'Test Image' });
      expect(img).toBeInTheDocument();
      expect(img).toHaveAttribute('src', 'test.jpg');
    });
  });

  it('renders inline code as styled tags', async () => {
    const mockContent = {
      title: 'About Me',
      body: '`Tag1` `Tag2`',
      last_updated: '2026-01-24T12:00:00Z',
    };
    (getContentBySlug as Mock).mockResolvedValueOnce(mockContent);

    render(
      <MemoryRouter>
        <AboutPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      const tag1 = screen.getByText('Tag1');
      expect(tag1).toHaveClass('glass-tag'); 
    });
  });
});
