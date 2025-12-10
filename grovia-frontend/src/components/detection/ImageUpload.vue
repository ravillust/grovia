<template>
  <div class="image-upload-container">
    <!-- Upload Area -->
    <div
      class="upload-zone"
      :class="{ 'drag-over': isDragging, 'has-image': previewUrl }"
      @drop.prevent="handleDrop"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @click="triggerFileInput"
      role="button"
      tabindex="0"
      :aria-label="previewUrl ? 'Klik untuk mengganti gambar' : 'Klik atau drag gambar ke sini'"
      @keydown.enter="triggerFileInput"
      @keydown.space.prevent="triggerFileInput"
    >
      <!-- Preview Image -->
      <div v-if="previewUrl" class="image-preview">
        <img :src="previewUrl" alt="Preview" />
        <button
          class="remove-image-btn"
          @click.stop="removeImage"
          aria-label="Hapus gambar"
        >
          <X :size="20" />
        </button>
      </div>

      <!-- Upload Prompt -->
      <div v-else class="upload-prompt">
        <div class="upload-icon">
          <Camera :size="48" :stroke-width="1.5" />
        </div>
        <p class="upload-title">
          {{ isDragging ? 'Lepaskan file di sini' : 'Unggah Foto Daun' }}
        </p>
        <p class="upload-subtitle">
          Klik atau drag & drop gambar daun di sini
        </p>
        <p class="upload-info">
          Format: JPG, PNG, WebP • Maksimal 5MB
        </p>
      </div>

      <!-- Hidden File Input -->
      <input
        ref="fileInput"
        type="file"
        accept="image/jpeg,image/jpg,image/png,image/webp"
        @change="handleFileSelect"
        style="display: none"
      />
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      <span class="error-icon">
        <AlertCircle :size="18" />
      </span>
      {{ errorMessage }}
    </div>

    <!-- File Info -->
    <div v-if="selectedFile && !errorMessage" class="file-info">
      <span class="file-name">{{ selectedFile.name }}</span>
      <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
    </div>

    <!-- Upload Progress -->
    <div v-if="isUploading" class="upload-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: `${uploadProgress}%` }"></div>
      </div>
      <p class="progress-text">Mengunggah... {{ Math.round(uploadProgress) }}%</p>
    </div>

    <!-- Detect Button -->
    <button
      v-if="selectedFile && !errorMessage && !isUploading"
      class="detect-btn"
      @click="handleDetect"
      :disabled="isProcessing"
    >
      {{ isProcessing ? 'Mendeteksi...' : 'Deteksi Penyakit' }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useDetectionStore } from '@/stores/detection';
import { validateImageFile, validateImageDimensions, formatFileSize } from '@/utils/validators';
import { Camera, X, AlertCircle } from 'lucide-vue-next';

const detectionStore = useDetectionStore();

// Refs
const fileInput = ref(null);
const selectedFile = ref(null);
const previewUrl = ref(null);
const isDragging = ref(false);
const errorMessage = ref(null);

// Computed
const isUploading = computed(() => detectionStore.isUploading);
const uploadProgress = computed(() => detectionStore.uploadProgress);
const isProcessing = computed(() => detectionStore.isProcessing);

// Emit untuk parent component
const emit = defineEmits(['detection-complete', 'detection-error']);

/**
 * Trigger file input click
 */
function triggerFileInput() {
  if (!isProcessing.value && fileInput.value) {
    fileInput.value.click();
  }
}

/**
 * Handle file selection dari input
 */
async function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    await processFile(file);
  }
}

/**
 * Handle drag & drop
 */
async function handleDrop(event) {
  isDragging.value = false;

  const file = event.dataTransfer.files[0];
  if (file) {
    await processFile(file);
  }
}

/**
 * Process dan validasi file
 */
async function processFile(file) {
  errorMessage.value = null;

  // Validasi tipe dan ukuran file
  const validation = validateImageFile(file);
  if (!validation.valid) {
    errorMessage.value = validation.error;
    return;
  }

  // Validasi dimensi gambar
  const dimensionValidation = await validateImageDimensions(file);
  if (!dimensionValidation.valid) {
    errorMessage.value = dimensionValidation.error;
    return;
  }

  // Quick client-side heuristic: check green area percentage to avoid uploading
  // obvious non-leaf images. This is lightweight and runs in browser using canvas.
  try {
    const greenCheck = await checkImageGreenPercentage(file);
    // If green percentage is very low, reject early (friendly message)
    if (greenCheck < 12) {
      errorMessage.value = 'Gambar ini tampaknya bukan daun atau memiliki terlalu sedikit area hijau. Pastikan foto close-up daun.';
      return;
    }
  } catch (e) {
    // If anything fails, fallback to normal flow and let backend validate
    console.warn('Client-side green check failed, continuing upload', e);
  }

  // Set file dan preview
  selectedFile.value = file;

  // Cleanup previous preview
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }

  previewUrl.value = URL.createObjectURL(file);
}

/**
 * Remove selected image
 */
function removeImage() {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }

  selectedFile.value = null;
  previewUrl.value = null;
  errorMessage.value = null;

  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

/**
 * Handle detection
 */
