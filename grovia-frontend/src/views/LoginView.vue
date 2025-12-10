<template>
  <div class="auth-page">
    <div class="auth-container">
      <!-- Left Side - Login Form -->
      <div class="auth-form-section">
        <div class="auth-form-container">
          <!-- Brand Logo -->
          <div class="brand-header">
            <div class="brand-logo-small">
              <Leaf :size="32" :stroke-width="2" />
            </div>
            <span class="brand-name">Grovia.</span>
          </div>

          <!-- Form Header -->
          <div class="form-header">
            <h2 class="form-title">Welcome back!</h2>
            <p class="form-subtitle">The faster you fill up, the faster you get a ticket</p>
          </div>

          <!-- Error Message -->
          <div v-if="authStore.error" class="error-alert">
            <span class="alert-icon">
              <AlertCircle :size="18" />
            </span>
            <span>{{ authStore.error }}</span>
            <button class="alert-close" @click="authStore.clearError">
              <X :size="16" />
            </button>
          </div>

          <!-- Login Form -->
          <form @submit.prevent="handleLogin" class="auth-form">
            <!-- Email Field -->
            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                class="form-input"
                :class="{ 'input-error': errors.email }"
                placeholder="Enter your email"
                required
                autocomplete="email"
                @blur="validateEmail"
              />
              <span v-if="errors.email" class="error-message">
                {{ errors.email }}
              </span>
            </div>

            <!-- Password Field -->
            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <div class="input-wrapper">
                <input
                  id="password"
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  :class="{ 'input-error': errors.password }"
                  placeholder="••••••••"
                  required
                  autocomplete="current-password"
                  @blur="validatePassword"
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                  tabindex="-1"
                >
                  <Eye v-if="showPassword" :size="18" />
                  <EyeOff v-else :size="18" />
                </button>
              </div>
              <span v-if="errors.password" class="error-message">
                {{ errors.password }}
              </span>
            </div>

            <!-- Remember Me & Forgot Password -->
            <div class="form-options">
              <label class="checkbox-label">
                <input
                  v-model="formData.rememberMe"
                  type="checkbox"
                  class="checkbox-input"
                />
                <span>Remember me</span>
              </label>
              <a href="#" class="forgot-link" @click.prevent="showForgotPassword = true">Forgot Password</a>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              class="submit-btn"
              :disabled="authStore.isLoading || !isFormValid"
            >
              <span v-if="!authStore.isLoading">Sign In</span>
              <span v-else class="loading-text">
                <span class="spinner-small"></span>
                Processing...
              </span>
            </button>

            <!-- Divider -->
            <div class="divider">
              <span>or</span>
            </div>

            <!-- Google Sign In Container -->
            <!-- Google will automatically render its button here -->
            <div id="google-signin-container" style="width: 100%;"></div>
          </form>

          <!-- Register Link -->
          <div class="form-footer">
            <p>
              Don't have an account?
              <router-link to="/register" class="register-link">
                Sign up
              </router-link>
            </p>
          </div>
        </div>
      </div>

      <!-- Forgot Password Modal -->
      <Transition name="modal">
        <div v-if="showForgotPassword" class="modal-overlay" @click="closeForgotPassword">
          <div class="modal-content" @click.stop>
            <div class="modal-header">
              <h3 class="modal-title">Reset Password</h3>
              <button class="modal-close" @click="closeForgotPassword">
                <X :size="20" />
              </button>
            </div>

            <div class="modal-body">
              <p class="modal-description">
                Enter your email address and we'll send you a link to reset your password.
              </p>

              <!-- Success Message -->
              <div v-if="resetSuccess" class="success-alert">
                <span class="alert-icon">
                  <Check :size="18" />
                </span>
                <span>Password reset link has been sent to your email!</span>
              </div>

              <!-- Error Message -->
              <div v-if="resetError" class="error-alert">
                <span class="alert-icon">
                  <AlertCircle :size="18" />
                </span>
                <span>{{ resetError }}</span>
              </div>

              <form @submit.prevent="handleForgotPassword" v-if="!resetSuccess">
                <div class="form-group">
                  <label for="reset-email" class="form-label">Email</label>
                  <input
                    id="reset-email"
                    v-model="resetEmail"
                    type="email"
                    class="form-input"
                    placeholder="Enter your email"
                    required
                  />
                </div>

                <div class="modal-actions">
                  <button
                    type="button"
                    class="btn-secondary"
                    @click="closeForgotPassword"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    class="btn-primary"
                    :disabled="isResetting || !resetEmail"
                  >
                    <span v-if="!isResetting">Send Reset Link</span>
                    <span v-else class="loading-text">
                      <span class="spinner-small"></span>
                      Sending...
                    </span>
                  </button>
                </div>
              </form>

              <div v-else class="modal-actions">
                <button class="btn-primary" @click="closeForgotPassword" style="width: 100%;">
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Reset Password Modal -->
      <ResetPasswordModal
        :is-open="showResetPasswordModal"
        :token="resetToken"
        :email="resetEmailFromUrl"
        @close="handleResetPasswordClose"
        @success="handleResetPasswordSuccess"
      />

      <!-- Right Side - Visual/Image -->
      <div class="auth-visual">
        <div class="visual-content">
          <div class="visual-overlay"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { validateEmail as validateEmailUtil } from '@/utils/validators';
