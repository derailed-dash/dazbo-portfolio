import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App Routing', () => {
  it('renders HomePage on default route', () => {
    // We don't need to wrap App in MemoryRouter because App already contains a BrowserRouter
    // But testing App directly might be tricky if it has BrowserRouter inside.
    // Usually we test a component that uses useRoutes or similar.
    // For now, let's just ensure App renders without crashing.
    render(<App />);
    expect(screen.getByText(/Welcome to Dazbo Portfolio/i)).toBeInTheDocument();
  });
});
