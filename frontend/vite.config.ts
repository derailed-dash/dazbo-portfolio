import { defineConfig } from 'vitest/config'
import type { Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import { injectSeoTags } from './src/utils/seoInjector'

function seoInjectorPlugin(): Plugin {
  return {
    name: 'html-seo-injector',
    apply: 'serve',
    transformIndexHtml: async (html, ctx) => {
      // For local dev, path is usually raw URL path
      // e.g. / or /about
      // Note: Vite's ctx.path might include trailing slash or be undefined if root
      const path = ctx.originalUrl || ctx.path || '/';
      return await injectSeoTags(html, path);
    }
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), seoInjectorPlugin()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/sitemap.xml': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
