<template>
  <div class="history-view">
    <div class="history-container">
      <!-- Page Header -->
      <div class="page-header">
        <h1 class="page-title">Riwayat Deteksi</h1>
        <p class="page-description">
          Lihat dan kelola riwayat deteksi penyakit tanaman Anda
        </p>
      </div>

      <!-- History List -->
      <HistoryList />
    </div>
  </div>
</template>

<script setup>
import HistoryList from '@/components/history/HistoryList.vue';
</script>

<style scoped>
.history-view {
  min-height: 100vh;
  background: #f8faf9;
  padding: 140px 40px 80px;
  position: relative;
}

.history-view::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 60%;
  background: radial-gradient(circle at 50% 0%, rgba(106, 165, 129, 0.04) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.history-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.page-header {
  text-align: center;
  margin-bottom: 80px;
}

.page-title {
  font-size: 64px;
  font-weight: 700;
  color: #1a3a2e;
  margin: 0 0 20px 0;
  letter-spacing: -0.03em;
}

.page-description {
  font-size: 20px;
  color: rgba(0, 0, 0, 0.6);
  margin: 0;
  line-height: 1.7;
}

@media (max-width: 768px) {
  .history-view {
    padding: 100px 16px 48px;
  }

  .page-title {
    font-size: 36px;
  }

  .page-description {
    font-size: 17px;
  }
}
</style>
