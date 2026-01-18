import React, { useState } from 'react';
import { Button, Card, Form, InputGroup } from 'react-bootstrap';
import { MessageSquare, Send, X, Bot } from 'lucide-react';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => setIsOpen(!isOpen);

  return (
    <div className="fixed-bottom p-4 d-flex flex-column align-items-end" style={{ zIndex: 1050 }}>
      {isOpen && (
        <Card 
          className="mb-3 shadow-lg border-primary" 
          style={{ width: '350px', height: '450px', borderRadius: '16px', overflow: 'hidden' }}
        >
          <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center py-3">
            <div className="d-flex align-items-center gap-2">
              <Bot size={20} />
              <span className="fw-bold">Dazbo Assistant</span>
            </div>
            <X size={20} style={{ cursor: 'pointer' }} onClick={toggleChat} />
          </Card.Header>
          <Card.Body className="d-flex flex-column bg-light overflow-auto p-3">
            <div className="mb-3">
              <div className="bg-white p-3 rounded-3 shadow-sm mb-2" style={{ maxWidth: '85%' }}>
                <p className="mb-0 small">Hi! I'm Dazbo's AI assistant. Ask me anything about his projects, blogs, or experience!</p>
              </div>
              <div className="text-muted smallest text-end px-2" style={{ fontSize: '0.7rem' }}>Just now</div>
            </div>
            <div className="mt-auto text-center text-muted py-4">
              <p className="small italic">Chat functionality coming soon...</p>
            </div>
          </Card.Body>
          <Card.Footer className="bg-white border-top-0 p-3">
            <InputGroup>
              <Form.Control
                placeholder="Type a message..."
                disabled
                aria-label="Chat input"
              />
              <Button variant="primary" disabled>
                <Send size={18} />
              </Button>
            </InputGroup>
          </Card.Footer>
        </Card>
      )}
      
      <Button 
        variant="primary" 
        className="rounded-circle shadow-lg d-flex align-items-center justify-content-center p-0" 
        style={{ width: '60px', height: '60px' }}
        onClick={toggleChat}
        aria-label="Toggle chat"
      >
        {isOpen ? <X size={28} /> : <MessageSquare size={28} />}
      </Button>
    </div>
  );
};

export default ChatWidget;
