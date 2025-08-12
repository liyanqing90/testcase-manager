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
        timeout: 1800000,  // 30分钟超时，匹配后端超时设置
        proxyTimeout: 1800000,  // 代理超时时间
        configure: (proxy, options) => {
          // 错误处理
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
            // 如果是ECONNRESET错误，尝试重新连接
            if (err.code === 'ECONNRESET') {
              console.log('Connection reset, this is normal for long-running AI operations');
            }
          });
          
          // 请求发送前
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
            // 设置keep-alive
            proxyReq.setHeader('Connection', 'keep-alive');
            // 设置更长的超时
            proxyReq.setHeader('Keep-Alive', 'timeout=1800');
          });
          
          // 响应接收后
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
            // 设置响应超时
            res.setTimeout(1800000);
          });
          
          // 连接建立
          proxy.on('open', (proxySocket) => {
            console.log('Proxy connection opened');
            // 设置socket超时
            proxySocket.setTimeout(1800000);
            proxySocket.setKeepAlive(true, 60000);
          });
          
          // 连接关闭
          proxy.on('close', (res, socket, head) => {
            console.log('Proxy connection closed');
          });
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})