import { Leaf, Check, Mail, Lock, Eye, EyeOff, AlertCircle, X } from 'lucide-vue-next';
import ResetPasswordModal from '@/components/common/ResetPasswordModal.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// Form data
const formData = ref({
  email: '',
  password: '',
  rememberMe: false,
});

// Form errors
const errors = ref({
  email: '',
  password: '',
});

// Show/hide password
const showPassword = ref(false);

// Forgot password state
const showForgotPassword = ref(false);
const resetEmail = ref('');
const resetSuccess = ref(false);
const resetError = ref('');
const isResetting = ref(false);

// Reset password modal state
const showResetPasswordModal = ref(false);
const resetToken = ref('');
const resetEmailFromUrl = ref('');

// Google Sign-In Client ID - REPLACE WITH YOUR ACTUAL CLIENT ID
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '';
const googleLoaded = ref(false);

// Form validation
const isFormValid = computed(() => {
  return (
    formData.value.email &&
    formData.value.password &&
    !errors.value.email &&
    !errors.value.password
  );
});

/**
 * Initialize Google Sign-In
 */
onMounted(() => {
  // Check if there's a reset password token in URL
  const token = route.query.token;
  const email = route.query.email;

  if (token && email) {
    resetToken.value = token;
    resetEmailFromUrl.value = email;
    showResetPasswordModal.value = true;

    // Clean URL without reloading
    router.replace({ query: {} });
  }

  // Wait for Google script to load
  const initGoogle = () => {
    if (window.google && window.google.accounts) {
      try {
        if (GOOGLE_CLIENT_ID && GOOGLE_CLIENT_ID !== 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com') {
          window.google.accounts.id.initialize({
            client_id: GOOGLE_CLIENT_ID,
            callback: handleGoogleSignIn,
            auto_select: false,
            cancel_on_tap_outside: false,
          });

          // Render button directly instead of using prompt
          const buttonContainer = document.getElementById('google-signin-container');
          if (buttonContainer) {
            // Clear existing content
            buttonContainer.innerHTML = '';

            // Render Google button
            window.google.accounts.id.renderButton(
              buttonContainer,
              {
                theme: 'outline',
                size: 'large',
                width: buttonContainer.offsetWidth,
                text: 'signin_with',
                shape: 'rectangular',
              }
            );
          }

          googleLoaded.value = true;

        } else {
          console.warn('⚠️ Google Client ID not configured. Set VITE_GOOGLE_CLIENT_ID in .env');
        }
      } catch (error) {
        console.error('❌ Error initializing Google Sign-In:', error);
      }
    } else {
      // Retry after a short delay
      setTimeout(initGoogle, 500);
    }
  };

  initGoogle();
});

/**
 * Handle Google Sign-In callback
 */
