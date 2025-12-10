<template>
  <div class="verify-email-page">
    <!-- Content -->
    <div class="verify-email-container">
      <div class="verify-email-card">
        <!-- Icon Email -->
        <div class="icon-wrapper">
          <svg class="email-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>

        <h1 class="title">Verifikasi Email Anda</h1>

        <p class="description">
          Kami telah mengirim email verifikasi ke:
        </p>

        <div class="email-box">
          <svg class="mail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
            <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
          </svg>
          <span class="email">{{ email }}</span>
        </div>

        <p class="instruction">
          Silakan buka email Anda dan klik link verifikasi untuk mengaktifkan akun.
        </p>

        <button class="gmail-btn" @click="goToGmail">
          <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z" />
            <path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z" />
          </svg>
          Buka Gmail
        </button>

        <div v-if="showResend" class="resend-section">
          <p class="resend-text">Tidak menerima email?</p>
          <button
            class="resend-btn"
            @click="resendEmail"
            :disabled="isResending"
          >
            {{ isResending ? 'Mengirim ulang...' : 'Kirim ulang email verifikasi' }}
          </button>

          <div v-if="resendSuccess" class="alert alert-success">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
            </svg>
            Email verifikasi berhasil dikirim ulang!
          </div>

          <div v-if="resendError" class="alert alert-error">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
            </svg>
            {{ resendError }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { authAPI } from '@/services/api';

const route = useRoute();
const authStore = useAuthStore();

// Ambil email dari query param atau dari store
const email = ref(route.query.email || authStore.user?.email || '');

const showResend = ref(!!email.value);
const isResending = ref(false);
const resendSuccess = ref(false);
const resendError = ref('');

function goToGmail() {
  window.open('https://mail.google.com/', '_blank');
}

async function resendEmail() {
  isResending.value = true;
  resendSuccess.value = false;
  resendError.value = '';
  try {
    await authAPI.resendVerification({ email: email.value });
    resendSuccess.value = true;
  } catch (err) {
    resendError.value = err.response?.data?.message || 'Gagal mengirim ulang email.';
  } finally {
    isResending.value = false;
  }
}
</script>

<style scoped>
/* Force navbar to be solid on this page */
:deep(.app-header) {
  background: rgba(255, 255, 255, 1) !important;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--color-border);
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

/* Page Layout */
.verify-email-page {
  min-height: 100vh;
  background: #ffffff;
  padding-top: 80px; /* Offset for MainHeader */
}

/* Content Container */
.verify-email-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  padding: 2rem;
}

.verify-email-card {
  background: #ffffff;
  padding: 3rem 2.5rem;
  border-radius: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  text-align: center;
  max-width: 500px;
  width: 100%;
  animation: slideUp 0.5s ease-out;
  border: 1px solid var(--color-border);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.email-icon {
  width: 80px;
  height: 80px;
  color: var(--color-primary);
  background: transparent;
  padding: 1.2rem;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.title {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
}

.description {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

.email-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  background: #ffffff;
  border: 2px solid var(--color-border);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.mail-icon {
  width: 24px;
  height: 24px;
  color: var(--color-primary);
  flex-shrink: 0;
}

.email {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-primary);
  word-break: break-word;
}

.instruction {
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.gmail-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  background: var(--color-primary);
  color: #fff;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.2);
}

.gmail-btn:hover {
  background: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
}

.gmail-btn:active {
  transform: translateY(0);
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.resend-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
}

.resend-text {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-bottom: 1rem;
}

.resend-btn {
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.resend-btn:hover:not(:disabled) {
  background: var(--color-primary);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.2);
}

.resend-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 12px;
  margin-top: 1rem;
  font-size: 0.9rem;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.alert-success {
  background: var(--color-success-bg);
  color: var(--color-success);
  border: 1px solid var(--color-primary-lighter);
}

.alert-success svg {
  color: var(--color-success);
}

.alert-error {
  background: var(--color-error-bg);
  color: var(--color-error);
  border: 1px solid #fecaca;
}

.alert-error svg {
  color: var(--color-error);
}

/* Responsive */
@media (max-width: 640px) {
  .verify-email-page {
    padding-top: 70px;
  }

  .verify-email-container {
    padding: 1.5rem;
    min-height: calc(100vh - 70px);
  }

  .verify-email-card {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .email-icon {
    width: 64px;
    height: 64px;
  }

  .email-box {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>
