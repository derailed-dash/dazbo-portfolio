import React from 'react';
import { Card, Button, Badge } from 'react-bootstrap';
import { ExternalLink, Github } from 'lucide-react';

interface ShowcaseCardProps {
  title: string;
  description: string;
  imageUrl?: string;
  tags?: string[];
  linkUrl?: string;
  repoUrl?: string;
  type: 'blog' | 'project' | 'app';
}

const ShowcaseCard: React.FC<ShowcaseCardProps> = ({
  title,
  description,
  imageUrl,
  tags = [],
  linkUrl,
  repoUrl,
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
        <div className="mb-2">
          {tags.slice(0, 3).map(tag => (
            <Badge key={tag} bg="light" text="dark" className="me-1 border text-uppercase" style={{ fontSize: '0.7rem' }}>
              {tag}
            </Badge>
          ))}
        </div>
        <Card.Title className="h5 mb-2 fw-bold">{title}</Card.Title>
        <Card.Text className="text-muted small flex-grow-1">
          {description.length > 120 ? `${description.substring(0, 120)}...` : description}
        </Card.Text>
        <div className="d-flex gap-2 mt-3">
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
      </Card.Body>
    </Card>
  );
};

export default ShowcaseCard;