async function handleGoogleSignIn(response) {
  try {

    // Send the credential to backend
    await authStore.googleSignIn(response.credential);

    // Wait a bit for state to update
    await new Promise(resolve => setTimeout(resolve, 100));

    // Redirect to intended page or detection page
    const redirect = router.currentRoute.value.query.redirect || '/detection';
    await router.push(redirect);
  } catch (error) {
    console.error('Google Sign-In failed:', error);
    errors.value.email = 'Google Sign-In failed. Please try again.';
  }
}

/**
 * Trigger Google Sign-In popup (fallback for custom button)
 */
function triggerGoogleSignIn() {
  // Clear previous errors
  errors.value.email = '';
  errors.value.password = '';

  if (!GOOGLE_CLIENT_ID || GOOGLE_CLIENT_ID === 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com') {
    errors.value.email = '⚠️ Google Sign-In belum dikonfigurasi. Silakan login dengan email & password.';
    console.error('Google Client ID not configured');
    return;
  }

  if (!googleLoaded.value) {
    errors.value.email = 'Google Sign-In sedang loading. Silakan tunggu sebentar atau refresh halaman.';
    console.error('Google Sign-In not loaded yet');
    return;
  }

  // Button should be auto-rendered by Google, this is just fallback
  errors.value.email = 'Gunakan tombol Google di atas untuk login.';
}

/**
 * Validate email field
 */
function validateEmail() {
  if (!formData.value.email) {
    errors.value.email = 'Email wajib diisi';
  } else if (!validateEmailUtil(formData.value.email)) {
    errors.value.email = 'Format email tidak valid';
  } else {
    errors.value.email = '';
  }
}

/**
 * Validate password field
 */
function validatePassword() {
  if (!formData.value.password) {
    errors.value.password = 'Password wajib diisi';
  } else if (formData.value.password.length < 6) {
    errors.value.password = 'Password minimal 6 karakter';
  } else {
    errors.value.password = '';
  }
}

/**
 * Handle login submission
 */
async function handleLogin() {
  // Validate all fields
  validateEmail();
  validatePassword();

  if (!isFormValid.value) {
    return;
  }

  try {
    const result = await authStore.login({
      email: formData.value.email,
      password: formData.value.password,
    });


    // Wait a bit for state to update
    await new Promise(resolve => setTimeout(resolve, 100));

    // Redirect to intended page or detection page
    const redirect = router.currentRoute.value.query.redirect || '/detection';

    await router.push(redirect);
  } catch (error) {
    // Error handled by store
    console.error('Login failed:', error);
  }
}

/**
 * Handle forgot password
 */
async function handleForgotPassword() {
  if (!resetEmail.value) return;

  isResetting.value = true;
  resetError.value = '';
  resetSuccess.value = false;

  try {
    // Panggil API forgot password
    await authStore.forgotPassword(resetEmail.value);
    resetSuccess.value = true;

  } catch (error) {
    resetError.value = 'Failed to send reset link. Please try again.';
    console.error('Forgot password error:', error);
  } finally {
    isResetting.value = false;
  }
}

/**
 * Close forgot password modal
 */
function closeForgotPassword() {
  showForgotPassword.value = false;
  resetEmail.value = '';
  resetSuccess.value = false;
  resetError.value = '';
}

/**
 * Handle reset password modal close
 */
function handleResetPasswordClose() {
  showResetPasswordModal.value = false;
  resetToken.value = '';
  resetEmailFromUrl.value = '';
}

/**
 * Handle reset password success
 */
function handleResetPasswordSuccess() {
  // Modal will auto-close and user can now login
  showResetPasswordModal.value = false;
  resetToken.value = '';
  resetEmailFromUrl.value = '';
}
</script>

<style scoped>
/* Modern Elegant Login Design */
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  padding: 0;
}

.auth-container {
  display: grid;
  grid-template-columns: 480px 1fr;
  max-width: 100%;
  width: 100%;
  height: 100vh;
  background: white;
  overflow: hidden;
}

/* Left Side - Form Section */
.auth-form-section {
  padding: 60px 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
}

.auth-form-container {
  width: 100%;
  max-width: 380px;
}

/* Brand Header */
.brand-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 60px;
}

.brand-logo-small {
  color: #16a34a;
  display: flex;
  align-items: center;
}

.brand-name {
  font-size: 24px;
  font-weight: 600;
  color: #0f172a;
  letter-spacing: -0.02em;
}

