import React, { useEffect, useState } from 'react';
import type { ShowcaseItem, Project } from '../types';
import ShowcaseCarousel from './ShowcaseCarousel';
import { getProjects } from '../services/contentService';
import { Spinner, Alert } from 'react-bootstrap';

const ProjectCarousel: React.FC = () => {
  const [projects, setProjects] = useState<ShowcaseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProjects()
      .then((data: Project[]) => {
        const mapped: ShowcaseItem[] = data.map((p) => ({
          id: p.id || p.repo_url || 'unknown',
          title: p.title,
          description: p.description || '',
          imageUrl: p.image_url,
          tags: p.tags,
          linkUrl: p.demo_url,
          repoUrl: p.repo_url,
          type: 'project'
        }));
        setProjects(mapped);
      })
      .catch(() => setError('Failed to load projects.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center my-5"><Spinner animation="border" variant="primary" role="status" /></div>;
  if (error) return <Alert variant="danger">{error}</Alert>;
  if (projects.length === 0) return null;

  return <ShowcaseCarousel items={projects} title="Featured Projects" />;
};

export default ProjectCarousel;