async function handleDetect() {
  if (!selectedFile.value || isProcessing.value) return;

  errorMessage.value = null;

  try {
    const result = await detectionStore.detectDisease(selectedFile.value);
    emit('detection-complete', result);
  } catch (error) {
    errorMessage.value = detectionStore.detectionError || 'Gagal mendeteksi penyakit';
    emit('detection-error', error);
  }
}

// Cleanup on unmount
import { onUnmounted } from 'vue';
onUnmounted(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
  }
});

/**
 * Quick client-side green pixel percentage check.
 * Draws the image to an offscreen canvas, samples pixels and
 * computes approximate percentage of 'green' pixels.
 * This is only a heuristic to avoid unnecessary uploads; backend
 * will still perform the authoritative OpenCV validation.
 *
 * @param {File} file
 * @returns {Promise<number>} green percentage (0-100)
 */
function checkImageGreenPercentage(file) {
  return new Promise((resolve, reject) => {
    try {
      const img = new Image();
      img.onload = () => {
        try {
          // Resize for performance: sample max 300x300
          const maxSample = 300;
          let w = img.width;
          let h = img.height;
          const scale = Math.min(1, maxSample / Math.max(w, h));
          w = Math.max(1, Math.round(w * scale));
          h = Math.max(1, Math.round(h * scale));

          const canvas = document.createElement('canvas');
          canvas.width = w;
          canvas.height = h;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, w, h);

          // Sample pixel data
          const imgData = ctx.getImageData(0, 0, w, h);
          const data = imgData.data;
          let greenCount = 0;
          const total = w * h;

          // Sample step to speed up, e.g., check every 2nd pixel
          const step = 2;
          for (let i = 0; i < data.length; i += 4 * step) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];

            // Simple heuristic for 'green-ish' pixel
            if (isGreenPixel(r, g, b)) greenCount++;
          }

          const sampled = Math.ceil(total / step);
          const percent = (greenCount / sampled) * 100;
          resolve(percent);
        } catch (err) {
          reject(err);
        }
      };

      img.onerror = (e) => reject(e);
      img.src = URL.createObjectURL(file);
    } catch (err) {
      reject(err);
    }
  });
}

/**
 * Basic green pixel test. Tuned to be permissive for leaves under various lighting.
 */
function isGreenPixel(r, g, b) {
  // Check that green is dominant and reasonably saturated
  // g significantly greater than r and b, and g above threshold
  return g > 80 && g > r + 15 && g > b + 15 && (g / Math.max(r + 1, b + 1)) > 1.15;
}
</script>

<style scoped>
.image-upload-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.upload-zone {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 64px 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: transparent;
  position: relative;
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone:hover {
  border-color: #6aa581;
  background-color: transparent;
  transform: none;
  box-shadow: none;
}

.upload-zone:focus-visible {
  outline: 2px solid #6aa581;
  outline-offset: 2px;
  border-color: #6aa581;
}

.upload-zone.drag-over {
  border-color: #6aa581;
  background-color: rgba(106, 165, 129, 0.05);
  transform: none;
}

.upload-zone.has-image {
  padding: 0;
  border: 2px solid #e5e7eb;
  min-height: auto;
  background-color: transparent;
}

.upload-zone.has-image:hover {
  border-color: #d1d5db;
  transform: none;
}

.image-preview {
  position: relative;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #f9fafb;
}

.image-preview img {
  width: 100%;
  height: auto;
  display: block;
  max-height: 480px;
  object-fit: contain;
}

.remove-image-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  backdrop-filter: blur(4px);
}

.remove-image-btn:hover {
  background: rgba(0, 0, 0, 0.85);
  transform: scale(1.1);
}

.remove-image-btn:focus-visible {
  outline: 2px solid white;
  outline-offset: 2px;
}

.upload-prompt {
  width: 100%;
}

.upload-icon {
  color: #6aa581;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.upload-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
  letter-spacing: -0.01em;
}

.upload-subtitle {
  font-size: 15px;
  color: #6b7280;
  margin-bottom: 12px;
  line-height: 1.6;
}

.upload-info {
  font-size: 13px;
  color: #9ca3af;
  font-weight: 400;
}

.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: #fff5f5;
  border: 1px solid #feb2b2;
  border-radius: 8px;
  color: #c53030;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.error-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.file-info {
  margin-top: 16px;
  padding: 12px 16px;
  background-color: #f0fff4;
  border: 1px solid #9ae6b4;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.file-name {
  color: #2f855a;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  margin-right: 12px;
}

.file-size {
  color: #68d391;
  font-size: 12px;
  white-space: nowrap;
}

.upload-progress {
  margin-top: 16px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4299e1, #48bb78);
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 14px;
  color: #4a5568;
  text-align: center;
}

.detect-btn {
  width: 100%;
  margin-top: 24px;
  padding: 15px 28px;
  background: #16a34a;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  letter-spacing: -0.01em;
}

.detect-btn:hover:not(:disabled) {
  background: #15803d;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.detect-btn:focus-visible {
  outline: 3px solid rgba(22, 163, 74, 0.4);
  outline-offset: 2px;
}

.detect-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.detect-btn:active:not(:disabled) {
  transform: translateY(0);
}
</style>
