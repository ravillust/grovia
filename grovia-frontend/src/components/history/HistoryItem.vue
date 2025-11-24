<template>
  <div class="history-item">
    <!-- Image Thumbnail -->
    <div class="item-image">
      <img
        :src="imageUrl"
        :alt="item.disease_name"
        @error="handleImageError"
      />
    </div>

    <!-- Content -->
    <div class="item-content">
      <div class="content-main">
        <h3 class="disease-name">{{ item.disease_name }}</h3>
        <div class="item-meta">
          <div class="confidence-badge" :class="confidenceClass">
            <span class="badge-text">{{ confidencePercentage }}%</span>
          </div>
          <div class="item-date">
            <Clock :size="14" :stroke-width="1.6" />
            <span>{{ formattedDate }}</span>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="item-actions">
        <button @click="handleView" class="btn-view" title="Lihat Detail">
          <Eye :size="18" :stroke-width="1.6" />
        </button>
        <button @click="handleDelete" class="btn-delete" title="Hapus">
          <Trash2 :size="18" :stroke-width="1.6" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { Eye, Trash2, Clock } from 'lucide-vue-next';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['view', 'delete']);

// State
const imageLoadError = ref(false);
const fallbackImage = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"%3E%3Crect fill="%23e2e8f0" width="200" height="200"/%3E%3Ctext x="50%25" y="50%25" font-family="Arial" font-size="16" fill="%23718096" text-anchor="middle" dy=".3em"%3EGambar tidak tersedia%3C/text%3E%3C/svg%3E';

// Computed
const imageUrl = computed(() => {
  if (imageLoadError.value) {
    return fallbackImage;
  }
  return props.item.image_url || fallbackImage;
});

const confidencePercentage = computed(() => {
  return (props.item.confidence * 100).toFixed(1);
});

const confidenceClass = computed(() => {
  const confidence = props.item.confidence;
  if (confidence >= 0.8) return 'high';
  if (confidence >= 0.6) return 'medium';
  return 'low';
});

const confidenceIcon = computed(() => {
  const confidence = props.item.confidence;
  if (confidence >= 0.8) return '✓';
  if (confidence >= 0.6) return '!';
  return '?';
});

const formattedDate = computed(() => {
  const date = new Date(props.item.detected_at);
  const now = new Date();
  const diffInMs = now - date;
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60));
  const diffInDays = Math.floor(diffInHours / 24);

  if (diffInHours < 1) {
    const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
    return `${diffInMinutes} menit yang lalu`;
  } else if (diffInHours < 24) {
    return `${diffInHours} jam yang lalu`;
  } else if (diffInDays < 7) {
    return `${diffInDays} hari yang lalu`;
  } else {
    return date.toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  }
});

// Methods
function handleImageError() {
  imageLoadError.value = true;
}

function handleView() {
  emit('view', props.item);
}

function handleDelete() {
  emit('delete', props.item);
}
</script>

<style scoped>
.history-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px;
}

.history-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #6aa581;
}

/* Image Thumbnail */
.item-image {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  background: #f8faf9;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Content */
.item-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  min-width: 0;
}

.content-main {
  flex: 1;
  min-width: 0;
}

.disease-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a3a2e;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  letter-spacing: -0.01em;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Confidence Badge */
.confidence-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.confidence-badge.high {
  background: rgba(106, 165, 129, 0.15);
  color: #2d5f4a;
}

.confidence-badge.medium {
  background: rgba(251, 191, 36, 0.15);
  color: #92400e;
}

.confidence-badge.low {
  background: rgba(239, 68, 68, 0.15);
  color: #991b1b;
}

/* Date */
.item-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.6);
}

.item-date svg {
  display: block;
}

/* Actions */
.item-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.btn-view,
.btn-delete {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-view {
  background: #6aa581;
  color: white;
}

.btn-view:hover {
  background: #5a9470;
  transform: translateY(-2px);
}

.btn-view svg {
  display: block;
}

.btn-delete {
  background: white;
  border: 2px solid #e5e7eb;
  color: rgba(0, 0, 0, 0.6);
}

.btn-delete:hover {
  border-color: #dc2626;
  background: #fef2f2;
  color: #dc2626;
}

.btn-delete svg {
  display: block;
}

/* Responsive */
@media (max-width: 640px) {
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    padding: 16px;
  }

  .item-image {
    width: 100%;
    height: 160px;
  }

  .item-content {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .disease-name {
    white-space: normal;
  }

  .item-meta {
    flex-wrap: wrap;
  }

  .item-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
