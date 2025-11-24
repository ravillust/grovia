<template>
  <div class="treatment-recommendation">
    <!-- Header -->
    <div class="treatment-header">
      <h2 class="treatment-title">💊 Rekomendasi Perawatan</h2>
      <p class="treatment-subtitle">
        Panduan lengkap untuk mengatasi {{ diseaseName }}
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Memuat rekomendasi perawatan...</p>
    </div>

    <!-- Content -->
    <div v-else-if="treatment" class="treatment-content">
      <!-- Healthy Plant Message -->
      <div v-if="isHealthyPlant" class="healthy-plant-message">
        <div class="success-icon">✅</div>
        <h3>Tanaman Anda Sehat!</h3>
        <p>{{ treatment.treatment[0] || 'Tidak perlu perawatan khusus. Pertahankan kondisi tanaman dengan perawatan rutin.' }}</p>
        <div class="maintenance-tips">
          <h4>Tips Perawatan Rutin:</h4>
          <ul>
            <li>Siram secara teratur sesuai kebutuhan tanaman</li>
            <li>Pastikan mendapat cahaya matahari yang cukup</li>
            <li>Berikan pupuk secara berkala</li>
            <li>Pantau kesehatan tanaman secara rutin</li>
          </ul>
        </div>
      </div>

      <!-- Disease Treatment Sections -->
      <template v-else>
        <!-- Prevention Section -->
        <div v-if="Array.isArray(treatment.prevention) && treatment.prevention.length > 0" class="treatment-section">
          <div class="section-header">
            <span class="section-icon">🛡️</span>
            <h3 class="section-title">Pencegahan</h3>
          </div>
          <ul class="treatment-list">
            <li v-for="(item, index) in treatment.prevention" :key="`prev-${index}`">
              {{ item }}
            </li>
          </ul>
        </div>

        <!-- Treatment Section -->
        <div v-if="Array.isArray(treatment.treatment) && treatment.treatment.length > 0" class="treatment-section">
          <div class="section-header">
            <span class="section-icon">🏥</span>
            <h3 class="section-title">Penanganan Umum</h3>
          </div>
          <ul class="treatment-list">
            <li v-for="(item, index) in treatment.treatment" :key="`treat-${index}`">
              {{ item }}
            </li>
          </ul>
        </div>
      </template>

      <!-- Organic Solutions -->
      <div v-if="Array.isArray(treatment.organicSolutions) && treatment.organicSolutions.length > 0" class="treatment-section organic">
        <div class="section-header">
          <span class="section-icon">🌿</span>
          <h3 class="section-title">Solusi Organik</h3>
        </div>
        <div class="solution-cards">
          <div
            v-for="(solution, index) in treatment.organicSolutions"
            :key="`org-${index}`"
            class="solution-card"
          >
            <div class="solution-number">{{ index + 1 }}</div>
            <p class="solution-text">{{ solution }}</p>
          </div>
        </div>
      </div>

      <!-- Chemical Solutions -->
      <div v-if="treatment.chemicalSolutions && treatment.chemicalSolutions.length > 0" class="treatment-section chemical">
        <div class="section-header">
          <span class="section-icon">⚗️</span>
          <h3 class="section-title">Solusi Kimia</h3>
        </div>
        <div class="warning-box">
          <span class="warning-icon">⚠️</span>
          <p>Gunakan pestisida kimia sesuai dosis yang dianjurkan dan perhatikan masa tunggu panen.</p>
        </div>
        <div class="solution-cards">
          <div
            v-for="(solution, index) in treatment.chemicalSolutions"
            :key="`chem-${index}`"
            class="solution-card"
          >
            <div class="solution-number">{{ index + 1 }}</div>
            <p class="solution-text">{{ solution }}</p>
          </div>
        </div>
      </div>

      <!-- Additional Tips -->
      <div v-if="Array.isArray(treatment.additionalTips) && treatment.additionalTips.length > 0" class="treatment-section tips">
        <div class="section-header">
          <span class="section-icon">💡</span>
          <h3 class="section-title">Tips Tambahan</h3>
        </div>
        <div class="tips-grid">
          <div
            v-for="(tip, index) in treatment.additionalTips"
            :key="`tip-${index}`"
            class="tip-card"
          >
            <span class="tip-icon">✓</span>
            <p>{{ tip }}</p>
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
      <div class="disclaimer">
        <p>
          <strong>Catatan:</strong> Rekomendasi ini bersifat umum. Untuk hasil terbaik,
          konsultasikan dengan ahli pertanian atau penyuluh di daerah Anda.
        </p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <span class="error-icon">❌</span>
      <p>{{ error }}</p>
      <button class="retry-btn" @click="$emit('retry')">
        Coba Lagi
      </button>
    </div>

    <!-- Back Button -->
    <button v-if="!isLoading" class="back-btn" @click="$emit('back')">
      ← Kembali ke Hasil Deteksi
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  treatment: {
    type: Object,
    default: null,
  },
  diseaseName: {
    type: String,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: null,
  },
});

