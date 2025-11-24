import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: {
        title: 'Grovia - Deteksi Penyakit Tanaman',
        requiresAuth: false,
      },
    },
    {
      path: '/detection',
      name: 'detection',
      component: () => import('@/views/DetectionView.vue'),
      meta: {
        title: 'Deteksi Penyakit - Grovia',
        requiresAuth: true,
      },
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryView.vue'),
      meta: {
        title: 'Riwayat Deteksi - Grovia',
        requiresAuth: true,
      },
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: {
        title: 'Login - Grovia',
        requiresAuth: false,
        hideForAuth: true, // Hide from authenticated users
      },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: {
        title: 'Daftar - Grovia',
        requiresAuth: false,
        hideForAuth: true,
      },
    },
    {
      path: '/privacy-policy',
      name: 'privacy-policy',
      component: () => import('@/views/PrivacyPolicyView.vue'),
      meta: {
        title: 'Kebijakan Privasi - Grovia',
        requiresAuth: false,
      },
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('@/views/TermsView.vue'),
      meta: {
        title: 'Syarat & Ketentuan - Grovia',
        requiresAuth: false,
      },
    },
    {
      path: '/cookie-policy',
      name: 'cookie-policy',
      component: () => import('@/views/CookiePolicyView.vue'),
      meta: {
        title: 'Kebijakan Cookie - Grovia',
        requiresAuth: false,
      },
    },
    {
      path: '/faq',
      name: 'faq',
      component: () => import('@/views/FaqView.vue'),
      meta: {
        title: 'FAQ - Grovia',
        requiresAuth: false,
      },
    },
    {
      path: '/guide',
      name: 'guide',
      component: () => import('@/views/GuideView.vue'),
      meta: {
        title: 'Panduan - Grovia',
        requiresAuth: false,
      },
    },
    {
      path: '/history/:id',
      name: 'history-detail',
      component: () => import('@/views/HistoryDetailView.vue'),
      meta: {
        title: 'Detail Riwayat - Grovia',
        requiresAuth: true,
      },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
      meta: {
        title: 'Halaman Tidak Ditemukan - Grovia',
      },
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// Navigation guards
router.beforeEach(async (to, from, next) => {
  // Set page title
  document.title = to.meta.title || 'Grovia';

  // Lazy load auth store to avoid circular dependency
  const { useAuthStore } = await import('@/stores/auth');
  const authStore = useAuthStore();

  // Check authentication from store
  const isAuthenticated = authStore.isAuthenticated;

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to login if route requires auth and user is not authenticated
    next({
      name: 'login',
      query: { redirect: to.fullPath },
    });
  } else if (to.meta.hideForAuth && isAuthenticated) {
    // Redirect to home if user is authenticated and tries to access login/register
    next({ name: 'home' });
  } else {
    next();
  }
});

// Prefetch common routes after initial load for instant navigation
router.isReady().then(() => {
  // Small delay to not block initial render
  setTimeout(() => {
    // Prefetch frequently visited routes
    import('@/views/DetectionView.vue');
    import('@/views/HistoryView.vue');
  }, 1500);
});

export default router;
