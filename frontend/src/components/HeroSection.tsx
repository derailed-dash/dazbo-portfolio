import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const HeroSection: React.FC = () => {
    return (
        <div className="hero-wrapper position-relative text-white mb-5" style={{ zIndex: 1 }}>
            {/* Banner Background - No Overlay, clean image */}
            <div
                className="position-absolute top-0 start-0 w-100 h-100"
                style={{
                    backgroundImage: 'url("/images/dazbo-banner.png")',
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    zIndex: -1
                }}
            ></div>

            {/* Content Container */}
            <Container className="position-relative py-5">
                <Row className="align-items-center">
                    
                    {/* Left Column: Profile Picture */}
                    <Col xs={12} md={4} lg={3} className="text-center text-md-start mb-4 mb-md-0">
                        <img
                            src="/images/dazbo-profile.png"
                            alt="Dazbo"
                            className="shadow-lg"
                            style={{
                                width: '180px',
                                height: '180px',
                                objectFit: 'cover',
                                border: '4px solid #ffffff', /* White border for contrast */
                                borderRadius: '12px',
                                boxShadow: '0 4px 15px rgba(0,0,0,0.5)' 
                            }}
                        />
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
