import { BrowserRouter } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import { Button } from 'react-bootstrap';
import BlogCarousel from './components/BlogCarousel';
import ProjectCarousel from './components/ProjectCarousel';
import AppsCarousel from './components/AppsCarousel';

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <div className="text-center py-5 hero-section">
          <h1 className="display-4 fw-bold mb-4">Welcome to Dazbo Portfolio</h1>
          <p className="lead mb-4">
            A showcase of technical writing, open-source projects, and professional experience.
          </p>
          <div>
            <Button variant="primary" size="lg" className="mb-5">
              Explore My Work
            </Button>
          </div>
        </div>

        <AppsCarousel />
        <BlogCarousel />
        <ProjectCarousel />
      </MainLayout>
    </BrowserRouter>
  )
}

export default App
