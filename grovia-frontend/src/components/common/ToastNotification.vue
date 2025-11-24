<template>
  <teleport to="body">
    <transition-group
      name="toast-list"
      tag="div"
      class="toast-container"
      :style="{ [position.includes('top') ? 'top' : 'bottom']: '24px', [position.includes('right') ? 'right' : 'left']: '24px' }"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="[`toast-${toast.type}`, { 'toast-dismissing': toast.dismissing }]"
        role="alert"
        :aria-live="toast.type === 'error' ? 'assertive' : 'polite'"
      >
        <div class="toast-icon" aria-hidden="true">
          <CheckCircle v-if="toast.type === 'success'" :size="20" />
          <AlertCircle v-else-if="toast.type === 'error'" :size="20" />
          <Info v-else-if="toast.type === 'info'" :size="20" />
          <AlertTriangle v-else-if="toast.type === 'warning'" :size="20" />
        </div>

        <div class="toast-content">
          <p v-if="toast.title" class="toast-title">{{ toast.title }}</p>
          <p class="toast-message">{{ toast.message }}</p>
        </div>

        <button
          class="toast-close"
          @click="removeToast(toast.id)"
          aria-label="Tutup notifikasi"
        >
          <X :size="16" />
        </button>

        <div
          v-if="toast.duration > 0"
          class="toast-progress"
          :style="{ animationDuration: `${toast.duration}ms` }"
        ></div>
      </div>
    </transition-group>
  </teleport>
</template>

<script setup>
import { ref } from 'vue';
import { CheckCircle, AlertCircle, Info, AlertTriangle, X } from 'lucide-vue-next';

defineProps({
  position: {
    type: String,
    default: 'top-right', // top-right, top-left, bottom-right, bottom-left
    validator: (value) => ['top-right', 'top-left', 'bottom-right', 'bottom-left'].includes(value),
  },
});

const toasts = ref([]);
let toastId = 0;

/**
 * Show toast notification
 */
function showToast({ type = 'info', title = '', message, duration = 5000 }) {
  const id = ++toastId;
  const toast = {
    id,
    type,
    title,
    message,
    duration,
    dismissing: false,
  };

  toasts.value.push(toast);

  if (duration > 0) {
    setTimeout(() => {
      removeToast(id);
    }, duration);
  }

  return id;
}

/**
 * Remove toast by id
 */
function removeToast(id) {
  const index = toasts.value.findIndex(t => t.id === id);
  if (index !== -1) {
    toasts.value[index].dismissing = true;
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id);
    }, 300);
  }
}

/**
 * Clear all toasts
 */
function clearAll() {
  toasts.value.forEach(toast => {
    toast.dismissing = true;
  });
  setTimeout(() => {
    toasts.value = [];
  }, 300);
}

// Expose methods
defineExpose({
  showToast,
  removeToast,
  clearAll,
  success: (message, title) => showToast({ type: 'success', title, message }),
  error: (message, title) => showToast({ type: 'error', title, message }),
  warning: (message, title) => showToast({ type: 'warning', title, message }),
  info: (message, title) => showToast({ type: 'info', title, message }),
});
</script>

<style scoped>
.toast-container {
  position: fixed;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 420px;
  width: 100%;
  pointer-events: none;
}

.toast {
  background: white;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-left: 4px solid;
  pointer-events: auto;
  position: relative;
  overflow: hidden;
}

.toast-success {
  border-left-color: #16a34a;
}

.toast-error {
  border-left-color: #dc2626;
}

.toast-warning {
  border-left-color: #f59e0b;
}

.toast-info {
  border-left-color: #0891b2;
}

.toast-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.toast-success .toast-icon {
  background: #dcfce7;
  color: #16a34a;
}

.toast-error .toast-icon {
  background: #fee2e2;
  color: #dc2626;
}

.toast-warning .toast-icon {
  background: #fef3c7;
  color: #f59e0b;
}

.toast-info .toast-icon {
  background: #cffafe;
  color: #0891b2;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 4px 0;
  letter-spacing: -0.01em;
}

.toast-message {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
  word-wrap: break-word;
}

.toast-close {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-close:hover {
  background: #f1f5f9;
  color: #64748b;
}

.toast-close:focus-visible {
  outline: 2px solid #16a34a;
  outline-offset: 1px;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: currentColor;
  animation: toast-progress linear forwards;
  opacity: 0.3;
}

.toast-success .toast-progress {
  color: #16a34a;
}

.toast-error .toast-progress {
  color: #dc2626;
}

.toast-warning .toast-progress {
  color: #f59e0b;
}

.toast-info .toast-progress {
  color: #0891b2;
}

@keyframes toast-progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

/* Transitions */
.toast-list-enter-active {
  animation: toast-in 0.3s ease-out;
}

.toast-list-leave-active {
  animation: toast-out 0.3s ease-in;
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes toast-out {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}

.toast-dismissing {
  animation: toast-out 0.3s ease-in forwards;
}

/* Responsive */
@media (max-width: 640px) {
  .toast-container {
    max-width: calc(100vw - 32px);
    left: 16px !important;
    right: 16px !important;
  }
}
</style>
