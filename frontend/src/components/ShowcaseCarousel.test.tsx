import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ShowcaseCarousel from './ShowcaseCarousel';

describe('ShowcaseCarousel', () => {
  const items = [
    { id: '1', title: 'Item 1', description: 'Desc 1', type: 'blog' as const },
    { id: '2', title: 'Item 2', description: 'Desc 2', type: 'blog' as const },
  ];

  it('renders the carousel items', () => {
    render(<ShowcaseCarousel items={items} />);
    expect(screen.getAllByText('Item 1').length).toBeGreaterThan(0);
    expect(screen.getAllByText('Item 2').length).toBeGreaterThan(0);
  });

  it('renders section title if provided', () => {
    render(<ShowcaseCarousel items={items} title="Latest Blogs" />);
    expect(screen.getByText('Latest Blogs')).toBeInTheDocument();
  });

  it('limits indicators on mobile when there are many items', () => {
    const manyItems = Array.from({ length: 20 }, (_, i) => ({
      id: `${i}`,
      title: `Item ${i}`,
      description: `Desc ${i}`,
      type: 'blog' as const,
      date: '2023-01-01'
    }));

    const { container } = render(<ShowcaseCarousel items={manyItems} />);
    
    // We expect to replace default Bootstrap indicators with custom ones on mobile
    // Default bootstrap indicators are usually in <div class="carousel-indicators">
    // We will use a custom class for our limited indicators
    const customDots = container.querySelectorAll('.mobile-custom-indicators .indicator-dot');
    
    // With 20 items, default behavior would be 20 dots (if we used default).
    // Our new behavior should show fewer (e.g. 5 or 7).
    expect(customDots.length).toBeGreaterThan(0);
    expect(customDots.length).toBeLessThan(20);
  });

  it('renders standard bootstrap indicators for desktop when needed', () => {
    // 5 items > 4, so desktop should have indicators
    const items = Array.from({ length: 5 }, (_, i) => ({
        id: `${i}`, title: `Item ${i}`, description: 'd', type: 'blog' as const, date: '2023'
    }));
    const { container } = render(<ShowcaseCarousel items={items} />);
    
    // Mobile carousel has indicators={false}.
    // Desktop carousel has indicators={true}.
    // So we expect exactly one .carousel-indicators (from desktop).
    const indicators = container.querySelectorAll('.carousel-indicators');
    expect(indicators.length).toBe(1);
  });
});
