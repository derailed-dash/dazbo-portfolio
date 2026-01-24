import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Spinner, Alert } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';
import { getContentBySlug } from '../services/contentService';
import { Content } from '../types';
import SEO from '../components/SEO';

const AboutPage: React.FC = () => {
  const [content, setContent] = useState<Content | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

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
      <SEO 
        title={content.title}
        description={`About Darren "Dazbo" Lester - ${content.title}`}
      />
      
      {/* Header Section (Reusing Hero styling principles) */}
      <div className="hero-wrapper position-relative text-white mb-5">
        <div className="position-absolute top-0 start-0 w-100 h-100 hero-banner"></div>
        <Container className="position-relative py-5">
          <Row>
            <Col>
              <h1 className="display-4 fw-bold">{content.title}</h1>
              <p className="lead">Professional Profile & Expertise</p>
            </Col>
          </Row>
        </Container>
      </div>

      <Container className="mb-5 pb-5">
        <Row>
          <Col lg={9} className="mx-auto">
            <div className="markdown-content bg-white p-4 p-md-5 shadow-sm rounded">
              <ReactMarkdown>{content.body}</ReactMarkdown>
            </div>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default AboutPage;
