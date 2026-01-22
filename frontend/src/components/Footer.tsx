import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Github, Linkedin, Code2 } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="app-footer py-5 mt-auto">
      <Container>
        <Row className="align-items-center">
          <Col md={6} className="text-center text-md-start mb-3 mb-md-0">
            <p className="mb-0 text-secondary">
              &copy; {currentYear} Darren Lester.
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
              <a 
                href="https://medium.com/@derailed.dash" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-white hover-primary"
                aria-label="Medium"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  width="20"
                  height="20"
                  fill="currentColor"
                >
                  <path d="M13.54 12a6.8 6.8 0 01-6.77 6.82A6.8 6.8 0 010 12a6.8 6.8 0 016.77-6.82A6.8 6.8 0 0113.54 12zM20.96 12c0 3.54-1.51 6.42-3.38 6.42-1.87 0-3.39-2.88-3.39-6.42s1.52-6.42 3.39-6.42 3.38 2.88 3.38 6.42M24 12c0 3.17-.53 5.75-1.19 5.75-.66 0-1.19-2.58-1.19-5.75s.53-5.75 1.19-5.75C23.47 6.25 24 8.83 24 12z" />
                </svg>
              </a>
              <a 
                href="https://dev.to/deraileddash" 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-white hover-primary"
                aria-label="Dev.to"
              >
                <Code2 size={20} />
              </a>
            </div>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
