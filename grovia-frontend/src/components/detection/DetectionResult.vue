<template>
  <div v-if="result" class="detection-result">
    <!-- Header -->
    <div class="result-header">
      <div class="result-icon" :class="severityClass">
        <span class="severity-dot"></span>
      </div>
      <h2 class="result-title">Hasil Deteksi</h2>
    </div>

    <!-- Disease Information -->
    <div class="disease-info-card">
      <div class="disease-image">
        <img :src="result.imageUrl" alt="Uploaded leaf" />
      </div>

      <div class="disease-details">
        <div class="disease-name-section">
          <h3 class="disease-name">{{ result.diseaseName }}</h3>
          <p class="scientific-name">{{ result.scientificName }}</p>
        </div>

        <!-- Confidence Score -->
        <div class="confidence-section">
          <div class="confidence-label">
            <span>Tingkat Kepercayaan</span>
            <span class="confidence-badge" :class="confidenceClass">
              {{ confidencePercentage }}%
            </span>
          </div>
          <div class="confidence-bar">
            <div
              class="confidence-fill"
              :class="confidenceClass"
              :style="{ width: `${confidencePercentage}%` }"
            ></div>
          </div>
          <p class="confidence-description">
            {{ confidenceDescription }}
          </p>
        </div>

        <!-- Symptoms -->
        <div v-if="result.symptoms && result.symptoms.length > 0" class="symptoms-section">
          <h4 class="section-title">Gejala Umum</h4>
          <ul class="symptoms-list">
            <li v-for="(symptom, index) in result.symptoms" :key="index">
              {{ symptom }}
            </li>
          </ul>
        </div>

        <!-- Description -->
        <div v-if="result.description" class="description-section">
          <h4 class="section-title">Deskripsi</h4>
          <p class="description-text">{{ result.description }}</p>
        </div>
      </div>
    </div>

    <!-- Timestamp -->
    <div class="detection-timestamp">
      <span class="timestamp-icon"><Clock :size="16" :stroke-width="1.6" /></span>
      <span>Dideteksi pada: {{ formattedTimestamp }}</span>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <button class="btn-secondary" @click="$emit('new-detection')">
        <RefreshCw :size="16" :stroke-width="1.6" style="margin-right:8px; vertical-align:middle;" /> Deteksi Baru
      </button>
      <button class="btn-primary" @click="$emit('view-treatment')">
        <Pill :size="16" :stroke-width="1.6" style="margin-right:8px; vertical-align:middle;" /> Lihat Rekomendasi Perawatan
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { RefreshCw, Pill, Clock } from 'lucide-vue-next';

const props = defineProps({
  result: {
    type: Object,
    required: true,
  },
});

defineEmits(['new-detection', 'view-treatment']);

// Computed properties
const confidencePercentage = computed(() => {
  const confidence = props.result?.confidence;
  if (typeof confidence !== 'number' || isNaN(confidence)) {
    return '0';
  }
  return Math.round(confidence * 100);
});

const confidenceClass = computed(() => {
  const confidence = props.result?.confidence;
  if (typeof confidence !== 'number' || isNaN(confidence)) {
    return 'low';
  }
  if (confidence >= 0.8) return 'high';
  if (confidence >= 0.6) return 'medium';
  return 'low';
});

const confidenceDescription = computed(() => {
  const confidence = props.result?.confidence;
  if (typeof confidence !== 'number' || isNaN(confidence)) {
    return 'Data confidence tidak tersedia. Silakan coba deteksi ulang.';
  }
  if (confidence >= 0.8) {
    return 'Deteksi sangat akurat. Hasil dapat dipercaya.';
  }
  if (confidence >= 0.6) {
    return 'Deteksi cukup akurat. Disarankan melakukan verifikasi tambahan.';
  }
  return 'Tingkat kepercayaan rendah. Sebaiknya konsultasi dengan ahli.';
});

