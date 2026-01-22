import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import { HelmetProvider } from 'react-helmet-async';
import DetailPlaceholderPage from './DetailPlaceholderPage';

describe('DetailPlaceholderPage', () => {
  it('renders content with ID and SEO title', async () => {
    render(
      <HelmetProvider>
        <MemoryRouter initialEntries={['/details/test-id']}>
          <Routes>
            <Route path="/details/:id" element={<DetailPlaceholderPage />} />
          </Routes>
        </MemoryRouter>
      </HelmetProvider>
    );

    expect(screen.getByText(/Content Detail: test-id/i)).toBeInTheDocument();
    
    // Wait for Helmet to update the title
    await new Promise(resolve => setTimeout(resolve, 100));
    expect(document.title).toContain('Content Detail: test-id');
  });
});
