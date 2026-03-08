import { describe, it, expect, vi, beforeEach } from 'vitest';
import { injectSeoTags } from '../utils/seoInjector';

declare var global: any;

// Mock the global fetch function
global.fetch = vi.fn();

const mockHtml = `
<!doctype html>
<html lang="en">
  <head>
    <!-- __SEO_TAGS__ -->
  </head>
  <body></body>
</html>
`;

describe('seoInjector', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('should inject title and description if backend returns data', async () => {
    // Mock the fetch response
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: async () => ({
        head_tags: '<title>Injected Title</title><meta property="og:title" content="Injected Title" />',
      }),
    });

    const result = await injectSeoTags(mockHtml, '/about');

    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/seo?path=/about');
    expect(result).toContain('<title>Injected Title</title><meta property="og:title" content="Injected Title" />');
    expect(result).not.toContain('<!-- __SEO_TAGS__ -->');
  });

  it('should return original HTML if fetch fails', async () => {
    (global.fetch as any).mockRejectedValue(new Error('Network error'));

    const result = await injectSeoTags(mockHtml, '/about');

    expect(result).toBe(mockHtml);
    expect(result).toContain('<!-- __SEO_TAGS__ -->');
  });

  it('should return original HTML if backend returns non-ok response', async () => {
    (global.fetch as any).mockResolvedValue({
      ok: false,
    });

    const result = await injectSeoTags(mockHtml, '/about');

    expect(result).toBe(mockHtml);
    expect(result).toContain('<!-- __SEO_TAGS__ -->');
  });
});
