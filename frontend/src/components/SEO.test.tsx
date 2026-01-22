import { render, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import SEO from './SEO';

describe('SEO Component', () => {
  it('renders title and meta tags', async () => {
    render(
      <SEO 
        title="Test Page" 
        description="This is a test description" 
      />
    );

    await waitFor(() => {
      expect(document.title).toContain('Test Page');
      expect(document.title).toContain('Darren "Dazbo" Lester');
      
      const metaDescription = document.querySelector('meta[name="description"]');
      expect(metaDescription).toHaveAttribute('content', 'This is a test description');
      
      const ogTitle = document.querySelector('meta[property="og:title"]');
      expect(ogTitle).toHaveAttribute('content', expect.stringContaining('Test Page'));
    });
  });

  it('renders JSON-LD when provided', async () => {
    const jsonLdData = {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "Darren Lester"
    };

    render(
      <SEO 
        title="Home" 
        description="Home page"
        jsonLd={jsonLdData}
      />
    );

    await waitFor(() => {
      // Note: React 19 does not hoist script tags by default, so it might be in the body container
      // But we just check if it exists in the document
      const script = document.querySelector('script[type="application/ld+json"]');
      expect(script).toBeInTheDocument();
      expect(script?.textContent).toBe(JSON.stringify(jsonLdData));
    });
  });
});
