import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/projects': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/blogs': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/experience': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/feedback': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
