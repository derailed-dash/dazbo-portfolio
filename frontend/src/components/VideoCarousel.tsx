import React, { useEffect, useState } from 'react';
import type { ShowcaseItem, Video } from '../types';
import ShowcaseCarousel from './ShowcaseCarousel';
import { getVideos } from '../services/videoService';
import { Spinner, Alert } from 'react-bootstrap';

/**
 * Component that fetches and displays a carousel of YouTube videos.
 */
const VideoCarousel: React.FC = () => {
  const [videos, setVideos] = useState<ShowcaseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getVideos()
      .then((data: Video[]) => {
        // Map backend video data to ShowcaseCarousel item format
        const mapped: ShowcaseItem[] = data.map((v) => ({
          id: v.id || v.video_url,
          title: v.title,
          description: v.description,
          imageUrl: v.thumbnail_url,
          tags: [v.source_platform],
          linkUrl: v.video_url,
          type: 'video'
        }));
        setVideos(mapped);
      })
      .catch((err) => {
        console.error('Error loading videos:', err);
        setError('Failed to load videos.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center my-5"><Spinner animation="border" variant="primary" role="status" /></div>;
  if (error) return <Alert variant="danger" className="mx-auto max-w-4xl my-4">{error}</Alert>;
  if (videos.length === 0) return null;

  return <ShowcaseCarousel items={videos} title="Videos & Presentations" />;
};

export default VideoCarousel;
