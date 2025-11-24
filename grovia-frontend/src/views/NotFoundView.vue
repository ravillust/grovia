<template>
  <div class="not-found-page">
    <div class="not-found-container">
      <div class="error-code">404</div>
      <div class="error-icon">
        <span class="error-icon-left"><Leaf :size="64" :stroke-width="1.8" /></span>
        <span class="error-icon-right"><Search :size="40" :stroke-width="1.6" /></span>
      </div>
      <h1 class="error-title">Halaman Tidak Ditemukan</h1>
      <p class="error-description">
        Maaf, halaman yang Anda cari tidak dapat ditemukan.
        Mungkin halaman telah dipindahkan atau URL salah.
      </p>
      <div class="error-actions">
        <router-link to="/" class="btn-primary">
          <Home :size="18" :stroke-width="1.6" style="margin-right:8px; vertical-align:middle;" /> Kembali ke Beranda
        </router-link>
        <router-link
          :to="authStore.isAuthenticated ? '/detection' : '/register'"
          class="btn-secondary"
        >
          <Search :size="16" :stroke-width="1.6" style="margin-right:8px; vertical-align:middle;" /> Mulai Deteksi
        </router-link>
      </div>

      <!-- Quick Links -->
      <div class="quick-links">
        <p class="quick-links-title">Atau kunjungi:</p>
        <div class="links-grid">
          <router-link to="/detection" class="quick-link">
            <span class="link-icon"><Search :size="20" :stroke-width="1.6" /></span>
            <span>Deteksi Penyakit</span>
          </router-link>
          <router-link to="/history" class="quick-link">
            <span class="link-icon"><FileText :size="20" :stroke-width="1.6" /></span>
            <span>Riwayat</span>
          </router-link>
          <router-link to="/knowledge-base" class="quick-link">
            <span class="link-icon"><BookOpen :size="20" :stroke-width="1.6" /></span>
            <span>Pengetahuan</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { Leaf, Search, Home, FileText, BookOpen } from 'lucide-vue-next';

const authStore = useAuthStore();
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
}

.not-found-container {
  max-width: 600px;
  text-align: center;
}

.error-code {
  font-size: 120px;
  font-weight: 900;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 24px;
  opacity: 0.3;
}

.error-icon {
  font-size: 80px;
  margin-bottom: 24px;
  animation: bounce 2s infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-icon svg {
  display: inline-block;
  vertical-align: middle;
  color: #16a34a;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.error-title {
  font-size: 36px;
  font-weight: 800;
  color: #2d3748;
  margin: 0 0 16px 0;
}

.error-description {
  font-size: 18px;
  line-height: 1.7;
  color: #718096;
  margin: 0 0 40px 0;
}

.error-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
}

.btn-primary,
.btn-secondary {
  padding: 14px 32px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #f7fafc;
}

.quick-links {
  margin-top: 40px;
  padding-top: 40px;
  border-top: 2px solid #e2e8f0;
}

.quick-links-title {
  font-size: 14px;
  font-weight: 600;
  color: #718096;
  margin: 0 0 20px 0;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.quick-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  text-decoration: none;
  color: #4a5568;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.quick-link:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  color: #667eea;
}

.link-icon {
  font-size: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.link-icon svg {
  display: block;
}

@media (max-width: 640px) {
  .error-code {
    font-size: 80px;
  }

  .error-icon {
    font-size: 60px;
  }

  .error-title {
    font-size: 28px;
  }

  .error-description {
    font-size: 16px;
  }

  .error-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .links-grid {
    grid-template-columns: 1fr;
  }
}
</style>
