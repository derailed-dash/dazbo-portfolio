import React from 'react';
import { Carousel, Row, Col } from 'react-bootstrap';
import ShowcaseCard from './ShowcaseCard';

import type { ShowcaseItem } from '../types';

/* Item interface replaced by import */

interface ShowcaseCarouselProps {
  items: ShowcaseItem[];
  title?: string;
}

const ShowcaseCarousel: React.FC<ShowcaseCarouselProps> = ({ items, title }) => {
  if (!items || items.length === 0) return null;

  // Function to chunk items for multi-item display on larger screens
  const chunkItems = (arr: ShowcaseItem[], size: number) => {
    const chunks = [];
    for (let i = 0; i < arr.length; i += size) {
      chunks.push(arr.slice(i, i + size));
    }
    return chunks;
  };

  const desktopChunks = chunkItems(items, 3);

  return (
    <div className="mb-5">
      {title && <h2 className="h3 mb-4 fw-bold border-start border-primary border-4 ps-3">{title}</h2>}
      
      {/* Desktop/Tablet View: 3 items per slide */}
      <Carousel interval={null} indicators={items.length > 3} className="pb-5 d-none d-md-block">
        {desktopChunks.map((chunk, idx) => (
          <Carousel.Item key={idx}>
            <Row className="px-5">
              {chunk.map(item => (
                <Col md={4} key={item.id} className="mb-3">
                  <ShowcaseCard {...item} />
                </Col>
              ))}
            </Row>
          </Carousel.Item>
        ))}
      </Carousel>

      {/* Mobile View: 1 item per slide */}
      <Carousel interval={null} indicators={items.length > 1} className="pb-5 d-md-none">
        {items.map((item) => (
          <Carousel.Item key={item.id}>
            <Row className="justify-content-center px-1">
              <Col xs={11}>
                <ShowcaseCard {...item} />
              </Col>
            </Row>
          </Carousel.Item>
        ))}
      </Carousel>
    </div>
  );
};

export default ShowcaseCarousel;
