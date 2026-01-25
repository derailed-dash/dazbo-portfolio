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
      // Expect H1 element
      const heading = screen.getByRole('heading', { level: 1, name: 'Heading 1' });
      expect(heading).toBeInTheDocument();

      // Expect Strong tag
      const boldText = screen.getByText('Bold Text');
      expect(boldText.tagName).toBe('STRONG');

      // Expect List Item
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
      // If table is supported, we should see a table row
      // We expect this to fail if GFM is not enabled
      const row = screen.getByRole('row', { name: /Val 1/i });
      expect(row).toBeInTheDocument();
    });
  });
});