import React, { useEffect, useState } from 'react';
import type { ShowcaseItem, Application } from '../types';
import ShowcaseCarousel from './ShowcaseCarousel';
import { getApplications } from '../services/contentService';
import { Spinner, Alert } from 'react-bootstrap';

const AppsCarousel: React.FC = () => {
  const [apps, setApps] = useState<ShowcaseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getApplications()
      .then((data: Application[]) => {
        const mapped: ShowcaseItem[] = data.map((p) => ({
          id: p.id || p.demo_url || 'unknown',
          title: p.title,
          description: p.description || '',
          imageUrl: p.image_url,
          tags: p.tags,
          linkUrl: p.demo_url,
          repoUrl: p.repo_url,
          type: 'app'
        }));
        setApps(mapped);
      })
      .catch(() => setError('Failed to load applications.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center my-5"><Spinner animation="border" variant="primary" role="status" /></div>;
  if (error) return <Alert variant="danger">{error}</Alert>;
  if (apps.length === 0) return null;

  return <ShowcaseCarousel items={apps} title="Applications & Sites" />;
};

export default AppsCarousel;
