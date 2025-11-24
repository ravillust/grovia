<template>
  <header class="app-header" :class="{ scrolled: isScrolled }">
    <div class="header-container">
      <!-- Logo & Brand -->
      <router-link to="/" class="brand" aria-label="Grovia - Beranda">
        <div class="logo" aria-hidden="true">
          <Leaf :size="28" :stroke-width="2" />
        </div>
        <span class="brand-name">Grovia</span>
      </router-link>

      <!-- Desktop Navigation -->
      <nav class="desktop-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-link"
          :class="{ active: isActive(item.path) }"
        >
          <span class="nav-text">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- User Actions -->
      <div class="user-actions">
        <template v-if="isAuthenticated">
          <button
            class="user-menu-btn"
            @click="toggleUserMenu"
            :aria-expanded="showUserMenu"
            aria-haspopup="true"
            aria-label="Menu pengguna"
          >
            <div class="user-avatar" aria-hidden="true">
              <User :size="18" :stroke-width="2" />
            </div>
            <span class="user-name">{{ userName }}</span>
            <span class="dropdown-icon" aria-hidden="true">▼</span>
          </button>

          <!-- User Dropdown Menu -->
          <transition name="dropdown">
            <div v-if="showUserMenu" class="user-dropdown" @click.stop>
              <div class="dropdown-header">
                <div class="user-avatar-dropdown">{{ userInitials }}</div>
                <div class="user-info">
                  <p class="dropdown-name">{{ userName }}</p>
                  <p class="dropdown-email">{{ userEmail }}</p>
                </div>
              </div>
              <button class="dropdown-item logout-btn" @click="handleLogout">
                <LogOut :size="16" />
                <span>Logout</span>
              </button>
            </div>
          </transition>
        </template>

        <template v-else>
          <router-link to="/login" class="btn-login">Login</router-link>
          <router-link to="/register" class="btn-register">Daftar</router-link>
        </template>
      </div>

      <!-- Mobile Menu Button -->
      <button
        class="mobile-menu-btn"
        @click="toggleMobileMenu"
        :aria-expanded="showMobileMenu"
        aria-label="Toggle menu"
        aria-controls="mobile-navigation"
      >
        <span class="hamburger" :class="{ open: showMobileMenu }" aria-hidden="true"></span>
      </button>
    </div>

    <!-- Mobile Navigation -->
    <transition name="mobile-menu">
      <nav v-if="showMobileMenu" class="mobile-nav" id="mobile-navigation" role="navigation" aria-label="Menu navigasi mobile">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="mobile-nav-link"
          @click="closeMobileMenu"
        >
          <component :is="iconComponents[item.icon]" :size="20" class="nav-icon" />
          <span class="nav-text">{{ item.label }}</span>
        </router-link>

        <div v-if="!isAuthenticated" class="mobile-auth-buttons">
          <router-link to="/login" class="btn-mobile-login" @click="closeMobileMenu">
            Login
          </router-link>
          <router-link to="/register" class="btn-mobile-register" @click="closeMobileMenu">
            Daftar
          </router-link>
        </div>
      </nav>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { Leaf, LogOut, Home, Search, FileText, User } from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// State
const showUserMenu = ref(false);
const showMobileMenu = ref(false);
const isScrolled = ref(false);

// Navigation items
const navItems = [
  { path: '/', label: 'Beranda', icon: 'Home' },
  { path: '/detection', label: 'Deteksi', icon: 'Search' },
  { path: '/history', label: 'Riwayat', icon: 'FileText' },
];

// Icon components map (not used since icons removed from nav)
const iconComponents = {
  Home,
  Search,
  FileText,
};

// Computed
const isAuthenticated = computed(() => authStore.isAuthenticated);
const userName = computed(() => authStore.user?.name || 'User');
const userEmail = computed(() => authStore.user?.email || '');
const userInitials = computed(() => {
  const name = userName.value;
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
});

// Methods
function isActive(path) {
  return route.path === path;
}

function toggleUserMenu() {
  showUserMenu.value = !showUserMenu.value;
}

function closeUserMenu() {
  showUserMenu.value = false;
}

function toggleMobileMenu() {
  showMobileMenu.value = !showMobileMenu.value;
}

function closeMobileMenu() {
  showMobileMenu.value = false;
}

async function handleLogout() {
  closeUserMenu();
  try {
    await authStore.logout();
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
  }
}

// Click outside functionality
function handleClickOutside(event) {
  const userActions = document.querySelector('.user-actions');
  if (userActions && !userActions.contains(event.target)) {
    closeUserMenu();
  }
}

// Scroll detection
function handleScroll() {
  // Only detect scroll on homepage
  if (route.path === '/') {
    isScrolled.value = window.scrollY > 20;
  }
}

// Check if current route needs dark navbar
function shouldUseDarkNavbar() {
  const whiteBackgroundPages = ['/detection', '/history'];
  return whiteBackgroundPages.includes(route.path);
}

// Watch route changes
watch(() => route.path, (newPath) => {
  if (shouldUseDarkNavbar()) {
    isScrolled.value = true;
  } else {
    isScrolled.value = window.scrollY > 20;
  }
});

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('scroll', handleScroll);
  // Set initial state based on current page
  if (shouldUseDarkNavbar()) {
    isScrolled.value = true;
  }
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.app-header {
  background: transparent;
  backdrop-filter: blur(0px);
  border-bottom: none;
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
}

/* Scrolled state - Add blur and background */
.app-header.scrolled {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.header-container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 20px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
}

