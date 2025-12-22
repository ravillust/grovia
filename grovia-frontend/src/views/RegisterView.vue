<template>
  <div class="auth-page">
    <div class="auth-container">
      <!-- Left Side - Register Form -->
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
            <h2 class="form-title">Create Account</h2>
            <p class="form-subtitle">Fill in your details to get started</p>
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

          <!-- Register Form -->
          <form @submit.prevent="handleRegister" class="auth-form">
            <!-- Name Field -->
            <div class="form-group">
              <label for="name" class="form-label">Full Name</label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                class="form-input"
                :class="{ 'input-error': errors.name }"
                placeholder="Enter your full name"
                required
                autocomplete="name"
                @blur="validateName"
              />
              <span v-if="errors.name" class="error-message">
                {{ errors.name }}
              </span>
            </div>

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
                  autocomplete="new-password"
                  @blur="validatePassword"
                  @input="checkPasswordStrength"
                  maxlength="72"
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

              <!-- Password Strength Indicator -->
              <div v-if="formData.password" class="password-strength">
                <div class="strength-bar">
                  <div
                    class="strength-fill"
                    :class="passwordStrength.class"
                    :style="{ width: passwordStrength.width }"
                  ></div>
                </div>
                <span class="strength-text" :class="passwordStrength.class">
                  {{ passwordStrength.label }}
                </span>
              </div>

              <span v-if="errors.password" class="error-message">
                {{ errors.password }}
              </span>
            </div>

            <!-- Confirm Password Field -->
            <div class="form-group">
              <label for="password-confirm" class="form-label">
                Confirm Password
              </label>
              <div class="input-wrapper">
                <input
                  id="password-confirm"
                  v-model="formData.passwordConfirmation"
                  :type="showPasswordConfirm ? 'text' : 'password'"
                  class="form-input"
                  :class="{ 'input-error': errors.passwordConfirmation }"
                  placeholder="••••••••"
                  required
                  autocomplete="new-password"
                  @blur="validatePasswordConfirmation"
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="showPasswordConfirm = !showPasswordConfirm"
                  tabindex="-1"
                >
                  <Eye v-if="showPasswordConfirm" :size="18" />
                  <EyeOff v-else :size="18" />
                </button>
              </div>
              <span v-if="errors.passwordConfirmation" class="error-message">
                {{ errors.passwordConfirmation }}
              </span>
            </div>

            <!-- Terms & Conditions -->
            <div class="form-options">
              <label class="checkbox-label">
                <input
                  v-model="formData.agreeToTerms"
                  type="checkbox"
                  class="checkbox-input"
                  required
                />
                <span>
                  I agree to the
                  <router-link to="/terms" class="terms-link">Terms & Conditions</router-link>
                </span>
              </label>
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              class="submit-btn"
              :disabled="authStore.isLoading || !isFormValid"
            >
              <span v-if="!authStore.isLoading">Sign Up</span>
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
            <div id="google-signup-container" style="width: 100%;"></div>
          </form>

          <!-- Login Link -->
          <div class="form-footer">
            <p>
              Already have an account?
              <router-link to="/login" class="register-link">
                Sign in
              </router-link>
            </p>
          </div>
        </div>
      </div>

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
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { validateEmail as validateEmailUtil, validatePassword as validatePasswordUtil } from '@/utils/validators';
import { Leaf, Eye, EyeOff, AlertCircle, X } from 'lucide-vue-next';

const router = useRouter();
const authStore = useAuthStore();

// Google Sign-In Client ID
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '';
const googleLoaded = ref(false);

// Form data
const formData = ref({
  name: '',
  email: '',
  password: '',
  passwordConfirmation: '',
  agreeToTerms: false,
});

// Form errors
const errors = ref({
  name: '',
  email: '',
  password: '',
  passwordConfirmation: '',
});

// Show/hide passwords
const showPassword = ref(false);
const showPasswordConfirm = ref(false);

/**
 * Initialize Google Sign-In
 */
