<template>
  <div class="detection-view">
    <div class="container">
      <!-- Page Title -->
      <div class="page-header">
        <h1 class="page-title">Unggah gambar untuk mendeteksi penyakit tanaman</h1>
      </div>

      <!-- Main Content -->
      <div class="detection-content">
        <!-- Step 1: Upload Image -->
        <div v-if="currentStep === 'upload'" class="step-container">
          <ImageUpload
            @detection-complete="handleDetectionComplete"
            @detection-error="handleDetectionError"
          />
        </div>

        <!-- Step 2: Detection Result -->
        <div v-else-if="currentStep === 'result'" class="step-container">
          <DetectionResult
            :result="detectionStore.detectionResult"
            @new-detection="handleNewDetection"
            @view-treatment="handleViewTreatment"
          />
        </div>

        <!-- Step 3: Treatment Recommendation -->
        <div v-else-if="currentStep === 'treatment'" class="step-container">
          <TreatmentRecommendation
            :treatment="detectionStore.treatmentRecommendation"
            :disease-name="detectionStore.detectionResult?.diseaseName || ''"
            :is-loading="detectionStore.isFetchingTreatment"
            :error="treatmentError"
            @back="currentStep = 'result'"
            @retry="retryFetchTreatment"
          />
        </div>
      </div>

      <!-- Processing Overlay -->
      <div v-if="detectionStore.isProcessing" class="processing-overlay">
        <div class="processing-content">
          <div class="processing-spinner"></div>
          <h3 class="processing-title">Menganalisis Gambar...</h3>
          <p class="processing-text">
            AI kami sedang mendeteksi penyakit pada tanaman Anda.
            <br />Proses ini memakan waktu beberapa detik.
          </p>
          <div class="processing-progress">
            <div class="progress-bar-container">
              <div
                class="progress-bar-fill"
                :style="{ width: `${processingProgress}%` }"
              ></div>
            </div>
            <p class="progress-text">{{ Math.round(processingProgress) }}%</p>
          </div>
        </div>
      </div>

      <!-- Info Cards (only show on upload step) -->
      <div v-if="false" class="info-section">
        <h3 class="info-title">Tips untuk Hasil Terbaik</h3>
        <div class="info-cards">
          <div class="info-card">
            <div class="info-icon"><Camera :size="40" :stroke-width="1.8" /></div>
            <h4>Pencahayaan Baik</h4>
            <p>Pastikan foto diambil dengan pencahayaan yang cukup dan tidak blur</p>
          </div>
          <div class="info-card">
            <div class="info-icon"><Leaf :size="40" :stroke-width="1.8" /></div>
            <h4>Fokus pada Daun</h4>
            <p>Ambil foto close-up dari daun yang menunjukkan gejala penyakit dengan jelas</p>
          </div>
          <div class="info-card">
            <div class="info-icon"><Ruler :size="40" :stroke-width="1.8" /></div>
            <h4>Resolusi Cukup</h4>
            <p>Gunakan gambar minimal 224x224 piksel untuk hasil deteksi optimal</p>
          </div>
          <div class="info-card">
            <div class="info-icon"><Target :size="40" :stroke-width="1.8" /></div>
            <h4>Satu Daun per Foto</h4>
            <p>Untuk akurasi terbaik, fokus pada satu daun dalam setiap foto</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useDetectionStore } from '@/stores/detection';
import ImageUpload from '@/components/detection/ImageUpload.vue';
import DetectionResult from '@/components/detection/DetectionResult.vue';
import TreatmentRecommendation from '@/components/detection/TreatmentRecommendation.vue';
import { Camera, Leaf, Ruler, Target } from 'lucide-vue-next';
import { onUnmounted } from 'vue';

const detectionStore = useDetectionStore();

// State
const currentStep = ref('upload'); // 'upload' | 'result' | 'treatment'
const treatmentError = ref(null);
const processingProgress = ref(0);

// Simulate processing progress for better UX
watch(() => detectionStore.isProcessing, (isProcessing) => {
  if (isProcessing) {
    processingProgress.value = 0;
    const interval = setInterval(() => {
      if (processingProgress.value < 90) {
        processingProgress.value += Math.random() * 15;
      }
    }, 500);

    // Clear interval when processing is done
    const stopWatch = watch(() => detectionStore.isProcessing, (stillProcessing) => {
      if (!stillProcessing) {
        clearInterval(interval);
        processingProgress.value = 100;
        stopWatch();

        // Small delay before showing result
        setTimeout(() => {
          processingProgress.value = 0;
        }, 500);
      }
    });
  }
});

