import React from 'react';
import { Card, Button, Badge } from 'react-bootstrap';
import { ExternalLink, Github, Lock } from 'lucide-react';

interface ShowcaseCardProps {
  title: string;
  description: string;
  imageUrl?: string;
  tags?: string[];
  linkUrl?: string;
  repoUrl?: string;
  isPrivate?: boolean;
  sourceIcon?: string;
  sourceUrl?: string;
  type: 'blog' | 'project' | 'app';
}

const ShowcaseCard: React.FC<ShowcaseCardProps> = ({
  title,
  description,
  imageUrl,
  tags = [],
  linkUrl,
  repoUrl,
  isPrivate,
  sourceIcon,
  sourceUrl,
  type
}) => {
  return (
    <Card className="h-100 overflow-hidden">
      {imageUrl && (
        <div style={{ height: '180px', overflow: 'hidden' }}>
          <Card.Img 
            variant="top" 
            src={imageUrl} 
            className="w-100 h-100 object-fit-cover"
            alt={title}
          />
        </div>
      )}
      <Card.Body className="d-flex flex-column">
        <div className="d-flex justify-content-between align-items-start mb-2">
          <div className="tags-container">
            {tags.slice(0, 3).map(tag => (
              <Badge key={tag} bg="light" text="dark" className="me-1 border text-uppercase" style={{ fontSize: '0.7rem' }}>
                {tag}
              </Badge>
            ))}
          </div>
          {isPrivate && (
            <Badge bg="warning" text="dark" className="d-flex align-items-center gap-1" style={{ fontSize: '0.7rem' }}>
              <Lock size={10} />
              <span>Member-only</span>
            </Badge>
          )}
        </div>
        <Card.Title className="h5 mb-2 fw-bold">{title}</Card.Title>
        <Card.Text className="text-muted small flex-grow-1">
          {description.length > 120 ? `${description.substring(0, 120)}...` : description}
        </Card.Text>

        
        {/* Footer Row: Buttons (Left) & Source Icon (Right) */}
        <div className="d-flex justify-content-between align-items-center mt-3">
          <div className="d-flex gap-2">
            {linkUrl && (
              <Button 
                variant="primary" 
                size="sm" 
                href={linkUrl} 
                target="_blank"
                className="d-flex align-items-center gap-1"
              >
                <ExternalLink size={14} />
                <span>{type === 'blog' ? 'Read' : 'View'}</span>
              </Button>
            )}
            {repoUrl && (
              <Button 
                variant="outline-secondary" 
                size="sm" 
                href={repoUrl} 
                target="_blank"
                className="d-flex align-items-center gap-1"
              >
                <Github size={14} />
                <span>Code</span>
              </Button>
            )}
          </div>

          {sourceIcon && (
            <div className="d-flex align-items-center">
              {sourceUrl ? (
                <a 
                  href={sourceUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="d-inline-flex opacity-75 hover-opacity-100 transition-opacity"
                  title="View Profile"
                >
                  <img 
                    src={sourceIcon} 
                    alt="Source" 
                    style={{ width: '24px', height: '24px', objectFit: 'contain' }} 
                  />
                </a>
              ) : (
                <img 
                  src={sourceIcon} 
                  alt="Source" 
                  style={{ width: '24px', height: '24px', objectFit: 'contain' }} 
                  title="Content Source"
                />
              )}
            </div>
          )}
        </div>
      </Card.Body>
    </Card>
  );
};

export default ShowcaseCard;
