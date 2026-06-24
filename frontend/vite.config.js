import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/',
  css: {
    transformer: 'postcss',   // PostCSS (Tailwind) runs first
    lightningcss: false,      // disable LightningCSS entirely
    minify: 'esbuild',        // use esbuild for final minification
  },
});