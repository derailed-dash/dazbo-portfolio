import React, { useState } from 'react';
import { Carousel, Row, Col } from 'react-bootstrap';
import ShowcaseCard from './ShowcaseCard';

import type { ShowcaseItem } from '../types';

interface ShowcaseCarouselProps {
  items: ShowcaseItem[];
  title?: string;
}

const ShowcaseCarousel: React.FC<ShowcaseCarouselProps> = ({ items, title }) => {
  const [activeIndex, setActiveIndex] = useState(0);

  if (!items || items.length === 0) return null;

  const handleSelect = (selectedIndex: number) => {
    setActiveIndex(selectedIndex);
  };

  // Function to chunk items for multi-item display on larger screens
  const chunkItems = (arr: ShowcaseItem[], size: number) => {
    const chunks = [];
    for (let i = 0; i < arr.length; i += size) {
      chunks.push(arr.slice(i, i + size));
    }
    return chunks;
  };

  const desktopChunks = chunkItems(items, 4);

  // Pagination Logic for Mobile
  const MAX_VISIBLE_DOTS = 5;
  let startDot = 0;
  if (items.length > MAX_VISIBLE_DOTS) {
    // Center the active dot in the window if possible
    startDot = Math.max(0, Math.min(activeIndex - 2, items.length - MAX_VISIBLE_DOTS));
  }
  // Determine the range of dots to show. 
  // If items.length <= MAX_VISIBLE_DOTS, we show all (0 to items.length).
  // Otherwise we show from startDot to startDot + MAX_VISIBLE_DOTS.
  const endDot = Math.min(items.length, items.length <= MAX_VISIBLE_DOTS ? items.length : startDot + MAX_VISIBLE_DOTS);
  
  // Create an array of indices to render
  const visibleDotIndices = [];
  for (let i = startDot; i < endDot; i++) {
    visibleDotIndices.push(i);
  }

  return (
    <div className="mb-5">
      {title && <h2 className="h3 mb-4 fw-bold text-center">{title}</h2>}
      
      {/* Desktop/Tablet View: 4 items per slide */}
      <Carousel interval={null} indicators={items.length > 4} className="pb-5 d-none d-md-block">
        {desktopChunks.map((chunk, idx) => (
          <Carousel.Item key={idx}>
            <Row className="g-3" style={{ paddingLeft: '6%', paddingRight: '6%', paddingTop: '10px' }}>
              {chunk.map(item => (
                <Col md={3} key={item.id} className="mb-3">
                  <ShowcaseCard {...item} />
                </Col>
              ))}
            </Row>
          </Carousel.Item>
        ))}
      </Carousel>

      {/* Mobile View: 1 item per slide */}
      <Carousel 
        activeIndex={activeIndex}
        onSelect={handleSelect}
        interval={null} 
        indicators={false} // Disable default indicators
        className="d-md-none"
      >
        {items.map((item) => (
          <Carousel.Item key={item.id}>
            <Row className="justify-content-center px-1" style={{ paddingTop: '10px' }}>
              <Col xs={11}>
                <ShowcaseCard {...item} />
              </Col>
            </Row>
          </Carousel.Item>
        ))}
      </Carousel>

      {/* Custom Mobile Indicators */}
      <div className="d-flex justify-content-center mt-3 d-md-none mobile-custom-indicators">
          {items.length <= 1 ? null : (
              visibleDotIndices.map((absoluteIndex) => {
                  const isActive = absoluteIndex === activeIndex;
                  return (
                      <div 
                          key={absoluteIndex}
                          className={`indicator-dot ${isActive ? 'active' : ''}`}
                          style={{
                              width: '8px',
                              height: '8px',
                              borderRadius: '50%',
                              backgroundColor: isActive ? 'var(--bs-primary)' : 'var(--bs-gray-400)',
                              margin: '0 4px',
                              cursor: 'pointer',
                              transition: 'all 0.3s ease'
                          }}
                          onClick={() => setActiveIndex(absoluteIndex)}
                          role="button"
                          aria-label={`Go to slide ${absoluteIndex + 1}`}
                      />
                  );
              })
          )}
      </div>
    </div>
  );
};

export default ShowcaseCarousel;