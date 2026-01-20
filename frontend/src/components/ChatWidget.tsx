import React, { useState, useRef, useEffect } from 'react';
import { Button, Card, Form, InputGroup, Spinner } from 'react-bootstrap';
import { MessageSquare, Send, X, Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import type { ChatMessage } from '../types';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'bot',
      content: "Hi! I'm Dazbo's AI assistant. Ask me anything about his projects, blogs, or experience!",
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'anonymous-user', // In a real app, this would be a real user ID or session ID
          message: input
        })
      });

      if (response.status === 429) {
        setMessages(prev => [...prev, {
          role: 'bot',
          content: "You're sending messages too fast. Please wait a moment before trying again.",
          timestamp: new Date()
        }]);
        setIsLoading(false);
        return;
      }

      if (!response.ok) throw new Error('Failed to send message');

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      const botMessage: ChatMessage = {
        role: 'bot',
        content: '',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);

      const decoder = new TextDecoder();
      let accumulatedContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) {
                accumulatedContent += data.content;
                setMessages(prev => {
                  const newMessages = [...prev];
                  const lastMessage = newMessages[newMessages.length - 1];
                  if (lastMessage && lastMessage.role === 'bot') {
                    lastMessage.content = accumulatedContent;
                  }
                  return newMessages;
                });
              }
            } catch (err) {
              console.error('Error parsing SSE data:', err);
            }
          }
        }
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        role: 'bot',
        content: "I'm sorry, I encountered an error. Please try again later.",
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed-bottom p-4 d-flex flex-column align-items-end chat-widget-container">
      {isOpen && (
        <Card 
          className="mb-3 shadow-lg border-primary chat-widget-card" 
        >
          <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center py-3">
            <div className="d-flex align-items-center gap-2">
              <Bot size={20} />
              <span className="fw-bold">Dazbo Assistant</span>
            </div>
            <X size={20} style={{ cursor: 'pointer' }} onClick={toggleChat} />
          </Card.Header>
          <Card.Body className="d-flex flex-column bg-light overflow-auto p-3">
            {messages.map((msg, idx) => (
              <div key={idx} className={`mb-3 d-flex flex-column ${msg.role === 'user' ? 'align-items-end' : 'align-items-start'}`}>
                <div 
                  className={`p-3 rounded-3 shadow-sm chat-message-bubble ${msg.role === 'user' ? 'bg-primary text-white' : 'bg-white'}`} 
                >
                  {msg.role === 'user' ? (
                    <p className="mb-0">{msg.content}</p>
                  ) : (
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  )}
                </div>
                <div className="text-muted smallest px-2 mt-1 chat-timestamp">
                  {msg.role === 'bot' ? <Bot size={12} className="me-1" /> : <User size={12} className="me-1" />}
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}
            {isLoading && messages[messages.length - 1]?.role !== 'bot' && (
              <div className="mb-3">
                <div className="bg-white p-3 rounded-3 shadow-sm d-flex align-items-center gap-2 chat-loading-dots">
                  <Spinner animation="grow" size="sm" variant="primary" />
                  <Spinner animation="grow" size="sm" variant="primary" />
                  <Spinner animation="grow" size="sm" variant="primary" />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </Card.Body>
          <Card.Footer className="bg-white border-top p-3">
            <Form onSubmit={handleSend}>
              <InputGroup>
                <Form.Control
                  placeholder="Type a message..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={isLoading}
                  aria-label="Chat input"
                />
                <Button 
                  variant="primary" 
                  type="submit" 
                  disabled={isLoading || !input.trim()}
                  aria-label="Send message"
                >
                  {isLoading ? <Spinner animation="border" size="sm" /> : <Send size={18} />}
                </Button>
              </InputGroup>
            </Form>
          </Card.Footer>
        </Card>
      )}
      
      <Button 
        variant="primary" 
        className="rounded-circle shadow-lg d-flex align-items-center justify-content-center p-0 chat-widget-toggle-btn" 
        onClick={toggleChat}
        aria-label="Toggle chat"
      >
        {isOpen ? <X size={28} /> : <MessageSquare size={28} />}
      </Button>
    </div>
  );
};

export default ChatWidget;
