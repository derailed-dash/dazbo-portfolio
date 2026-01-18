import React from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import { User } from 'lucide-react';

const AppNavbar: React.FC = () => {
  return (
    <Navbar bg="white" expand="lg" className="shadow-sm py-3 mb-4 sticky-top">
      <Container>
        <Navbar.Brand as={NavLink} to="/" className="d-flex align-items-center gap-2 fw-bold text-primary">
          <User size={24} />
          <span>Dazbo Portfolio</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto gap-3">
            <Nav.Link as={NavLink} to="/" end>Home</Nav.Link>
            <Nav.Link as={NavLink} to="/blogs">Blogs</Nav.Link>
            <Nav.Link as={NavLink} to="/projects">Projects</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
