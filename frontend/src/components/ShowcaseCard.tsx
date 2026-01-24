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
  const getSafeUrl = (url: string | undefined): string | undefined => {
    if (!url) return undefined;
    if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('/')) {
      return url;
    }
    return undefined;
  };

  const safeLinkUrl = getSafeUrl(linkUrl);
  const safeRepoUrl = getSafeUrl(repoUrl);
  const safeSourceUrl = getSafeUrl(sourceUrl);

  const sourceIconStyle: React.CSSProperties = { 
    width: '24px', 
    height: '24px', 
    objectFit: 'contain' 
  };

  return (
    <Card className="h-100 overflow-hidden glass-card">
      {imageUrl && (
        <div style={{ height: '180px', overflow: 'hidden', background: 'rgba(0,0,0,0.2)' }} className="d-flex align-items-center justify-content-center">
          <Card.Img 
            variant="top" 
            src={imageUrl} 
            style={{ height: '90%', width: '90%', objectFit: 'contain' }}
            alt={title}
          />
        </div>
      )}
      <Card.Body className="d-flex flex-column">
        <div className="d-flex justify-content-between align-items-start mb-2">
          <div className="tags-container">
            {tags.slice(0, 3).map(tag => (
              <Badge key={tag} bg="transparent" className="me-1 border text-uppercase" style={{ fontSize: '0.6rem', color: 'rgba(255,255,255,0.8)', borderColor: 'rgba(255,255,255,0.3)' }}>
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
        <Card.Text className="small flex-grow-1">
          {description.length > 120 ? `${description.substring(0, 120)}...` : description}
        </Card.Text>

        
        {/* Footer Row: Buttons (Left) & Source Icon (Right) */}
        <div className="d-flex justify-content-between align-items-center mt-3">
          <div className="d-flex gap-2">
            {safeLinkUrl && (
              <Button 
                variant="primary" 
                size="sm" 
                href={safeLinkUrl} 
                target="_blank"
                className="d-flex align-items-center gap-1"
              >
                <ExternalLink size={14} />
                <span>{type === 'blog' ? 'Read' : 'View'}</span>
              </Button>
            )}
            {safeRepoUrl && (
              <Button 
                variant="outline-secondary" 
                size="sm" 
                href={safeRepoUrl} 
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
              {safeSourceUrl ? (
                <a 
                  href={safeSourceUrl} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="d-inline-flex opacity-100 hover-opacity-100 transition-opacity bg-white rounded-circle p-1 shadow-sm"
                  title="View Profile"
                >
                  <img 
                    src={sourceIcon} 
                    alt="Source" 
                    style={sourceIconStyle} 
                  />
                </a>
              ) : (
                <div className="bg-white rounded-circle p-1 shadow-sm d-inline-flex">
                  <img 
                    src={sourceIcon} 
                    alt="Source" 
                    style={sourceIconStyle} 
                    title="Content Source"
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </Card.Body>
    </Card>
  );
};

export default ShowcaseCard;
