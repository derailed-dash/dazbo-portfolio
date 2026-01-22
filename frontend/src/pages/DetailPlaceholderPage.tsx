import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { Button } from 'react-bootstrap';
import { ArrowLeft } from 'lucide-react';
import SEO from '../components/SEO';

const DetailPlaceholderPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  return (
    <div className="py-5">
      <SEO 
        title={`Content Detail: ${id}`}
        description={`Details for content item: ${id}`}
        type="article"
      />
      <Link to="/">
        <Button variant="outline-secondary" className="mb-4 d-flex align-items-center gap-2">
          <ArrowLeft size={18} />
          Back to Home
        </Button>
      </Link>
      <h1 className="display-5 fw-bold mb-4">Content Detail: {id}</h1>
      <div className="bg-white p-5 rounded shadow-sm border">
        <p className="lead">
          This is a placeholder page for the detailed view of item: <strong>{id}</strong>.
        </p>
        <p>
          Full content for this item will be implemented in a future phase. 
          The routing and structure are now in place to support deep-linking.
        </p>
      </div>
    </div>
  );
};

export default DetailPlaceholderPage;