onMounted(() => {
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

          // Render button directly
          const buttonContainer = document.getElementById('google-signup-container');
          if (buttonContainer) {
            buttonContainer.innerHTML = '';

            window.google.accounts.id.renderButton(
              buttonContainer,
              {
                theme: 'outline',
                size: 'large',
                width: buttonContainer.offsetWidth,
                text: 'signup_with',
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

    // Redirect to detection page
    await router.push('/detection');
  } catch (error) {
    console.error('Google Sign-In failed:', error);
    errors.value.email = 'Google Sign-In failed. Please try again.';
  }
}

/**
 * Trigger Google Sign-In popup (fallback)
 */
function triggerGoogleSignIn() {
  errors.value.email = '';
  errors.value.name = '';
  errors.value.password = '';

  if (!GOOGLE_CLIENT_ID || GOOGLE_CLIENT_ID === 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com') {
    errors.value.email = '⚠️ Google Sign-In belum dikonfigurasi. Silakan register dengan email & password.';
    console.error('Google Client ID not configured');
    return;
  }

  if (!googleLoaded.value) {
    errors.value.email = 'Google Sign-In sedang loading. Silakan tunggu sebentar atau refresh halaman.';
    console.error('Google Sign-In not loaded yet');
    return;
  }

  errors.value.email = 'Gunakan tombol Google di atas untuk register.';
}

// Password strength
const passwordStrength = ref({
  label: '',
  class: '',
  width: '0%',
});

// Form validation
const isFormValid = computed(() => {
  return (
    formData.value.name &&
    formData.value.email &&
    formData.value.password &&
    formData.value.passwordConfirmation &&
    formData.value.agreeToTerms &&
    !errors.value.name &&
    !errors.value.email &&
    !errors.value.password &&
    !errors.value.passwordConfirmation
  );
});

/**
 * Validate name field
 */
function validateName() {
  if (!formData.value.name) {
    errors.value.name = 'Name is required';
  } else if (formData.value.name.length < 3) {
    errors.value.name = 'Name must be at least 3 characters';
  } else {
    errors.value.name = '';
  }
}

/**
 * Validate email field
 */
function validateEmail() {
  if (!formData.value.email) {
    errors.value.email = 'Email is required';
  } else if (!validateEmailUtil(formData.value.email)) {
    errors.value.email = 'Invalid email format';
  } else {
    errors.value.email = '';
  }
}

/**
 * Validate password field
 */
function validatePassword() {
  const validation = validatePasswordUtil(formData.value.password);

  if (!validation.valid) {
    errors.value.password = validation.error;
  } else {
    errors.value.password = '';
  }
}

/**
 * Validate password confirmation
 */
function validatePasswordConfirmation() {
  if (!formData.value.passwordConfirmation) {
    errors.value.passwordConfirmation = 'Password confirmation is required';
  } else if (formData.value.password !== formData.value.passwordConfirmation) {
    errors.value.passwordConfirmation = 'Passwords do not match';
  } else {
    errors.value.passwordConfirmation = '';
  }
}

/**
 * Check password strength
 */
function checkPasswordStrength() {
  const password = formData.value.password;
  let strength = 0;

  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[^a-zA-Z0-9]/.test(password)) strength++;

  if (strength <= 2) {
    passwordStrength.value = {
      label: 'Weak',
      class: 'weak',
      width: '33%',
    };
  } else if (strength <= 3) {
    passwordStrength.value = {
      label: 'Medium',
      class: 'medium',
      width: '66%',
    };
  } else {
    passwordStrength.value = {
      label: 'Strong',
      class: 'strong',
      width: '100%',
    };
  }
}

/**
 * Handle register submission
 */
async function handleRegister(event) {
  // Prevent default form submission explicitly
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }

  // Clear previous errors
  authStore.clearError();

  // Validate all fields
  validateName();
  validateEmail();
  validatePassword();
  validatePasswordConfirmation();

  if (!isFormValid.value) {

    return false;
  }

  try {
    const userData = {
      name: formData.value.name,
      email: formData.value.email,
      password: formData.value.password,
      password_confirmation: formData.value.passwordConfirmation,
    };

    const result = await authStore.register(userData);

    // Setelah registrasi sukses, redirect ke halaman verifikasi email
    if (result.success) {
      await router.push({
        name: 'verify-email',
        query: { email: formData.value.email }
      });
      return;
    }
  } catch (error) {
    console.error('Registration failed:', {
      error: error.message,
      response: error.response?.data,
      status: error.response?.status
    });
    // Error handled by store - form data is preserved
    // Make sure we don't navigate anywhere
    return false;
  }
}
</script>

<style scoped>
/* Modern Elegant Register Design */
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
  overflow-y: auto;
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

/* Error Alert */
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
  gap: 20px;
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

/* Password Strength */
.password-strength {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
}

.strength-bar {
  flex: 1;
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: width 0.3s ease, background-color 0.3s ease;
  border-radius: 2px;
}

.strength-fill.weak {
  background: #fc8181;
}

.strength-fill.medium {
  background: #ecc94b;
}

.strength-fill.strong {
  background: #48bb78;
}

.strength-text {
  font-size: 11px;
  font-weight: 600;
  min-width: 45px;
}

.strength-text.weak {
  color: #e53e3e;
}

.strength-text.medium {
  color: #d69e2e;
}

.strength-text.strong {
  color: #38a169;
}

/* Form Options */
.form-options {
  display: flex;
  justify-content: flex-start;
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

.terms-link {
  font-size: 13px;
  color: #0f172a;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
  position: relative;
}

.terms-link:hover {
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
}
</style>