/* Form Header */
.form-header {
  margin-bottom: 40px;
}

.form-title {
  font-size: 32px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.form-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

/* Error Alert - Softer */
.error-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  color: #dc2626;
  font-size: 14px;
  margin-bottom: 24px;
  animation: slideDownBounce 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideDownBounce {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.alert-close {
  margin-left: auto;
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.alert-close:hover {
  background-color: rgba(220, 38, 38, 0.15);
  transform: scale(1.1);
}

.alert-close:active {
  transform: scale(0.9);
}

/* Form Styling */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
  background: #fafafa;
  color: #0f172a;
}

.form-input::placeholder {
  color: #94a3b8;
}

.form-input:hover {
  background: white;
  border-color: #cbd5e1;
}

.form-input:focus {
  outline: none;
  border-color: #0f172a;
  background: white;
  box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.05);
}

.form-input.input-error {
  border-color: #ef4444;
}

.password-toggle {
  position: absolute;
  right: 14px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  opacity: 0.5;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.password-toggle:hover {
  opacity: 1;
}

.error-message {
  font-size: 12px;
  color: #ef4444;
  font-weight: 500;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
  transition: color 0.2s ease;
  user-select: none;
}

.checkbox-label:hover {
  color: #0f172a;
}

.checkbox-input {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: #0f172a;
  transition: transform 0.2s ease;
}

.checkbox-input:hover {
  transform: scale(1.1);
}

.checkbox-input:active {
  transform: scale(0.95);
}

.forgot-link {
  font-size: 13px;
  color: #0f172a;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
  position: relative;
}

.forgot-link:hover {
  color: #16a34a;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 13px;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.submit-btn:hover:not(:disabled) {
  background: #1e293b;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spinner-small {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
  color: #94a3b8;
  font-size: 12px;
  text-transform: lowercase;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e2e8f0;
}

.divider span {
  padding: 0 16px;
}

/* Google Sign-In Container */
#google-signin-container {
  width: 100%;
}

/* Google Button */
.google-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #0f172a;
}

.google-btn:hover {
  border-color: #cbd5e1;
  background: #fafafa;
}

.google-icon {
  flex-shrink: 0;
}

/* Form Footer */
.form-footer {
  margin-top: 32px;
  text-align: center;
  font-size: 13px;
  color: #64748b;
}

.register-link {
  color: #0f172a;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.register-link:hover {
  color: #16a34a;
}

/* Right Side - Visual */
.auth-visual {
  position: relative;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  overflow: hidden;
}

.visual-content {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/image/still-life-with-indoor-plants.jpg');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: flex-end;
  justify-content: flex-start;
  padding: 60px;
}

.visual-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(22, 163, 74, 0.85) 0%, rgba(21, 128, 61, 0.85) 100%);
  mix-blend-mode: multiply;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 450px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
  letter-spacing: -0.02em;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.modal-body {
  padding: 28px;
  overflow-y: auto;
}

.modal-description {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 24px 0;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-primary,
.btn-secondary {
  flex: 1;
  padding: 11px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: #0f172a;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #1e293b;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #0f172a;
  border: 1px solid #e2e8f0;
}

.btn-secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.success-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #dcfce7;
  border: 1px solid #bbf7d0;
  border-radius: 10px;
  color: #16a34a;
  font-size: 14px;
  margin-bottom: 24px;
  animation: slideDownBounce 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Modal Transitions */
.modal-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-leave-active {
  transition: all 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content {
  transform: scale(0.9) translateY(-20px);
}

.modal-leave-to .modal-content {
  transform: scale(0.95) translateY(10px);
}

/* Responsive */
@media (max-width: 1024px) {
  .auth-container {
    grid-template-columns: 1fr;
  }

  .auth-visual {
    display: none;
  }

  .auth-form-section {
    padding: 40px;
  }
}

@media (max-width: 640px) {
  .auth-form-section {
    padding: 32px 24px;
  }

  .brand-header {
    margin-bottom: 48px;
  }

  .form-title {
    font-size: 28px;
  }

  .modal-content {
    margin: 0 16px;
  }
}
</style>
