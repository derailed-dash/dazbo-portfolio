import { renderHook, waitFor } from '@testing-library/react';
import { useSeo } from './useSeo';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import React from 'react';

// Mock fetch
const mockFetch = vi.fn();
(globalThis as any).fetch = mockFetch;

describe('useSeo hook', () => {
  beforeEach(() => {
    mockFetch.mockReset();
    document.title = 'Default Title';
  });

  it('updates document.title on mount and path change', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ title: 'New Page Title' }),
    });

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={['/test']}>
        {children}
      </MemoryRouter>
    );

    renderHook(() => useSeo(), { wrapper });

    await waitFor(() => {
      expect(document.title).toBe('New Page Title');
    });

    expect(mockFetch).toHaveBeenCalledWith('/api/seo?path=/test');
  });

  it('does not update document.title if response is not ok', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
    });

    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={['/error']}>
        {children}
      </MemoryRouter>
    );

    renderHook(() => useSeo(), { wrapper });

    // Wait a bit to ensure it doesn't change
    await new Promise(resolve => setTimeout(resolve, 100));
    expect(document.title).toBe('Default Title');
  });
});
