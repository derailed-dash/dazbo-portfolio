import React, { useEffect, useState } from 'react';
import type { ShowcaseItem, Blog, BlogSource } from '../types';
import ShowcaseCarousel from './ShowcaseCarousel';
import { getBlogs } from '../services/contentService';
import { Spinner, Alert } from 'react-bootstrap';
import { mergeDuplicateArticles } from '../utils/blogUtils';

const BlogCarousel: React.FC = () => {
  const [blogs, setBlogs] = useState<ShowcaseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getBlogs()
      .then((data: Blog[]) => {
        // Deduplicate cross-platform articles
        const deduplicated = mergeDuplicateArticles(data);

        // Map backend data to ShowcaseCarousel item format
        const mapped: ShowcaseItem[] = deduplicated.map((b) => {
          // Map platforms to BlogSource format
          const sources: BlogSource[] = (b.platforms || []).map((p) => {
            let iconPath = '';
            const lowerPlatform = p.name.toLowerCase();
            if (lowerPlatform.includes('medium')) {
              iconPath = '/images/medium-icon.png';
            } else if (lowerPlatform.includes('dev.to')) {
              iconPath = '/images/dev-black.png';
            }
            return {
              platform: p.name,
              url: p.url,
              iconPath
            };
          });

          return {
            id: b.id || b.url || 'unknown',
            title: b.title,
            description: b.ai_summary || b.summary || '',
            imageUrl: b.image_url,
            tags: b.tags || [b.platform],
            linkUrl: b.url,
            isPrivate: b.is_private,
            sources,
            type: 'blog'
          };
        });
        setBlogs(mapped);
      })
      .catch(() => setError('Failed to load blogs.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center my-5"><Spinner animation="border" variant="primary" role="status" /></div>;
  if (error) return <Alert variant="danger">{error}</Alert>;
  if (blogs.length === 0) return null;

  return <ShowcaseCarousel items={blogs} title="Latest Blog Posts" />;
};

export default BlogCarousel;