/* Brand - Clean & Simple */
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #ffffff;
  transition: opacity 0.3s ease;
}

.brand:hover {
  opacity: 0.9;
}

.logo {
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.03em;
  font-feature-settings: 'ss01' 1;
}

/* Dark text when scrolled */
.app-header.scrolled .brand,
.app-header.scrolled .brand-name {
  color: #0f172a;
}

.app-header.scrolled .logo {
  color: #6aa581;
}

/* Desktop Navigation - Minimal */
.desktop-nav {
  display: flex;
  gap: 2px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 9px 20px;
  border-radius: 10px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  font-size: 15px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

/* Dark nav when scrolled */
.app-header.scrolled .nav-link {
  color: #64748b;
}

.app-header.scrolled .nav-link:hover {
  background-color: #f8fafc;
  color: #6aa581;
}

.app-header.scrolled .nav-link.active {
  background-color: #f1f5f9;
  color: #6aa581;
}

.nav-link:focus-visible {
  outline: 2px solid #16a34a;
  outline-offset: 2px;
  border-radius: 8px;
}

.nav-icon {
  color: inherit;
}

.nav-text {
  font-size: 15px;
}

/* User Actions - Clean */
.user-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 50;
}

.user-menu-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  z-index: 10;
}

.user-menu-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
}

/* Scrolled state */
.app-header.scrolled .user-menu-btn {
  background: white;
  border-color: #e2e8f0;
}

.app-header.scrolled .user-menu-btn:hover {
  border-color: #cbd5e0;
  background-color: #f8fafc;
}

.user-menu-btn:focus-visible {
  outline: 2px solid #16a34a;
  outline-offset: 2px;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6aa581, #5a9470);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar svg {
  display: block;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
}

.dropdown-icon {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.7);
}

/* Dark text when scrolled */
.app-header.scrolled .user-name {
  color: #0f172a;
}

.app-header.scrolled .dropdown-icon {
  color: #94a3b8;
}

/* User Dropdown - Minimal Clean */
.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(0, 0, 0, 0.04);
  min-width: 240px;
  overflow: hidden;
  z-index: 1000;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.user-avatar-dropdown {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6aa581, #5a9470);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.dropdown-name {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 2px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-email {
  font-size: 12px;
  color: #64748b;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: none;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.logout-btn:hover {
  background-color: #f8fafc;
  color: #0f172a;
}

.logout-btn svg {
  flex-shrink: 0;
}

/* Auth Buttons - Simple */
.btn-login,
.btn-register {
  padding: 10px 24px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
}

.btn-login {
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: transparent;
}

.btn-login:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-register {
  background: #ffffff;
  color: #2d5f4a;
  border: 1px solid transparent;
}

.btn-register:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-1px);
}

/* Scrolled state */
.app-header.scrolled .btn-login {
  color: #64748b;
  border-color: #e2e8f0;
  background: white;
}

.app-header.scrolled .btn-login:hover {
  background-color: #f8fafc;
  border-color: #cbd5e0;
  color: #6aa581;
}

.app-header.scrolled .btn-register {
  background: #6aa581;
  color: white;
}

.app-header.scrolled .btn-register:hover {
  background: #5a9470;
}

.btn-login:focus-visible,
.btn-register:focus-visible {
  outline: 2px solid #16a34a;
  outline-offset: 2px;
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.mobile-menu-btn:hover {
  background-color: #f8fafc;
}

.mobile-menu-btn:focus-visible {
  outline: 2px solid #16a34a;
  outline-offset: 2px;
}

.hamburger {
  display: block;
  width: 22px;
  height: 2px;
  background-color: #475569;
  position: relative;
  transition: background-color 0.3s ease;
}

.hamburger::before,
.hamburger::after {
  content: '';
  display: block;
  width: 22px;
  height: 2px;
  background-color: #475569;
  position: absolute;
  transition: transform 0.3s ease;
}

.hamburger::before {
  top: -7px;
}

.hamburger::after {
  top: 7px;
}

.hamburger.open {
  background-color: transparent;
}

.hamburger.open::before {
  transform: translateY(7px) rotate(45deg);
}

.hamburger.open::after {
  transform: translateY(-7px) rotate(-45deg);
}

/* Mobile Navigation */
.mobile-nav {
  display: none;
  flex-direction: column;
  padding: 12px 20px 20px;
  background: white;
  border-top: 1px solid #f1f5f9;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: #64748b;
  font-weight: 500;
  transition: all 0.2s ease;
}

.mobile-nav-link:hover {
  background-color: #f8fafc;
  color: #16a34a;
}

.mobile-auth-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.btn-mobile-login,
.btn-mobile-register {
  padding: 11px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  text-align: center;
  transition: all 0.2s ease;
}

.btn-mobile-login {
  color: #64748b;
  border: 1px solid #e2e8f0;
  background: white;
}

.btn-mobile-register {
  background: #16a34a;
  color: white;
  border: 1px solid #16a34a;
}

/* Transitions - Smooth */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  max-height: 0;
}

.mobile-menu-enter-to,
.mobile-menu-leave-from {
  opacity: 1;
  max-height: 500px;
}

/* Responsive */
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }

  .user-actions .user-name,
  .user-actions .dropdown-icon {
    display: none;
  }

  .btn-login,
  .btn-register {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }

  .mobile-nav {
    display: flex;
  }
}

@media (max-width: 480px) {
  .brand-name {
    font-size: 19px;
  }

  .logo {
    transform: scale(0.9);
  }
}
</style>
