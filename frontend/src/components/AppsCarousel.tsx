import React, { useEffect, useState } from 'react';
import type { ShowcaseItem, Project } from '../types';
import ShowcaseCarousel from './ShowcaseCarousel';
import { getProjects } from '../services/contentService';
import { Spinner, Alert } from 'react-bootstrap';

const AppsCarousel: React.FC = () => {
  const [apps, setApps] = useState<ShowcaseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getProjects()
      .then((data: Project[]) => {
        // For AppsCarousel, we filter for 'featured' projects that have a demo_url
        let filtered = data.filter((p) => p.featured && p.demo_url);
        
        // MOCK DATA FALLBACK (TEMPORARY: To verify UI when no Firestore data exists)
        if (filtered.length === 0) {
          filtered = [
            {
              // @ts-ignore - Mock data doesn't strictly adhere to Project interface yet
              id: 'mock-1',
              title: 'Advent of Code Walkthroughs',
              description: 'My solutions and Python learning resources for Advent of Code. (Mock Data)',
              image_url: 'https://placehold.co/600x400?text=AoC+Site',
              tags: ['python', 'algorithms', 'education'],
              demo_url: 'https://aoc.just2good.co.uk/',
              featured: true,
              is_manual: true,
              metadata_only: false
            },
            {
               // @ts-ignore
              id: 'mock-2',
              title: 'Portfolio Agent',
              description: 'This very portfolio, powered by Gemini and React. (Mock Data)',
              image_url: 'https://placehold.co/600x400?text=Portfolio',
              tags: ['react', 'fastapi', 'gemini'],
              demo_url: 'https://dazbo.dev',
              featured: true,
              is_manual: true,
              metadata_only: false
            }
          ];
        }

        const mapped: ShowcaseItem[] = filtered.map((p) => ({
          id: p.id || p.demo_url || 'unknown',
          title: p.title,
          description: p.description || '',
          imageUrl: p.image_url,
          tags: p.tags,
          linkUrl: p.demo_url,
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

  return <ShowcaseCarousel items={apps} title="Live Applications" />;
};

export default AppsCarousel;
