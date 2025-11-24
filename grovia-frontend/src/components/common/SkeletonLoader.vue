<template>
  <div class="skeleton-loader" :class="[variantClass, { animated: animated }]">
    <div v-if="variant === 'text'" class="skeleton-text" :style="textStyle"></div>
    <div v-else-if="variant === 'circle'" class="skeleton-circle" :style="circleStyle"></div>
    <div v-else-if="variant === 'rectangle'" class="skeleton-rectangle" :style="rectangleStyle"></div>
    <div v-else-if="variant === 'card'" class="skeleton-card">
      <div class="skeleton-card-image"></div>
      <div class="skeleton-card-content">
        <div class="skeleton-text" style="width: 70%; height: 20px; margin-bottom: 12px;"></div>
        <div class="skeleton-text" style="width: 100%; height: 14px; margin-bottom: 8px;"></div>
        <div class="skeleton-text" style="width: 85%; height: 14px;"></div>
      </div>
    </div>
    <div v-else-if="variant === 'avatar'" class="skeleton-avatar" :style="avatarStyle"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // Variant type: 'text' | 'circle' | 'rectangle' | 'card' | 'avatar'
  variant: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'circle', 'rectangle', 'card', 'avatar'].includes(value),
  },

  // Width for rectangle/text
  width: {
    type: [String, Number],
    default: '100%',
  },

  // Height for rectangle/text
  height: {
    type: [String, Number],
    default: '20px',
  },

  // Size for circle/avatar
  size: {
    type: [String, Number],
    default: '40px',
  },

  // Enable shimmer animation
  animated: {
    type: Boolean,
    default: true,
  },

  // Custom border radius
  borderRadius: {
    type: [String, Number],
    default: null,
  },
});

const variantClass = computed(() => `skeleton-${props.variant}`);

const textStyle = computed(() => ({
  width: typeof props.width === 'number' ? `${props.width}px` : props.width,
  height: typeof props.height === 'number' ? `${props.height}px` : props.height,
  borderRadius: props.borderRadius ? (typeof props.borderRadius === 'number' ? `${props.borderRadius}px` : props.borderRadius) : '4px',
}));

const rectangleStyle = computed(() => ({
  width: typeof props.width === 'number' ? `${props.width}px` : props.width,
  height: typeof props.height === 'number' ? `${props.height}px` : props.height,
  borderRadius: props.borderRadius ? (typeof props.borderRadius === 'number' ? `${props.borderRadius}px` : props.borderRadius) : '8px',
}));

const circleStyle = computed(() => ({
  width: typeof props.size === 'number' ? `${props.size}px` : props.size,
  height: typeof props.size === 'number' ? `${props.size}px` : props.size,
}));

const avatarStyle = computed(() => ({
  width: typeof props.size === 'number' ? `${props.size}px` : props.size,
  height: typeof props.size === 'number' ? `${props.size}px` : props.size,
}));
</script>

<style scoped>
.skeleton-loader {
  display: inline-block;
}

/* Base skeleton styles */
.skeleton-text,
.skeleton-rectangle,
.skeleton-circle,
.skeleton-avatar {
  background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 50%, #f1f5f9 100%);
  background-size: 200% 100%;
  display: block;
}

.skeleton-text {
  width: 100%;
  height: 20px;
  border-radius: 4px;
}

.skeleton-rectangle {
  width: 100%;
  height: 100px;
  border-radius: 8px;
}

.skeleton-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.skeleton-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

/* Card skeleton */
.skeleton-card {
  background: white;
  border: 1px solid #f1f5f9;
  border-radius: 16px;
  overflow: hidden;
  width: 100%;
}

.skeleton-card-image {
  width: 100%;
  height: 200px;
  background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 50%, #f1f5f9 100%);
  background-size: 200% 100%;
}

.skeleton-card-content {
  padding: 20px;
}

/* Shimmer animation */
.skeleton-loader.animated .skeleton-text,
.skeleton-loader.animated .skeleton-rectangle,
.skeleton-loader.animated .skeleton-circle,
.skeleton-loader.animated .skeleton-avatar,
.skeleton-loader.animated .skeleton-card-image {
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

/* Accessibility */
.skeleton-loader {
  pointer-events: none;
  user-select: none;
}

/* Performance optimization */
.skeleton-text,
.skeleton-rectangle,
.skeleton-circle,
.skeleton-avatar,
.skeleton-card-image {
  will-change: background-position;
}
</style>
