<template>
  <div class="history-detail-view">
    <div class="detail-container">
      <!-- Back Button -->
      <button @click="$router.back()" class="btn-back">
        ← Kembali ke Riwayat
      </button>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-container">
        <div class="spinner"></div>
        <p>Memuat detail...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-card">
        <h2>❌ Gagal memuat data</h2>
        <p>{{ error }}</p>
        <button @click="fetchDetail" class="btn-retry">Coba Lagi</button>
      </div>

      <!-- Detail Content -->
      <div v-else-if="detail" class="detail-card">
        <div class="detail-header">
          <h1>Detail Riwayat Deteksi</h1>
          <span class="detail-date">{{ formatDate(detail.detected_at) }}</span>
        </div>

        <div class="detail-content">
          <!-- Image -->
          <div class="detail-image">
            <img :src="detail.image_url" :alt="detail.disease_name" />
          </div>

          <!-- Info -->
          <div class="detail-info">
            <div class="info-item">
              <label>Penyakit Terdeteksi:</label>
              <h2>{{ detail.disease_name }}</h2>
              <p v-if="detail.scientific_name" class="scientific-name">
                <em>{{ detail.scientific_name }}</em>
              </p>
            </div>

            <div class="info-item">
              <label>Tingkat Keyakinan:</label>
              <div class="confidence-bar">
                <div
                  class="confidence-fill"
                  :style="{ width: detail.confidence_percent + '%' }"
                ></div>
                <span class="confidence-text">{{ detail.confidence_percent }}%</span>
              </div>
            </div>

            <div class="info-item" v-if="detail.description">
              <label>Deskripsi:</label>
              <p>{{ detail.description }}</p>
            </div>

            <div class="info-item" v-if="detail.symptoms && detail.symptoms.length > 0">
              <label>Gejala:</label>
              <ul class="symptoms-list">
                <li v-for="(symptom, index) in detail.symptoms" :key="index">
                  {{ symptom }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { historyAPI } from '@/services/api' // Import historyAPI

const route = useRoute()
const historyId = computed(() => route.params.id)

const detail = ref(null)
const isLoading = ref(true)
const error = ref(null)

// Fetch detail dari API
async function fetchDetail() {
  isLoading.value = true
  error.value = null

  try {
    const response = await historyAPI.getHistoryDetail(historyId.value)

    console.log('API Response:', response.data) // Debug log

    if (response.data.success) {
      detail.value = response.data.data
    } else {
      throw new Error('Failed to fetch detail')
    }
  } catch (err) {
    console.error('Error fetching detail:', err)
    error.value = err.response?.data?.message || err.message || 'Gagal memuat detail'
  } finally {
    isLoading.value = false
  }
}

// Format tanggal
function formatDate(dateString) {
  if (!dateString) return '-'

  const date = new Date(dateString)
  return new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

onMounted(() => {
  fetchDetail()
})
</script>

<style scoped>
/* ... sama seperti sebelumnya ... */
.history-detail-view {
  min-height: 100vh;
  background: #f8faf9;
  padding: 140px 40px 80px;
}

.detail-container {
  max-width: 1000px;
  margin: 0 auto;
}

.btn-back {
  padding: 12px 24px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #1a3a2e;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 24px;
}

.btn-back:hover {
  background: #f8faf9;
  border-color: #6aa581;
  color: #6aa581;
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #6aa581;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error */
.error-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  border: 1px solid #fecaca;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.error-card h2 {
  color: #dc2626;
  margin-bottom: 12px;
  font-size: 20px;
}

.error-card p {
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 20px;
}

.btn-retry {
  padding: 12px 24px;
  background: #6aa581;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-retry:hover {
  background: #5a9470;
}

/* Detail Card */
.detail-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.detail-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a3a2e;
  margin: 0;
}

.detail-date {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.6);
}

.detail-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}

.detail-image {
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 1;
  background: #f8faf9;
  border: 1px solid #e5e7eb;
}

.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-item label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.6);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a3a2e;
  margin: 0 0 4px 0;
}

.scientific-name {
  font-size: 16px;
  color: rgba(0, 0, 0, 0.5);
  margin: 0;
}

.info-item p {
  font-size: 15px;
  color: rgba(0, 0, 0, 0.7);
  line-height: 1.6;
  margin: 0;
}

/* Confidence Bar */
.confidence-bar {
  position: relative;
  height: 40px;
  background: #f3f4f6;
  border-radius: 8px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #6aa581, #4a9068);
  transition: width 0.5s ease;
}

.confidence-text {
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  font-weight: 700;
  font-size: 16px;
  color: #1a3a2e;
}

/* Symptoms List */
.symptoms-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.symptoms-list li {
  padding: 12px 16px;
  background: #f8faf9;
  border-radius: 8px;
  margin-bottom: 8px;
  font-size: 15px;
  color: rgba(0, 0, 0, 0.7);
  border-left: 3px solid #6aa581;
}

/* Responsive */
@media (max-width: 768px) {
  .history-detail-view {
    padding: 100px 16px 48px;
  }

  .detail-card {
    padding: 24px;
  }

  .detail-content {
    grid-template-columns: 1fr;
  }

  .detail-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .detail-header h1 {
    font-size: 24px;
  }
}
</style>
