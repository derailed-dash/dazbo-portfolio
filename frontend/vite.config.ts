import { defineConfig } from 'vitest/config'
import type { Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import { injectSeoTags } from './src/utils/seoInjector'

function seoInjectorPlugin(): Plugin {
  return {
    name: 'html-seo-injector',
    apply: 'serve',
    transformIndexHtml: async (html, ctx) => {
      // Extract just the path part to ignore query parameters (e.g. /about?foo=bar -> /about)
      const rawUrl = ctx.originalUrl || ctx.path || '/';
      const path = rawUrl.split('?')[0];
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
