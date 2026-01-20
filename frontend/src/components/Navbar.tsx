import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
/* Removed Lucide User icon as we are moving to text-based branding */

const AppNavbar: React.FC = () => {
  return (
    <Navbar className="shadow-sm py-3 mb-0 sticky-top" style={{ backgroundColor: '#000000', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
      <Container>
        <Navbar.Brand as={NavLink} to="/" className="d-flex align-items-center gap-2" style={{ fontSize: '1.5rem' }}>
          {/* Styled Text moved from Hero Section */}
          <span className="fw-bold" style={{ color: '#ffffff' }}>
            <span style={{ color: '#BB86FC' }}>Dazbo's</span> Portfolio
          </span>
        </Navbar.Brand>
        
        {/* Tagline moved from Hero - Visible on Large screens only to prevent clutter */}
        <div className="d-none d-lg-block text-end" style={{ color: 'rgba(255,255,255,0.7)', fontSize: '0.9rem', maxWidth: '750px' }}>
            A showcase of technical writing, open-source craftsmanship, and professional experience.
            <br />
            Powered by Python, React, and Gemini AI.
        </div>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
