import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  server: {
    proxy: {
      '/upload_case': 'http://localhost:5000',
      '/import_case': 'http://localhost:5000',
      '/project': 'http://localhost:5000',
      '/test_case': 'http://localhost:5000',
      '/ai_generate': 'http://localhost:5000'
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})