/**
 * Handle successful detection
 */
function handleDetectionComplete() {
  currentStep.value = 'result';
  treatmentError.value = null;
}

/**
 * Handle detection error
 */
function handleDetectionError(error) {
  console.error('Detection failed:', error);
  // Error sudah ditampilkan di ImageUpload component
}

/**
 * Handle new detection request
 */
function handleNewDetection() {
  detectionStore.resetDetection();
  currentStep.value = 'upload';
  treatmentError.value = null;
}

/**
 * Handle view treatment
 */
function handleViewTreatment() {
  currentStep.value = 'treatment';

  // Fetch treatment if not already loaded
  if (!detectionStore.treatmentRecommendation && detectionStore.detectionResult) {
    retryFetchTreatment();
  }
}

/**
 * Retry fetching treatment recommendation
 */
async function retryFetchTreatment() {
  if (!detectionStore.detectionResult) return;

  treatmentError.value = null;

  try {
    await detectionStore.fetchTreatmentRecommendation(
      detectionStore.detectionResult.diseaseId
    );
  } catch (error) {
  // Gunakan error.message atau error.response.data untuk pesan yang lebih informatif
  console.error("Fetch Treatment Failed:", error);
  treatmentError.value = error.message || 'Gagal memuat rekomendasi perawatan. Silakan coba lagi.';
}
onUnmounted(() => {
  detectionStore.resetDetection();
});
}
</script>

<style scoped>
.detection-view {
  min-height: 100vh;
  background: #ffffff;
  padding: 140px 40px 80px;
  position: relative;
}

.detection-view::before {
  display: none;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* Page Header - Clean */
.page-header {
  text-align: center;
  margin-bottom: 60px;
}

.page-title {
  font-size: 42px;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
  letter-spacing: -0.02em;
  line-height: 1.3;
  max-width: 700px;
  margin: 0 auto;
}

.page-description {
  display: none;
}

/* Detection Content - Minimal Shadow */
.detection-content {
  background: transparent;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
  margin-bottom: 60px;
  border: none;
  max-width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.step-container {
  animation: fadeIn 0.4s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Processing Overlay - Modern */
.processing-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(26, 58, 46, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(12px);
}

.processing-content {
  text-align: center;
  padding: 56px 48px;
  background: white;
  border-radius: 24px;
  max-width: 460px;
  width: 90%;
  border: 1px solid #e5e7eb;
}

.processing-spinner {
  width: 64px;
  height: 64px;
  border: 4px solid #f3f4f6;
  border-top-color: #6aa581;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 28px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.processing-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a3a2e;
  margin: 0 0 12px 0;
  letter-spacing: -0.015em;
}

.processing-text {
  font-size: 16px;
  color: rgba(0, 0, 0, 0.6);
  line-height: 1.7;
  margin: 0 0 28px 0;
}

.processing-progress {
  margin-top: 24px;
}

.progress-bar-container {
  width: 100%;
  height: 8px;
  background-color: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-bar-fill {
  height: 100%;
  background: #6aa581;
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-text {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.6);
  font-weight: 600;
  margin: 0;
}

/* Info Section - Clean Cards */
.info-section {
  margin-top: 80px;
  padding-top: 60px;
  border-top: 1px solid #e5e7eb;
}

.info-title {
  text-align: center;
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 40px 0;
  letter-spacing: -0.01em;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}

.info-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 28px 24px;
  text-align: center;
  border: 1px solid #f3f4f6;
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border-color: #e5e7eb;
}

.info-icon {
  font-size: 40px;
  margin-bottom: 16px;
  display: block;
}

.info-icon svg {
  display: block;
  margin: 0 auto 12px;
  width: 36px;
  height: 36px;
  color: #6aa581;
}

.info-card h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
  letter-spacing: -0.01em;
}

.info-card p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .detection-view {
    padding: 32px 20px;
  }

  .page-title {
    font-size: 36px;
  }

  .page-description {
    font-size: 17px;
  }

  .detection-content {
    padding: 40px 28px;
    border-radius: 20px;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .processing-content {
    padding: 40px 32px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 32px;
  }

  .detection-content {
    padding: 32px 24px;
  }
}
</style>
