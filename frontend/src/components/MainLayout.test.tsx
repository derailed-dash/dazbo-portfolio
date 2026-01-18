import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import MainLayout from './MainLayout';

describe('MainLayout', () => {
  it('renders children content', () => {
    render(
      <BrowserRouter>
        <MainLayout>
          <div data-testid="child">Test Content</div>
        </MainLayout>
      </BrowserRouter>
    );
    expect(screen.getByTestId('child')).toBeInTheDocument();
    expect(screen.getByText(/Test Content/i)).toBeInTheDocument();
  });

  it('renders navbar and footer', () => {
    render(
      <BrowserRouter>
        <MainLayout>
          <div>Content</div>
        </MainLayout>
      </BrowserRouter>
    );
    expect(screen.getAllByText(/Dazbo Portfolio/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Built with React & FastAPI/i)).toBeInTheDocument();
  });
});
