<template>
  <div class="loading-spinner" :class="[sizeClass, { fullscreen: fullscreen }]">
    <div class="spinner-wrapper">
      <!-- Spinner Animation -->
      <div class="spinner" :class="variantClass">
        <div class="spinner-circle"></div>
      </div>

      <!-- Loading Text -->
      <p v-if="text" class="loading-text">{{ text }}</p>

      <!-- Progress Bar (optional) -->
      <div v-if="showProgress && progress !== null" class="progress-container">
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <span class="progress-percentage">{{ progress }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // Loading text to display
  text: {
    type: String,
    default: '',
  },

  // Spinner size: 'small' | 'medium' | 'large'
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value),
  },

  // Spinner variant: 'primary' | 'secondary' | 'white'
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'white'].includes(value),
  },

  // Show as fullscreen overlay
  fullscreen: {
    type: Boolean,
    default: false,
  },

  // Show progress bar
  showProgress: {
    type: Boolean,
    default: false,
  },

  // Progress value (0-100)
  progress: {
    type: Number,
    default: null,
    validator: (value) => value === null || (value >= 0 && value <= 100),
  },
});

const sizeClass = computed(() => `size-${props.size}`);
const variantClass = computed(() => `variant-${props.variant}`);
</script>

<style scoped>
.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.loading-spinner.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  z-index: 9999;
  padding: 0;
}

.spinner-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.loading-spinner.fullscreen .spinner-wrapper {
  background: white;
  padding: 40px;
  border-radius: 20px;
  min-width: 280px;
}

/* Spinner Animation */
.spinner {
  position: relative;
  animation: spin 1.2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinner-circle {
  border-radius: 50%;
  border-style: solid;
}

/* Size Variants */
.size-small .spinner-circle {
  width: 24px;
  height: 24px;
  border-width: 3px;
}

.size-medium .spinner-circle {
  width: 48px;
  height: 48px;
  border-width: 4px;
}

.size-large .spinner-circle {
  width: 64px;
  height: 64px;
  border-width: 5px;
}

/* Variant Colors */
.variant-primary .spinner-circle {
  border-color: #f1f5f9;
  border-top-color: #16a34a;
}

.variant-secondary .spinner-circle {
  border-color: #f1f5f9;
  border-top-color: #0891b2;
}

.variant-white .spinner-circle {
  border-color: rgba(255, 255, 255, 0.2);
  border-top-color: white;
}

/* Loading Text */
.loading-text {
  font-size: 15px;
  font-weight: 500;
  color: #0f172a;
  margin: 0;
}

.loading-spinner.fullscreen .loading-text {
  color: #0f172a;
}

/* Progress Container */
.progress-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #16a34a, #22c55e);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-percentage {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  text-align: center;
}

/* Animation Performance */
.spinner {
  will-change: transform;
}

.progress-fill {
  will-change: width;
}
</style>