defineEmits(['back', 'retry']);

// Check if plant is healthy - ONLY based on disease name
const isHealthyPlant = computed(() => {
  if (!props.treatment) return false;

  const name = props.diseaseName?.toLowerCase() || '';

  // Only show healthy message if disease name explicitly contains 'sehat' or 'healthy'
  return name.includes('sehat') || name.includes('healthy');
});
</script>

<style scoped>
.treatment-recommendation {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.treatment-header {
  text-align: center;
  margin-bottom: 32px;
}

.treatment-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.treatment-subtitle {
  font-size: 16px;
  color: #718096;
  margin: 0;
}

/* Loading State */
.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Treatment Content */
.treatment-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.treatment-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.treatment-section.organic {
  border-left: 4px solid #48bb78;
}

.treatment-section.chemical {
  border-left: 4px solid #ed8936;
}

.treatment-section.tips {
  border-left: 4px solid #4299e1;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.section-icon {
  font-size: 28px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

/* Healthy Plant Message */
.healthy-plant-message {
  background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(72, 187, 120, 0.2);
}

.success-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.healthy-plant-message h3 {
  font-size: 28px;
  font-weight: 700;
  color: #22543d;
  margin: 0 0 12px 0;
}

.healthy-plant-message > p {
  font-size: 18px;
  color: #276749;
  margin: 0 0 24px 0;
  line-height: 1.6;
}

.maintenance-tips {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  padding: 24px;
  margin-top: 24px;
  text-align: left;
}

.maintenance-tips h4 {
  font-size: 18px;
  font-weight: 600;
  color: #22543d;
  margin: 0 0 16px 0;
  text-align: center;
}

.maintenance-tips ul {
  margin: 0;
  padding-left: 24px;
  list-style: none;
}

.maintenance-tips li {
  position: relative;
  padding-left: 28px;
  margin-bottom: 12px;
  color: #2d3748;
  font-size: 15px;
  line-height: 1.6;
}

.maintenance-tips li:before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #38a169;
  font-weight: bold;
  font-size: 18px;
}

.maintenance-tips li:last-child {
  margin-bottom: 0;
}

.treatment-list {
  margin: 0;
  padding-left: 20px;
}

.treatment-list li {
  margin-bottom: 12px;
  color: #4a5568;
  font-size: 15px;
  line-height: 1.6;
}

.treatment-list li:last-child {
  margin-bottom: 0;
}

/* Solution Cards */
.solution-cards {
  display: grid;
  gap: 16px;
}

.solution-card {
  display: flex;
  gap: 16px;
  padding: 16px;
  background-color: #f7fafc;
  border-radius: 8px;
  transition: transform 0.2s;
}

.solution-card:hover {
  transform: translateX(4px);
}

.solution-number {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #4299e1, #3182ce);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.solution-text {
  flex: 1;
  color: #2d3748;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

/* Warning Box */
.warning-box {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  background-color: #fffbeb;
  border: 1px solid #fbbf24;
  border-radius: 8px;
  margin-bottom: 16px;
}

.warning-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.warning-box p {
  margin: 0;
  color: #78350f;
  font-size: 14px;
  line-height: 1.5;
}

/* Tips Grid */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.tip-card {
  display: flex;
  gap: 12px;
  padding: 14px;
  background-color: #f0f9ff;
  border-radius: 8px;
}

.tip-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  background-color: #4299e1;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.tip-card p {
  flex: 1;
  margin: 0;
  color: #1e40af;
  font-size: 13px;
  line-height: 1.5;
}

/* Disclaimer */
.disclaimer {
  padding: 16px;
  background-color: #edf2f7;
  border-left: 4px solid #a0aec0;
  border-radius: 8px;
  margin-top: 8px;
}

.disclaimer p {
  margin: 0;
  color: #4a5568;
  font-size: 14px;
  line-height: 1.6;
}

/* Error State */
.error-container {
  text-align: center;
  padding: 60px 20px;
}

.error-icon {
  font-size: 64px;
  display: block;
  margin-bottom: 16px;
}

.error-container p {
  color: #e53e3e;
  font-size: 16px;
  margin-bottom: 20px;
}

.retry-btn {
  padding: 12px 24px;
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-btn:hover {
  background-color: #3182ce;
}

/* Back Button */
.back-btn {
  width: 100%;
  padding: 14px 24px;
  margin-top: 24px;
  background: white;
  color: #4a5568;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background-color: #f7fafc;
  border-color: #cbd5e0;
}

@media (max-width: 640px) {
  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>
