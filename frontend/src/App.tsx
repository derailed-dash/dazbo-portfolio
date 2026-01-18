import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import HomePage from './pages/HomePage';
import DetailPlaceholderPage from './pages/DetailPlaceholderPage';

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/details/:id" element={<DetailPlaceholderPage />} />
          {/* Support navigation to sections if needed, or other routes */}
          <Route path="/blogs" element={<HomePage />} />
          <Route path="/projects" element={<HomePage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  )
}

export default App
