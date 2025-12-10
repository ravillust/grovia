<template>
  <div class="reset-password-page">
    <div class="reset-container">
      <!-- Left Side - Form -->
      <div class="reset-form-section">
        <div class="reset-header">
          <router-link to="/" class="logo-link">
            <div class="logo-container">
              <Leaf :size="32" class="logo-icon" />
              <span class="logo-text">Grovia</span>
            </div>
          </router-link>
          <h2 class="reset-title">Reset Password</h2>
          <p class="reset-subtitle">Enter your new password below</p>
        </div>

        <!-- Success Message -->
        <div v-if="resetSuccess" class="success-container">
          <div class="success-icon-wrapper">
            <Check :size="48" class="success-icon" />
          </div>
          <h3 class="success-title">Password Reset Successful!</h3>
          <p class="success-message">Your password has been reset successfully.</p>
          <button @click="goToLogin" class="btn-primary" style="width: 100%; margin-top: 1.5rem;">
            Go to Login
          </button>
        </div>

        <!-- Reset Form -->
        <form v-else @submit.prevent="handleResetPassword" class="reset-form">
          <!-- Error Alert -->
          <div v-if="error" class="error-alert">
            <span class="alert-icon">
              <AlertCircle :size="18" />
            </span>
            <span>{{ error }}</span>
          </div>

          <!-- New Password -->
          <div class="form-group">
            <label for="new-password" class="form-label">
              <Lock :size="16" />
              New Password
            </label>
            <div class="input-wrapper">
              <input
                id="new-password"
                v-model="formData.newPassword"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Enter new password"
                required
                minlength="8"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showPassword = !showPassword"
              >
                <Eye v-if="!showPassword" :size="18" />
                <EyeOff v-else :size="18" />
              </button>
            </div>
            <p class="form-hint">Password must be at least 8 characters</p>
          </div>

          <!-- Confirm Password -->
          <div class="form-group">
            <label for="confirm-password" class="form-label">
              <Lock :size="16" />
              Confirm Password
            </label>
            <div class="input-wrapper">
              <input
                id="confirm-password"
                v-model="formData.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-input"
                placeholder="Confirm new password"
                required
                minlength="8"
              />
              <button
                type="button"
                class="toggle-password"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <Eye v-if="!showConfirmPassword" :size="18" />
                <EyeOff v-else :size="18" />
              </button>
            </div>
          </div>

          <!-- Password Strength Indicator -->
          <div v-if="formData.newPassword" class="password-strength">
            <div class="strength-bar">
              <div
                class="strength-fill"
                :class="`strength-${passwordStrength.level}`"
                :style="{ width: `${passwordStrength.percentage}%` }"
              ></div>
            </div>
            <p class="strength-text" :class="`text-${passwordStrength.level}`">
              {{ passwordStrength.text }}
            </p>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn-primary"
            :disabled="isLoading || !canSubmit"
          >
            <span v-if="!isLoading">Reset Password</span>
            <span v-else class="loading-text">
              <span class="spinner"></span>
              Resetting...
            </span>
          </button>
        </form>

        <!-- Back to Login -->
        <div class="reset-footer">
          <p class="footer-text">
            Remember your password?
            <router-link to="/login" class="footer-link">Back to Login</router-link>
          </p>
        </div>
      </div>

      <!-- Right Side - Visual -->
      <div class="reset-visual">
        <div class="visual-content">
          <div class="visual-overlay"></div>
          <div class="visual-text">
            <h2>Secure Your Account</h2>
            <p>Create a strong password to protect your Grovia account and plant health data.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Leaf, Check, Lock, Eye, EyeOff, AlertCircle } from 'lucide-vue-next';
import api from '@/services/api';

const router = useRouter();
const route = useRoute();

