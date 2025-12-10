<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-container" role="dialog" aria-labelledby="modal-title" aria-modal="true">
          <!-- Close Button -->
          <button
            class="modal-close"
            @click="closeModal"
            aria-label="Close modal"
          >
            <X :size="20" />
          </button>

          <!-- Modal Header -->
          <div class="modal-header">
            <h2 id="modal-title" class="modal-title">Reset Password</h2>
            <p class="modal-subtitle">Masukkan password baru Anda</p>
          </div>

          <!-- Success State -->
          <div v-if="isSuccess" class="success-content">
            <div class="success-icon-wrapper">
              <CheckCircle2 :size="48" class="success-icon" />
            </div>
            <h3 class="success-title">Password Berhasil Direset!</h3>
            <p class="success-message">
              Password Anda telah berhasil diubah. Silakan login dengan password baru Anda.
            </p>
            <button class="btn-primary" @click="closeModalAndLogin">
              Lanjut ke Login
            </button>
          </div>

          <!-- Reset Form -->
          <form v-else @submit.prevent="handleSubmit" class="modal-form">
            <!-- Error Alert -->
            <div v-if="error" class="error-alert">
              <AlertCircle :size="20" class="alert-icon" />
              <span>{{ error }}</span>
            </div>

            <!-- New Password -->
            <div class="form-group">
              <label for="password" class="form-label">
                <Lock :size="18" />
                Password Baru
              </label>
              <div class="input-wrapper">
                <input
                  id="password"
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Masukkan password baru"
                  required
                  minlength="8"
                  @input="calculatePasswordStrength"
                />
                <button
                  type="button"
                  class="toggle-password"
                  @click="showPassword = !showPassword"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                >
                  <Eye v-if="!showPassword" :size="20" />
                  <EyeOff v-else :size="20" />
                </button>
              </div>
              <p class="form-hint">Minimal 8 karakter, kombinasi huruf dan angka</p>
            </div>

            <!-- Password Strength -->
            <div v-if="formData.password" class="password-strength">
              <div class="strength-bar">
                <div
                  class="strength-fill"
                  :class="`strength-${passwordStrength.level}`"
                  :style="{ width: `${passwordStrength.percentage}%` }"
                ></div>
              </div>
              <p
                class="strength-text"
                :class="`text-${passwordStrength.level}`"
              >
                {{ passwordStrength.text }}
              </p>
            </div>

            <!-- Confirm Password -->
            <div class="form-group">
              <label for="confirmPassword" class="form-label">
                <Lock :size="18" />
                Konfirmasi Password
              </label>
              <div class="input-wrapper">
                <input
                  id="confirmPassword"
                  v-model="formData.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="Ulangi password baru"
                  required
                />
                <button
                  type="button"
                  class="toggle-password"
                  @click="showConfirmPassword = !showConfirmPassword"
                  :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'"
                >
                  <Eye v-if="!showConfirmPassword" :size="20" />
                  <EyeOff v-else :size="20" />
                </button>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="modal-actions">
              <button
                type="button"
                class="btn-secondary"
                @click="closeModal"
                :disabled="isLoading"
              >
                Batal
              </button>
              <button
                type="submit"
                class="btn-primary"
                :disabled="isLoading || !isFormValid"
              >
                <span v-if="!isLoading">Reset Password</span>
                <span v-else class="loading-text">
                  <span class="spinner"></span>
                  Memproses...
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { Lock, Eye, EyeOff, X, AlertCircle, CheckCircle2 } from 'lucide-vue-next';
import { useToast } from '@/composables/useToast';
import api from '@/services/api';

// Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  token: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true
  }
});

// Emits
const emit = defineEmits(['close', 'success']);

// Composables
const { showToast } = useToast();

// State
const formData = ref({
  password: '',
  confirmPassword: ''
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isLoading = ref(false);
const error = ref('');
const isSuccess = ref(false);
const passwordStrength = ref({
  level: 'weak',
  percentage: 0,
  text: ''
});

// Computed
const isFormValid = computed(() => {
  return formData.value.password.length >= 8 &&
         formData.value.password === formData.value.confirmPassword;
});

// Methods
const calculatePasswordStrength = () => {
  const password = formData.value.password;
  let strength = 0;

  if (password.length >= 8) strength += 25;
  if (password.length >= 12) strength += 25;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 25;
  if (/\d/.test(password)) strength += 15;
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength += 10;

  let level = 'weak';
  let text = 'Password Lemah';

  if (strength >= 75) {
    level = 'strong';
    text = 'Password Kuat';
  } else if (strength >= 50) {
    level = 'medium';
    text = 'Password Sedang';
  }

  passwordStrength.value = { level, percentage: strength, text };
};

const handleSubmit = async () => {
  error.value = '';

  // Validation
  if (formData.value.password !== formData.value.confirmPassword) {
    error.value = 'Password tidak cocok';
    return;
  }

  if (formData.value.password.length < 8) {
    error.value = 'Password minimal 8 karakter';
    return;
  }

  isLoading.value = true;

  try {
    await api.post('/auth/reset-password', {
      token: props.token,
      email: props.email,
      new_password: formData.value.password
    });

    isSuccess.value = true;
    showToast('Password berhasil direset!', 'success');

    // Auto close after 2 seconds
    setTimeout(() => {
      closeModalAndLogin();
    }, 2000);
  } catch (err) {
    console.error('Reset password error:', err);
    error.value = err.response?.data?.detail || 'Token tidak valid atau sudah kadaluarsa';
    showToast(error.value, 'error');
  } finally {
    isLoading.value = false;
  }
};

const closeModal = () => {
  if (!isLoading.value) {
    emit('close');
  }
};

const closeModalAndLogin = () => {
  emit('success');
  emit('close');
};

// Reset form when modal closes
watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    formData.value = {
      password: '',
      confirmPassword: ''
    };
    showPassword.value = false;
    showConfirmPassword.value = false;
    error.value = '';
    isSuccess.value = false;
    passwordStrength.value = {
      level: 'weak',
      percentage: 0,
      text: ''
    };
  }
});
</script>

<style scoped>
/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 1rem;
}

/* Modal Container */
.modal-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Close Button */
.modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: #f1f5f9;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s ease;
  z-index: 1;
}

.modal-close:hover {
  background: #e2e8f0;
  color: #1e293b;
}

/* Modal Header */
.modal-header {
  margin-bottom: 1.5rem;
  text-align: center;
  padding-right: 2rem;
}

.modal-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.modal-subtitle {
  color: #64748b;
  font-size: 0.95rem;
}

/* Success Content */
.success-content {
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
  margin-bottom: 2rem;
}

/* Form Styles */
.modal-form {
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

/* Modal Actions */
.modal-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 0.5rem;
}

/* Buttons */
.btn-primary,
.btn-secondary {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
}

.btn-secondary {
  background: #f1f5f9;
  color: #64748b;
}

.btn-secondary:hover:not(:disabled) {
  background: #e2e8f0;
  color: #1e293b;
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
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

/* Success state button */
.success-content .btn-primary {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

/* Modal Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-container {
  animation: modalSlideIn 0.3s ease-out;
}

.modal-fade-leave-active .modal-container {
  animation: modalSlideOut 0.3s ease-in;
}

@keyframes modalSlideOut {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
}

/* Responsive */
@media (max-width: 480px) {
  .modal-container {
    padding: 1.5rem;
  }

  .modal-title {
    font-size: 1.5rem;
  }

  .modal-actions {
    grid-template-columns: 1fr;
  }
}

/* Scrollbar */
.modal-container::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.modal-container::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
