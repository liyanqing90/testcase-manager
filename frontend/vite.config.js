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
      '/upload_case': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        timeout: 1800000  // 30分钟超时
      },
      '/import_case': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        timeout: 1800000
      },
      '/project': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        timeout: 1800000
      },
      '/test_case': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        timeout: 1800000
      },
      '/ai_generate': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        timeout: 1800000  // 30分钟超时，匹配后端超时设置
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})