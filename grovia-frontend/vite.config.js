import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    host: true,
    proxy: {
      // Proxy API requests to backend during development
      '/api/v1': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api\/v1/, '/api/v1'),
        configure: (proxy, _options) => {
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        },
      }
    }
  },
  build: {
    // Output directory
    outDir: 'dist',

    // Generate sourcemaps for production
    sourcemap: false,

    // Chunk size warnings
    chunkSizeWarningLimit: 1000,

    // Minify for better performance
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },

    // Rollup options
    rollupOptions: {
      output: {
        // Manual chunks for better caching and parallel loading
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          'axios-vendor': ['axios'],
          'lucide': ['lucide-vue-next'],
        }
      }
    }
  },
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia', 'axios', 'lucide-vue-next']
  }
});
