import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './assets/styles/main.css';
import './assets/styles/performance.css';

// Create Vue app instance
const app = createApp(App);

// Create Pinia store
const pinia = createPinia();

// Use plugins
app.use(pinia);
app.use(router);

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err);
  console.error('Error info:', info);
  // You can send to error tracking service here
  // e.g., Sentry, LogRocket, etc.
};

// Performance monitoring (optional)
if (import.meta.env.DEV) {
  router.afterEach((to, from) => {
    requestAnimationFrame(() => {
      performance.getEntriesByType('navigation');
    });
  });
}

// Mount app
app.mount('#app');
