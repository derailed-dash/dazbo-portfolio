import React, { useEffect, useState } from 'react';
import ShowcaseCarousel from './ShowcaseCarousel';
import { getProjects } from '../services/contentService';
import { Spinner, Alert } from 'react-bootstrap';

const AppsCarousel: React.FC = () => {
  const [apps, setApps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProjects()
      .then(data => {
        // For AppsCarousel, we filter for 'featured' projects that have a demo_url
        const filtered = data.filter((p: any) => p.featured && p.demo_url);
        const mapped = filtered.map((p: any) => ({
          id: p.id || p.demo_url,
          title: p.title,
          description: p.description || '',
          imageUrl: p.image_url,
          tags: p.tags,
          linkUrl: p.demo_url,
          type: 'app'
        }));
        setApps(mapped);
      })
      .catch(err => setError('Failed to load applications.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center my-5"><Spinner animation="border" variant="primary" role="status" /></div>;
  if (error) return <Alert variant="danger">{error}</Alert>;
  if (apps.length === 0) return null;

  return <ShowcaseCarousel items={apps} title="Live Applications" />;
};

export default AppsCarousel;
