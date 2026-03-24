import React from 'react';

import { useSeo } from '../hooks/useSeo';
import HeroSection from '../components/HeroSection';
import BlogCarousel from '../components/BlogCarousel';
import ProjectCarousel from '../components/ProjectCarousel';
import VideoCarousel from '../components/VideoCarousel';
import AppsCarousel from '../components/AppsCarousel';

const HomePage: React.FC = () => {
  useSeo();
  return (
    <>
      <HeroSection />

      <BlogCarousel />
      <ProjectCarousel />
      <VideoCarousel />
      <AppsCarousel />
    </>
  );
};

export default HomePage;
