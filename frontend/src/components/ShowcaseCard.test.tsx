import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ShowcaseCard from './ShowcaseCard';

describe('ShowcaseCard', () => {
  const props = {
    title: 'Test Project',
    description: 'A test project description.',
    tags: ['react', 'vitest'],
    type: 'project' as const,
    linkUrl: 'https://example.com',
    repoUrl: 'https://github.com/test/repo'
  };

  it('renders title and description', () => {
    render(<ShowcaseCard {...props} />);
    expect(screen.getByText('Test Project')).toBeInTheDocument();
    expect(screen.getByText(/A test project description/i)).toBeInTheDocument();
  });

  it('renders tags', () => {
    render(<ShowcaseCard {...props} />);
    expect(screen.getByText(/react/i)).toBeInTheDocument();
    expect(screen.getByText(/vitest/i)).toBeInTheDocument();
  });

  it('renders action buttons', () => {
    render(<ShowcaseCard {...props} />);
    expect(screen.getByText(/View/i)).toBeInTheDocument();
    expect(screen.getByText(/Code/i)).toBeInTheDocument();
  });
});
