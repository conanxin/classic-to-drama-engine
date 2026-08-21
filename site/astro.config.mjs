import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://conanxin.github.io',
  base: '/classic-to-drama-engine/',
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()],
  build: {
    assets: 'assets'
  },
  vite: {
    build: {
      sourcemap: false
    }
  }
});
