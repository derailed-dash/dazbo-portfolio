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


});
