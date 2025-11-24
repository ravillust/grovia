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
                  <a href="#" class="terms-link">Terms & Conditions</a>
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

            <!-- Google Sign In -->
            <button type="button" class="google-btn">
              <svg class="google-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Sign Up with Google
            </button>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { validateEmail as validateEmailUtil, validatePassword as validatePasswordUtil } from '@/utils/validators';
import { Leaf, Eye, EyeOff, AlertCircle, X } from 'lucide-vue-next';

const router = useRouter();
const authStore = useAuthStore();

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
    console.log('Form validation failed');
    return false;
  }

  // Check if backend is running
  const isBackendRunning = await axios.get('http://localhost:8000/api/v1/health-check')
    .catch(() => false);

  if (!isBackendRunning) {
    authStore.error = 'Cannot connect to server. Please make sure the backend is running.';
    return false;
  }

  try {
    const userData = {
      name: formData.value.name,
      email: formData.value.email,
      password: formData.value.password,
      password_confirmation: formData.value.passwordConfirmation,
    };
    console.log('Attempting to register with:', { ...userData, password: '***', password_confirmation: '***' });

    const result = await authStore.register(userData);
    console.log('Registration result:', result);
    console.log('Auth store state after registration:', {
      isAuthenticated: authStore.isAuthenticated,
      hasToken: !!authStore.token,
      hasUser: !!authStore.user,
      token: authStore.token,
      user: authStore.user
    });

    // Check if user is automatically logged in
    if (authStore.isAuthenticated && authStore.token && authStore.user) {
      // User is logged in, redirect to detection page
      console.log('✅ User auto-logged in successfully, redirecting to detection');
      await router.push('/detection');
    } else {
      // User not auto-logged in, need to login manually
      console.log('⚠️ User not auto-logged in, backend did not return token');
      console.log('Redirecting to login page...');

      // Auto-login with the credentials
      console.log('Attempting auto-login with provided credentials...');
      try {
        await authStore.login({
          email: formData.value.email,
          password: formData.value.password,
        });
        console.log('✅ Auto-login successful, redirecting to detection');
        await router.push('/detection');
      } catch (loginError) {
        console.error('❌ Auto-login failed:', loginError);
        // Fallback to login page
        await router.push('/login');
      }
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
