import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
/* Removed Lucide User icon as we are moving to text-based branding */

const AppNavbar: React.FC = () => {
  return (
    <Navbar className="shadow-sm py-3 mb-0 sticky-top">
      <Container>
        <Navbar.Brand as={NavLink} to="/" className="d-flex align-items-center gap-2">
          {/* Styled Text moved from Hero Section */}
          <span className="fw-bold navbar-brand-text">
            <span className="navbar-brand-accent">Dazbo's</span> Portfolio
          </span>
        </Navbar.Brand>
        
        {/* Tagline moved from Hero - Visible on Large screens only to prevent clutter */}
        <div className="d-none d-lg-block text-end navbar-tagline">
            A showcase of technical writing, open-source craftsmanship, and professional experience.
            <br />
            Powered by Python, React, and Gemini AI.
        </div>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
