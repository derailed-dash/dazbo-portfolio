import React from 'react';

import HeroSection from '../components/HeroSection';
import BlogCarousel from '../components/BlogCarousel';
import ProjectCarousel from '../components/ProjectCarousel';
import AppsCarousel from '../components/AppsCarousel';

const HomePage: React.FC = () => {
  return (
    <>
      <HeroSection />

      <BlogCarousel />
      <ProjectCarousel />
      <AppsCarousel />
    </>
  );
};

export default HomePage;
