import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import HomePage from './pages/HomePage';

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          {/* Support navigation to sections if needed, or other routes */}
          <Route path="/blogs" element={<HomePage />} />
          <Route path="/projects" element={<HomePage />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  )
}

export default App
