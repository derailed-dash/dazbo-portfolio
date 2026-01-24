import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import ChatWidget from './ChatWidget';
import type { Mock } from 'vitest';

describe('ChatWidget', () => {
  beforeEach(() => {
    globalThis.fetch = vi.fn();
    // Mock scrollIntoView
    window.HTMLElement.prototype.scrollIntoView = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

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

  it('sends message and displays streaming response', async () => {
    render(<ChatWidget />);
    
    // Open chat
    fireEvent.click(screen.getByLabelText(/Toggle chat/i));
    
    const mockReader = {
      read: vi.fn()
        .mockResolvedValueOnce({ 
          done: false, 
          value: new TextEncoder().encode('data: {"content": "Hello"}\n\n') 
        })
        .mockResolvedValueOnce({ 
          done: false, 
          value: new TextEncoder().encode('data: {"content": " World"}\n\n') 
        })
        .mockResolvedValueOnce({ done: true }),
      cancel: vi.fn(),
    };

    const mockStream = {
      getReader: () => mockReader,
    };

    (globalThis.fetch as Mock).mockResolvedValue({
      ok: true,
      body: mockStream,
    });

    // Type and send
    const input = screen.getByPlaceholderText(/Type a message/i);
    // Button is inside InputGroup, checking aria-label or role might be tricky if not set explicitly on button
    // The existing code has <Button ...><Send /></Button>
    // I will target by Role button inside the footer or similar, but for now assuming it will be enabled.
    
    // Note: In the current implementation the input and button are disabled.
    // The test expects them to be enabled.
    expect(input).not.toBeDisabled();

    fireEvent.change(input, { target: { value: 'Hi' } });
    
    // Find the send button by aria-label
    const sendButton = screen.getByLabelText(/Send message/i);
    expect(sendButton).not.toBeDisabled();
    
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(globalThis.fetch).toHaveBeenCalledWith('/api/chat/stream', expect.objectContaining({
        method: 'POST',
        body: expect.stringContaining('"message":"Hi"'),
      }));
    });

    // Check if response is displayed
    // "Hello World"
    await waitFor(() => {
        expect(screen.getByText(/Hello World/i)).toBeInTheDocument();
    });
  });

  it('displays error message on 429 Rate Limit Exceeded', async () => {
    render(<ChatWidget />);
    fireEvent.click(screen.getByLabelText(/Toggle chat/i));

    (globalThis.fetch as Mock).mockResolvedValue({
      ok: false,
      status: 429,
    });

    const input = screen.getByPlaceholderText(/Type a message/i);
    fireEvent.change(input, { target: { value: 'Spam' } });
    
    const sendButton = screen.getByLabelText(/Send message/i);
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/You're sending messages too fast/i)).toBeInTheDocument();
    });
  });
});
