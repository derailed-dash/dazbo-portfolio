import React from 'react';
import { Carousel, Row, Col } from 'react-bootstrap';
import ShowcaseCard from './ShowcaseCard';

interface Item {
  id: string;
  title: string;
  description: string;
  imageUrl?: string;
  tags?: string[];
  linkUrl?: string;
  repoUrl?: string;
  type: 'blog' | 'project' | 'app';
}

interface ShowcaseCarouselProps {
  items: Item[];
  title?: string;
}

const ShowcaseCarousel: React.FC<ShowcaseCarouselProps> = ({ items, title }) => {
  if (!items || items.length === 0) return null;

  // For this initial implementation, we'll show 1 item per slide on mobile
  // and try to accommodate more on desktop if we refactor later.
  // For now, keeping it simple: 1 item per slide to ensure stability.
  return (
    <div className="mb-5">
      {title && <h2 className="h3 mb-4 fw-bold border-start border-primary border-4 ps-3">{title}</h2>}
      <Carousel interval={null} indicators={items.length > 1} className="pb-4">
        {items.map((item) => (
          <Carousel.Item key={item.id}>
            <Row className="justify-content-center px-1">
              <Col xs={12} md={8} lg={6}>
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
