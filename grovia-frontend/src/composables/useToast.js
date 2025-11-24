import { ref } from 'vue';

// Global toast instance
const toastInstance = ref(null);

export function useToast() {
  /**
   * Set toast instance (called from App.vue)
   */
  function setToastInstance(instance) {
    toastInstance.value = instance;
  }

  /**
   * Show success toast
   */
  function success(message, title = 'Berhasil') {
    if (toastInstance.value) {
      return toastInstance.value.success(message, title);
    }
    console.warn('Toast instance not initialized');
  }

  /**
   * Show error toast
   */
  function error(message, title = 'Error') {
    if (toastInstance.value) {
      return toastInstance.value.error(message, title);
    }
    console.warn('Toast instance not initialized');
  }

  /**
   * Show warning toast
   */
  function warning(message, title = 'Peringatan') {
    if (toastInstance.value) {
      return toastInstance.value.warning(message, title);
    }
    console.warn('Toast instance not initialized');
  }

  /**
   * Show info toast
   */
  function info(message, title = 'Info') {
    if (toastInstance.value) {
      return toastInstance.value.info(message, title);
    }
    console.warn('Toast instance not initialized');
  }

  /**
   * Show custom toast
   */
  function show({ type = 'info', title, message, duration = 5000 }) {
    if (toastInstance.value) {
      return toastInstance.value.showToast({ type, title, message, duration });
    }
    console.warn('Toast instance not initialized');
  }

  /**
   * Remove specific toast
   */
  function remove(id) {
    if (toastInstance.value) {
      toastInstance.value.removeToast(id);
    }
  }

  /**
   * Clear all toasts
   */
  function clearAll() {
    if (toastInstance.value) {
      toastInstance.value.clearAll();
    }
  }

  return {
    setToastInstance,
    success,
    error,
    warning,
    info,
    show,
    remove,
    clearAll,
  };
}
