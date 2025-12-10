<template>
  <div id="app">
    <!-- Skip to main content link for accessibility -->
    <a href="#main-content" class="skip-to-main">Skip to main content</a>

    <!-- Header -->
    <Header v-if="showHeader" />

    <!-- Main Content -->
    <main id="main-content" class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <Footer v-if="showFooter" />

    <!-- Global Loading Overlay -->
    <LoadingSpinner
      v-if="globalLoading"
      fullscreen
      text="Memuat..."
      variant="primary"
    />

    <!-- Toast Notifications -->
    <ToastNotification ref="toastRef" position="top-right" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useToast } from '@/composables/useToast';
import Header from '@/components/common/MainHeader.vue';
import Footer from '@/components/common/MainFooter.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import ToastNotification from '@/components/common/ToastNotification.vue';

const route = useRoute();
const authStore = useAuthStore();
const { setToastInstance } = useToast();

// Refs
const toastRef = ref(null);

// Global loading state
const globalLoading = ref(false);

// Computed properties to conditionally show header/footer
const showHeader = computed(() => {
  // Hide header on specific routes like login, register
  const hideOnRoutes = ['login', 'register', 'verify-email'];
  return !hideOnRoutes.includes(route.name);
});

const showFooter = computed(() => {
  // Hide footer on specific routes
  const hideOnRoutes = ['login', 'register', 'verify-email'];
  return !hideOnRoutes.includes(route.name);
});

// Initialize app
onMounted(() => {
  // Initialize auth state from localStorage
  authStore.initAuth();

  // Initialize toast instance
  if (toastRef.value) {
    setToastInstance(toastRef.value);
  }
});
</script>

<style>
/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2d3748;
  background-color: #f7fafc;
}

/* Performance optimizations */
html {
  scroll-behavior: smooth;
}

* {
  /* Prevent lag during animations - use GPU acceleration wisely */
  -webkit-tap-highlight-color: transparent;
}

/* Only apply GPU acceleration to elements that animate */
.page-enter-active *,
.page-leave-active * {
  transform: translateZ(0);
  backface-visibility: hidden;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  /* Contain layout calculations */
  contain: layout style paint;
}

/* Skip to main content - Accessibility */
.skip-to-main {
  position: absolute;
  top: -100px;
  left: 0;
  background: #16a34a;
  color: white;
  padding: 12px 24px;
  text-decoration: none;
  z-index: 9999;
  border-radius: 0 0 8px 0;
  font-weight: 600;
  transition: top 0.2s;
}

.skip-to-main:focus {
  top: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Page Transitions - Ultra optimized */
.page-enter-active {
  transition: opacity 0.12s ease-out;
}

.page-leave-active {
  transition: opacity 0.08s ease-in;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}

/* Prevent layout shift during transitions */
.main-content > div {
  contain: layout;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}

/* Utility Classes */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.text-center {
  text-align: center;
}

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

/* Responsive helpers */
@media (max-width: 768px) {
  .hide-mobile {
    display: none !important;
  }
}

@media (min-width: 769px) {
  .hide-desktop {
    display: none !important;
  }
}
</style>
