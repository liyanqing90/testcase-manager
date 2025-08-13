import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// 自定义插件：处理前端路由刷新
const historyFallbackPlugin = () => {
  return {
    name: 'history-fallback',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // 如果是API请求，直接跳过
        if (req.url.startsWith('/logs/') || 
            req.url.startsWith('/upload_case/') || 
            req.url.startsWith('/import_case/') || 
            req.url.startsWith('/project/') || 
            req.url.startsWith('/test_case/') || 
            req.url.startsWith('/ai_generate/')) {
          return next()
        }
        
        // 如果是前端路由，返回index.html
        if (req.url.startsWith('/logs') || 
            req.url.startsWith('/manage') || 
            req.url.startsWith('/upload') || 
            req.url.startsWith('/ai-generate')) {
          req.url = '/index.html'
        }
        
        next()
      })
    }
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    historyFallbackPlugin(),
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
      },
      '/logs': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        timeout: 30000,  // 30秒超时
        proxyTimeout: 30000
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})