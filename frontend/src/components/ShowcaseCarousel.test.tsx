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
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    expect(screen.getByText('Item 2')).toBeInTheDocument();
  });

  it('renders section title if provided', () => {
    render(<ShowcaseCarousel items={items} title="Latest Blogs" />);
    expect(screen.getByText('Latest Blogs')).toBeInTheDocument();
  });
});
