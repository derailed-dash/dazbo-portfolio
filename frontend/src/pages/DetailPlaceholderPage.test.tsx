import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import DetailPlaceholderPage from './DetailPlaceholderPage';

describe('DetailPlaceholderPage', () => {
  it('renders content with ID and SEO title', async () => {
    render(
      <MemoryRouter initialEntries={['/details/test-id']}>
        <Routes>
          <Route path="/details/:id" element={<DetailPlaceholderPage />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText(/Content Detail: test-id/i)).toBeInTheDocument();
    
    // Wait for Title update
    await waitFor(() => {
      expect(document.title).toContain('Content Detail: test-id');
    });
  });
});
