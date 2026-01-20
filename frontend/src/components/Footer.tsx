import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Github, Linkedin } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="app-footer py-5 mt-auto">
      <Container>
        <Row className="align-items-center">
          <Col md={6} className="text-center text-md-start mb-3 mb-md-0">
            <p className="mb-0 text-secondary">
              &copy; {currentYear} Dazbo Portfolio. Built with React & FastAPI.
            </p>
          </Col>
          <Col md={6} className="text-center text-md-end">
            <div className="d-flex justify-content-center justify-content-md-end gap-4 footer-icons">
              <a 
                href="https://github.com/derailed-dash" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-white hover-primary"
                aria-label="GitHub"
              >
                <Github size={20} />
              </a>
              <a 
                href="https://www.linkedin.com/in/darren-lester-architect/" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-white hover-primary"
                aria-label="LinkedIn"
              >
                <Linkedin size={20} />
              </a>
            </div>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
