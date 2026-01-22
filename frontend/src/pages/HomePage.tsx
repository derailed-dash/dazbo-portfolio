import React from 'react';

import HeroSection from '../components/HeroSection';
import BlogCarousel from '../components/BlogCarousel';
import ProjectCarousel from '../components/ProjectCarousel';
import AppsCarousel from '../components/AppsCarousel';
import SEO from '../components/SEO';

const HomePage: React.FC = () => {
  return (
    <>
      <SEO 
        title="Home"
        description='Explore the professional portfolio of Darren "Dazbo" Lester, an Enterprise Cloud Architect and Google Cloud expert, specialising in agentic AI, open-source craftsmanship, and technical writing.'
        jsonLd={{
          "@context": "https://schema.org",
          "@type": "Person",
          "name": "Darren Lester",
          "alternateName": "Dazbo",
          "jobTitle": "Enterprise Cloud Architect",
          "url": "https://darrenlester.net",
          "sameAs": [
            "https://github.com/derailed-dash",
            "https://www.linkedin.com/in/darren-lester-architect/",
            "https://medium.com/@derailed.dash",
            "https://dev.to/deraileddash"
          ]
        }}
      />
      <HeroSection />

      <BlogCarousel />
      <ProjectCarousel />
      <AppsCarousel />
    </>
  );
};

export default HomePage;
