import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export const useSeo = () => {
  const location = useLocation();

  useEffect(() => {
    const fetchSeoData = async () => {
      try {
        const response = await fetch(`/api/seo?path=${location.pathname}`);
        if (response.ok) {
          const data = await response.json();
          if (data.title) {
            document.title = data.title;
          }
        }
      } catch (error) {
        console.error('Failed to fetch SEO data:', error);
      }
    };

    fetchSeoData();
  }, [location.pathname]);
};
