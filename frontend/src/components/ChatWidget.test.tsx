import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ChatWidget from './ChatWidget';

describe('ChatWidget', () => {
  it('renders the floating button initially', () => {
    render(<ChatWidget />);
    expect(screen.getByLabelText(/Toggle chat/i)).toBeInTheDocument();
    expect(screen.queryByText(/Dazbo Assistant/i)).not.toBeInTheDocument();
  });

  it('toggles the chat window when button is clicked', () => {
    render(<ChatWidget />);
    const button = screen.getByLabelText(/Toggle chat/i);
    
    fireEvent.click(button);
    expect(screen.getByText(/Dazbo Assistant/i)).toBeInTheDocument();
    
    fireEvent.click(button);
    expect(screen.queryByText(/Dazbo Assistant/i)).not.toBeInTheDocument();
  });
});
