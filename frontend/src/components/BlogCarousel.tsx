import React, { useEffect, useState } from 'react';
import ShowcaseCarousel from './ShowcaseCarousel';
import { getBlogs } from '../services/contentService';
import { Spinner, Alert } from 'react-bootstrap';

const BlogCarousel: React.FC = () => {
  const [blogs, setBlogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getBlogs()
      .then(data => {
        // Map backend data to ShowcaseCarousel item format
        const mapped = data.map((b: any) => ({
          id: b.id || b.url,
          title: b.title,
          description: b.summary || b.description || '',
          imageUrl: b.image_url,
          tags: b.tags || [b.platform],
          linkUrl: b.url,
          type: 'blog'
        }));
        setBlogs(mapped);
      })
      .catch(err => setError('Failed to load blogs.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center my-5"><Spinner animation="border" variant="primary" role="status" /></div>;
  if (error) return <Alert variant="danger">{error}</Alert>;
  if (blogs.length === 0) return null;

  return <ShowcaseCarousel items={blogs} title="Latest Blog Posts" />;
};

export default BlogCarousel;