const severityClass = computed(() => {
  const confidence = props.result?.confidence;
  if (typeof confidence !== 'number' || isNaN(confidence)) {
    return 'severity-low';
  }
  if (confidence >= 0.8) return 'severity-high';
  if (confidence >= 0.6) return 'severity-medium';
  return 'severity-low';
});

// We render a visual severity dot inside .result-icon; no emoji used.

const formattedTimestamp = computed(() => {
  const date = new Date(props.result.timestamp);
  return date.toLocaleString('id-ID', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
});
</script>

<style scoped>
.detection-result {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.result-icon {
  font-size: 48px;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-icon .severity-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: inline-block;
}

.result-icon.severity-high .severity-dot {
  background: #fc8181;
}

.result-icon.severity-medium .severity-dot {
  background: #fbbf24;
}

.result-icon.severity-low .severity-dot {
  background: #68d391;
}

.result-icon.severity-high {
  background-color: #fff5f5;
  border: 2px solid #fc8181;
}

.result-icon.severity-medium {
  background-color: #fffbeb;
  border: 2px solid #fbbf24;
}

.result-icon.severity-low {
  background-color: #f0fff4;
  border: 2px solid #68d391;
}

.result-title {
  font-size: 28px;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
}

.disease-info-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 20px;
}

.disease-image {
  width: 100%;
  height: 300px;
  overflow: hidden;
  background-color: #f7fafc;
}

.disease-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.disease-details {
  padding: 24px;
}

.disease-name-section {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e2e8f0;
}

.disease-name {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.scientific-name {
  font-size: 16px;
  font-style: italic;
  color: #718096;
  margin: 0;
}

.confidence-section {
  margin-bottom: 24px;
}

.confidence-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #4a5568;
}

.confidence-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
}

.confidence-badge.high {
  background-color: #c6f6d5;
  color: #22543d;
}

.confidence-badge.medium {
  background-color: #fef3c7;
  color: #78350f;
}

.confidence-badge.low {
  background-color: #fed7d7;
  color: #742a2a;
}

.confidence-bar {
  width: 100%;
  height: 12px;
  background-color: #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}

.confidence-fill {
  height: 100%;
  transition: width 1s ease-out;
  border-radius: 6px;
}

.confidence-fill.high {
  background: linear-gradient(90deg, #48bb78, #38a169);
}

.confidence-fill.medium {
  background: linear-gradient(90deg, #ecc94b, #d69e2e);
}

.confidence-fill.low {
  background: linear-gradient(90deg, #fc8181, #f56565);
}

.confidence-description {
  font-size: 13px;
  color: #718096;
  margin: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 12px 0;
}

.symptoms-section {
  margin-bottom: 24px;
}

.symptoms-list {
  margin: 0;
  padding-left: 20px;
}

.symptoms-list li {
  margin-bottom: 8px;
  color: #4a5568;
  font-size: 14px;
  line-height: 1.6;
}

.description-section {
  margin-bottom: 0;
}

.description-text {
  color: #4a5568;
  font-size: 14px;
  line-height: 1.8;
  margin: 0;
}

.detection-timestamp {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background-color: #edf2f7;
  border-radius: 8px;
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 24px;
}

.timestamp-icon {
  font-size: 16px;
}

.timestamp-icon svg {
  display: inline-block;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-buttons button {
  flex: 1;
  min-width: 200px;
  padding: 14px 24px;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #48bb78, #38a169);
  color: white;
  box-shadow: 0 4px 6px rgba(72, 187, 120, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(72, 187, 120, 0.4);
}

.btn-secondary {
  background: white;
  color: #4a5568;
  border: 2px solid #e2e8f0;
}

.btn-secondary:hover {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

@media (max-width: 640px) {
  .action-buttons {
    flex-direction: column;
  }

  .action-buttons button {
    min-width: 100%;
  }

  .disease-image {
    height: 200px;
  }
}
</style>
