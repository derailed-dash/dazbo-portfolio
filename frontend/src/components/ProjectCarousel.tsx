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
        // Filter for GitHub projects
        const githubProjects = data.filter((p) => p.source_platform === 'github');

        const mapped: ShowcaseItem[] = githubProjects.map((p) => ({
          id: p.id || p.repo_url || 'unknown',
          title: p.title,
          description: p.description || '',
          imageUrl: p.image_url,
          tags: p.tags,
          linkUrl: p.demo_url,
          repoUrl: p.repo_url,
          stargazers_count: p.stargazers_count,
          updated_at: p.updated_at,
          type: 'project'
        }));
        const FORTY_FIVE_DAYS_MS = 45 * 24 * 60 * 60 * 1000;
        const now = Date.now();

        // Sort: if updated <= 45 days ago AND has > 0 stars -> prioritise by updated_at.
        // Else -> sort by stargazers_count descending, then updated_at descending.
        mapped.sort((a, b) => {
          const dateA = a.updated_at ? new Date(a.updated_at).getTime() : 0;
          const dateB = b.updated_at ? new Date(b.updated_at).getTime() : 0;
          
          const aRecent = (now - dateA) <= FORTY_FIVE_DAYS_MS && (a.stargazers_count || 0) > 0;
          const bRecent = (now - dateB) <= FORTY_FIVE_DAYS_MS && (b.stargazers_count || 0) > 0;

          if (aRecent && !bRecent) return -1;
          if (!aRecent && bRecent) return 1;

          if (aRecent && bRecent) {
            return dateB - dateA;
          }

          const starsA = a.stargazers_count || 0;
          const starsB = b.stargazers_count || 0;
          if (starsA !== starsB) {
            return starsB - starsA;
          }
          return dateB - dateA;
        });

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
