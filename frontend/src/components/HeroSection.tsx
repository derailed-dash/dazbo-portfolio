import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const HeroSection: React.FC = () => {
    return (
        <div className="hero-wrapper position-relative text-white mb-5">
            {/* Banner Background - No Overlay, clean image */}
            <div className="position-absolute top-0 start-0 w-100 h-100 hero-banner"></div>

            {/* Content Container */}
            <Container className="position-relative py-5">
                <Row className="align-items-center">
                    
                    {/* Left Column: Profile Picture */}
                    <Col xs={12} md={4} lg={3} className="text-start mb-4 mb-md-0">
                        <img
                            src="/images/dazbo-profile.png"
                            alt="Dazbo"
                            className="shadow-lg hero-profile-img"
                        />
                        <div className="mt-3 text-center text-md-start">
                            <Link to="/about" className="text-white text-decoration-none fw-bold border-bottom border-2 border-white pb-1">
                                More about me &rarr;
                            </Link>
                        </div>
                    </Col>

                    {/* Right Column: Empty now, but keeping structure for spacing or future use */}
                    <Col xs={12} md={8} lg={9}>
                       {/* Content moved to Navbar */}
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default HeroSection;
