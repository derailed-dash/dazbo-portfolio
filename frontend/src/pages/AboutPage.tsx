import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Spinner, Alert, Button } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useSeo } from '../hooks/useSeo';
import { getContentBySlug } from '../services/contentService';
import type { Content } from '../types';

const AboutPage: React.FC = () => {
  useSeo();
  const [content, setContent] = useState<Content | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const data = await getContentBySlug('about');
        setContent(data);
      } catch (err) {
        console.error('Error fetching about content:', err);
        setError('Failed to load about page content. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </Container>
    );
  }

  if (error || !content) {
    return (
      <Container className="py-5">
        <Alert variant="danger">{error || 'Content not found.'}</Alert>
      </Container>
    );
  }

  return (
    <>
      <div className="hero-wrapper position-relative text-white mb-4">
        <div className="position-absolute top-0 start-0 w-100 h-100 hero-banner"></div>
        <Container className="position-relative py-2">
          <div className="d-flex flex-column align-items-start gap-2">
            <img 
              src="/images/dazbo-polo-removebg.png" 
              alt="Dazbo" 
              style={{ height: '140px', width: 'auto', objectFit: 'contain' }}
              className="rounded transition-transform hover-scale-sm"
            />
            <Button 
              variant="link" 
              className="text-white text-decoration-none p-0 d-flex align-items-center btn-glass px-3 py-1 rounded-pill"
              onClick={() => navigate(-1)}
              style={{ width: 'fit-content' }}
            >
              <ArrowLeft size={18} className="me-2" />
              Back
            </Button>
          </div>
        </Container>

      </div>


      <Container className="mb-5 pb-5">
        {/* Title BELOW Banner - Matching Carousel Style */}
        <Row className="mb-4">
          <Col className="text-center">
            <h2 className="h3 mb-1 fw-bold">About Darren: Professional Profile & Expertise</h2>
          </Col>
        </Row>

        <Row>
          <Col lg={9} className="mx-auto">
            <div 
              className="markdown-content p-4 p-md-5 shadow-sm rounded"
              style={{
                background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: 'var(--md-sys-color-on-background)'
              }}
            >
              {/* Replace literal \n with actual newlines to fix Firestore console input issues */}
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]} 
                rehypePlugins={[rehypeRaw]}
                components={{
                  code: ({className, children, ...props}) => {
                    // Apply glass tag style to inline code blocks (those without language- class)
                    const match = /language-(\w+)/.exec(className || '');
                    const isInline = !match;
                    return (
                      <code 
                        className={`${className || ''} ${isInline ? 'glass-tag' : ''}`} 
                        {...props}
                      >
                        {children}
                      </code>
                    );
                  }
                }}
              >
                {content.body.replace(/\\n/g, '\n')}
              </ReactMarkdown>
            </div>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default AboutPage;
