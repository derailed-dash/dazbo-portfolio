import React from 'react';
import { Container } from 'react-bootstrap';
import AppNavbar from './Navbar';
import Footer from './Footer';
import ChatWidget from './ChatWidget';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <AppNavbar />
      <main className="flex-grow-1">
        <Container className="py-4 app-container">
          {children}
        </Container>
      </main>
      <ChatWidget />
      <Footer />
    </div>
  );
};

export default MainLayout;
