import { BrowserRouter } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import { Button } from 'react-bootstrap';

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <div className="text-center py-5">
          <h1 className="display-4 fw-bold mb-4">Welcome to Dazbo Portfolio</h1>
          <p className="lead mb-4">
            A showcase of technical writing, open-source projects, and professional experience.
          </p>
          <Button variant="primary" size="lg">
            Explore My Work
          </Button>
        </div>
      </MainLayout>
    </BrowserRouter>
  )
}

export default App
