import { render, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { HelmetProvider } from 'react-helmet-async';
import SEO from './SEO';

describe('SEO Component', () => {
  it('renders title and meta tags', async () => {
    const context = {};
    render(
      <HelmetProvider context={context}>
        <SEO 
          title="Test Page" 
          description="This is a test description" 
        />
      </HelmetProvider>
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
    const context = {};
    const jsonLdData = {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "Darren Lester"
    };

    render(
      <HelmetProvider context={context}>
        <SEO 
          title="Home" 
          description="Home page"
          jsonLd={jsonLdData}
        />
      </HelmetProvider>
    );

    await waitFor(() => {
      const script = document.querySelector('script[type="application/ld+json"]');
      expect(script).toBeInTheDocument();
      expect(script?.textContent).toBe(JSON.stringify(jsonLdData));
    });
  });
});
