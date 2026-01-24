import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { User } from 'lucide-react';

const HeroSection: React.FC = () => {
    const [isMobile, setIsMobile] = React.useState(window.innerWidth < 768);

    React.useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth < 768);
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <div className="hero-wrapper position-relative text-white mb-5">
            {/* Banner Background - No Overlay, clean image */}
            <div className="position-absolute top-0 start-0 w-100 h-100 hero-banner"></div>

            {/* Content Container */}
            <Container className="position-relative py-5">
                <Row className="align-items-center">
                    
                    {/* Left Column: Profile Picture & About Link */}
                    <Col xs={12} md={4} lg={3} className="text-start mb-4 mb-md-0">
                        <div className="d-inline-flex flex-column align-items-center">
                            <img
                                src="/images/dazbo-profile.png"
                                alt="Dazbo"
                                className="shadow-lg hero-profile-img"
                            />
                            <div className="mt-3">
                                <Link 
                                    to="/about" 
                                    className="btn btn-glass rounded-pill px-4 fw-bold"
                                >
                                    <User size={isMobile ? 14 : 18} className="me-2" />
                                    About Me
                                </Link>
                            </div>
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