const formData = ref({
  newPassword: '',
  confirmPassword: '',
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isLoading = ref(false);
const error = ref('');
const resetSuccess = ref(false);

// Get token and email from URL query params
const token = ref('');
const email = ref('');

onMounted(() => {
  token.value = route.query.token || '';
  email.value = route.query.email || '';

  if (!token.value || !email.value) {
    error.value = 'Invalid reset link. Please request a new password reset.';
  }
});

// Password strength calculator
const passwordStrength = computed(() => {
  const password = formData.value.newPassword;
  if (!password) return { level: 'weak', percentage: 0, text: '' };

  let strength = 0;

  // Length check
  if (password.length >= 8) strength += 25;
  if (password.length >= 12) strength += 15;

  // Character variety
  if (/[a-z]/.test(password)) strength += 15;
  if (/[A-Z]/.test(password)) strength += 15;
  if (/[0-9]/.test(password)) strength += 15;
  if (/[^a-zA-Z0-9]/.test(password)) strength += 15;

  let level = 'weak';
  let text = 'Weak password';

  if (strength >= 70) {
    level = 'strong';
    text = 'Strong password';
  } else if (strength >= 40) {
    level = 'medium';
    text = 'Medium password';
  }

  return { level, percentage: strength, text };
});

// Check if form can be submitted
const canSubmit = computed(() => {
  return (
    formData.value.newPassword.length >= 8 &&
    formData.value.confirmPassword.length >= 8 &&
    formData.value.newPassword === formData.value.confirmPassword &&
    token.value &&
    email.value
  );
});

const handleResetPassword = async () => {
  error.value = '';

  // Validate passwords match
  if (formData.value.newPassword !== formData.value.confirmPassword) {
    error.value = 'Passwords do not match';
    return;
  }

  // Validate password strength
  if (formData.value.newPassword.length < 8) {
    error.value = 'Password must be at least 8 characters';
    return;
  }

  if (!token.value || !email.value) {
    error.value = 'Invalid reset link';
    return;
  }

  isLoading.value = true;

  try {
    const response = await api.post('/auth/reset-password', {
      token: token.value,
      email: email.value,
      new_password: formData.value.newPassword,
    });

    if (response.data.success) {
      resetSuccess.value = true;
    }
  } catch (err) {
    console.error('Reset password error:', err);

    if (err.response?.data?.detail) {
      error.value = err.response.data.detail;
    } else if (err.response?.status === 400) {
      error.value = 'Invalid or expired reset token. Please request a new password reset.';
    } else {
      error.value = 'Failed to reset password. Please try again.';
    }
  } finally {
    isLoading.value = false;
  }
};

const goToLogin = () => {
  router.push('/login');
};
</script>

<style scoped>
/* Reset Password Page Container */
.reset-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  padding: 1rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
}

.reset-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1200px;
  width: 100%;
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  min-height: 600px;
}

/* Form Section */
.reset-form-section {
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.reset-header {
  margin-bottom: 2rem;
  text-align: center;
}

.logo-link {
  text-decoration: none;
  display: inline-block;
  margin-bottom: 1.5rem;
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.logo-icon {
  color: #22c55e;
}

.logo-text {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
}

.reset-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.reset-subtitle {
  color: #64748b;
  font-size: 0.95rem;
}

/* Success Container */
.success-container {
  text-align: center;
  padding: 2rem 0;
}

.success-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border-radius: 50%;
  margin-bottom: 1.5rem;
}

.success-icon {
  color: white;
}

.success-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.success-message {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.6;
}

/* Form Styles */
.reset-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #1e293b;
  font-size: 0.875rem;
}

.input-wrapper {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 0.875rem 1rem;
  padding-right: 3rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: #f8fafc;
}

.form-input:focus {
  outline: none;
  border-color: #22c55e;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.toggle-password {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.toggle-password:hover {
  color: #1e293b;
}

.form-hint {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

/* Password Strength */
.password-strength {
  margin-top: -0.5rem;
}

.strength-bar {
  height: 4px;
  background: #e2e8f0;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.strength-fill.strength-weak {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.strength-fill.strength-medium {
  background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
}

.strength-fill.strength-strong {
  background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%);
}

.strength-text {
  font-size: 0.8rem;
  font-weight: 600;
  margin: 0;
}

.strength-text.text-weak {
  color: #ef4444;
}

.strength-text.text-medium {
  color: #f59e0b;
}

.strength-text.text-strong {
  color: #22c55e;
}

/* Alerts */
.error-alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-size: 0.875rem;
}

.alert-icon {
  display: flex;
  flex-shrink: 0;
}

/* Buttons */
.btn-primary {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Footer */
.reset-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.footer-text {
  color: #64748b;
  font-size: 0.875rem;
}

.footer-link {
  color: #22c55e;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: #16a34a;
  text-decoration: underline;
}

/* Visual Section */
.reset-visual {
  position: relative;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.visual-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.visual-overlay {
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.1;
}

.visual-text {
  position: relative;
  z-index: 2;
}

.visual-text h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.visual-text p {
  font-size: 1.1rem;
  opacity: 0.9;
  line-height: 1.6;
  max-width: 400px;
  margin: 0 auto;
}

/* Responsive Design */
@media (max-width: 968px) {
  .reset-container {
    grid-template-columns: 1fr;
  }

  .reset-visual {
    display: none;
  }

  .reset-form-section {
    padding: 2rem;
  }
}

@media (max-width: 480px) {
  .reset-form-section {
    padding: 1.5rem;
  }

  .reset-title {
    font-size: 1.5rem;
  }

  .logo-text {
    font-size: 1.5rem;
  }
}
</style>
