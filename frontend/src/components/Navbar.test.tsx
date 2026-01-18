import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import AppNavbar from './Navbar';

describe('AppNavbar', () => {
  it('renders the brand name', () => {
    render(
      <BrowserRouter>
        <AppNavbar />
      </BrowserRouter>
    );
    expect(screen.getByText(/Dazbo/i)).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    render(
      <BrowserRouter>
        <AppNavbar />
      </BrowserRouter>
    );
    expect(screen.getByText(/Home/i)).toBeInTheDocument();
    expect(screen.getByText(/Blogs/i)).toBeInTheDocument();
    expect(screen.getByText(/Projects/i)).toBeInTheDocument();
  });
});
