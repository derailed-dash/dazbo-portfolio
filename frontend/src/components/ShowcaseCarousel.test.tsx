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
});
