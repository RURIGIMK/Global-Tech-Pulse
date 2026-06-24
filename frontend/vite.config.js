import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/Global-Tech-Pulse/',    // <-- change this
  css: {
    transformer: 'postcss',
    lightningcss: false,
    minify: 'esbuild',
  },
});