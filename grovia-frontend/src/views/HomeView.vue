<template>
  <div class="home-page">
    <!-- Hero Section - Layout seperti plants.me -->
    <section class="hero-section">
      <div class="hero-container">
        <!-- Text Content - Kiri, Lebar, Spasi Banyak -->
        <div class="hero-content">
          <h1 class="hero-title">
            Kesehatan<br>
            tanaman yang<br>
            semua orang<br>
            <span class="gradient-text">sukai</span>
          </h1>
          <div class="hero-action">
            <router-link
              :to="authStore.isAuthenticated ? '/detection' : '/register'"
              class="btn-explore"
            >
              Mulai Deteksi
            </router-link>
          </div>
        </div>

        <!-- Hero Image - Kanan, Large, Clean -->
        <div class="hero-visual">
          <div class="visual-container">
            <img
              src="@/assets/image/person-holding-green-leaf.jpg"
              alt="Grovia Plant Detection"
              class="hero-main-image"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Section - Grid Cards dengan Image -->
    <section class="featured-section">
      <div class="section-container">
        <div class="section-intro">
          <h2 class="intro-title">Deteksi berbagai jenis penyakit</h2>
          <p class="intro-text">
            Identifikasi masalah kesehatan tanaman Anda dengan teknologi AI.
            Dapatkan diagnosis akurat dan solusi perawatan dalam hitungan detik.
          </p>
        </div>

        <!-- Product Grid - 3 Kolom dengan Gambar Besar -->
        <div class="product-grid">
          <div class="product-card">
            <div class="product-image">
              <img src="@/assets/image/side-view-woman-looking-leaves.jpg" alt="Deteksi Cepat" />
            </div>
            <div class="product-info">
              <h3 class="product-name">Deteksi Cepat</h3>
              <p class="product-detail">AI-Powered | Hasil Instan</p>
            </div>
          </div>

          <div class="product-card">
            <div class="product-image">
              <img src="@/assets/image/top-view-plants-notebook-arrangement.jpg" alt="Analisis Mendalam" />
            </div>
            <div class="product-info">
              <h3 class="product-name">Analisis Lengkap</h3>
              <p class="product-detail">10+ Jenis Penyakit | Akurasi 95%</p>
            </div>
          </div>

          <div class="product-card">
            <div class="product-image">
              <img src="@/assets/image/eco-friendly-recycling-concept.jpg" alt="Rekomendasi" />
            </div>
            <div class="product-info">
              <h3 class="product-name">Solusi Tepat</h3>
              <p class="product-detail">Organik & Kimia | Mudah Diikuti</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="section-container">
        <div class="section-header">
          <h2 class="section-title">Mengapa memilih Grovia?</h2>
        </div>

        <div class="features-list">
          <div class="feature-item">
            <div class="feature-number">01</div>
            <h3 class="feature-name">Teknologi AI Terpercaya</h3>
            <p class="feature-text">
              Menggunakan Convolutional Neural Network yang telah dilatih dengan ribuan data penyakit tanaman untuk hasil yang akurat.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-number">02</div>
            <h3 class="feature-name">Hasil dalam Hitungan Detik</h3>
            <p class="feature-text">
              Upload foto dan dapatkan diagnosis lengkap beserta rekomendasi perawatan dalam waktu singkat.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-number">03</div>
            <h3 class="feature-name">Basis Pengetahuan Lengkap</h3>
            <p class="feature-text">
              Akses informasi detail tentang berbagai jenis penyakit, gejala, pencegahan, dan cara penanganan.
            </p>
          </div>

          <div class="feature-item">
            <div class="feature-number">04</div>
            <h3 class="feature-name">Pantau Riwayat Tanaman</h3>
            <p class="feature-text">
              Simpan dan lacak kesehatan tanaman Anda dari waktu ke waktu untuk perawatan yang lebih baik.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works-section">
      <div class="section-container">
        <div class="section-intro">
          <h2 class="intro-title">Cara Kerja</h2>
          <p class="intro-text">
            Deteksi penyakit tanaman dalam 3 langkah mudah
          </p>
        </div>

        <div class="steps-container">
          <div class="step-item">
            <div class="step-badge">1</div>
            <div class="step-content">
              <h3 class="step-title">Upload Foto</h3>
              <p class="step-text">
                Ambil atau upload foto daun tanaman yang menunjukkan gejala penyakit dengan jelas.
              </p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-badge">2</div>
            <div class="step-content">
              <h3 class="step-title">AI Menganalisis</h3>
              <p class="step-text">
                AI kami akan menganalisis gambar dan mendeteksi jenis penyakit dengan tingkat kepercayaan tinggi.
              </p>
            </div>
          </div>

          <div class="step-item">
            <div class="step-badge">3</div>
            <div class="step-content">
              <h3 class="step-title">Dapatkan Solusi</h3>
              <p class="step-text">
                Terima hasil deteksi lengkap dengan rekomendasi perawatan yang tepat untuk tanaman Anda.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-container">
        <h2 class="cta-title">Mulai jaga kesehatan tanaman Anda hari ini</h2>
        <router-link
          :to="authStore.isAuthenticated ? '/detection' : '/register'"
          class="cta-button"
        >
          Deteksi Sekarang - Gratis
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  CheckCircle2,
  Bot,
  Users,
  Leaf,
  Sparkles,
  Rocket,
  BookOpen,
  Search,
  Pill,
  BarChart3,
  Smartphone,
  Camera,
  Zap,
  CheckCircle
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isLoggedIn)

const goToDetection = () => {
  if (isLoggedIn.value) {
    router.push('/detection')
  } else {
    router.push('/login')
  }
}
</script>

<style scoped>
.home-page {
  width: 100%;
  background: #f8faf9;
}

/* ============================================
   HERO SECTION - Layout Seperti Plants.me
   ============================================ */
.hero-section {
  background: #6aa581;
  padding: 140px 40px 160px;
  margin-top: -100px;
  padding-top: 160px;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.08) 0%, transparent 50%);
  pointer-events: none;
}

.hero-container {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 120px;
  align-items: center;
}

/* Content Kiri - Minimalis & Spasi Besar */
.hero-content {
  max-width: 600px;
}

.hero-title {
  font-size: 76px;
  font-weight: 700;
  line-height: 1.1;
  margin: 0 0 56px 0;
  color: #ffffff;
  letter-spacing: -0.025em;
}

.gradient-text {
  color: #fff8e1;
  display: inline;
}

.hero-action {
  margin-top: 48px;
}

.btn-explore {
  display: inline-block;
  padding: 20px 44px;
  background: #ffffff;
  color: #2d5f4a;
  font-size: 17px;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  letter-spacing: -0.01em;
}

.btn-explore:hover {
  background: transparent;
  color: #ffffff;
  border-color: #ffffff;
}

/* Visual Kanan - Gambar Besar Clean */
.hero-visual {
  position: relative;
  display: flex;
  justify-content: flex-end;
}

.visual-container {
  width: 100%;
  max-width: 480px;
  aspect-ratio: 3/4;
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
  background: #f5f5f5;
}

.hero-main-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.hero-visual:hover .hero-main-image {
  transform: scale(1.05);
}

/* ============================================
   FEATURED SECTION - Grid 3 Kolom Product
   ============================================ */
.featured-section {
  padding: 120px 40px;
  background: #f8faf9;
  position: relative;
}

.featured-section::before {
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

.section-container {
  max-width: 1320px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.section-intro {
  max-width: 800px;
  margin-bottom: 80px;
}

.intro-title {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.15;
  margin: 0 0 28px 0;
  color: #1a1a1a;
  letter-spacing: -0.025em;
}

.intro-text {
  font-size: 20px;
  line-height: 1.6;
  color: #666;
  margin: 0;
}

/* Product Grid - 3 Kolom dengan Gambar */
.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.product-card {
  background: #ffffff;
  border-radius: 20px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  border: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #6aa581;
}

.product-image {
  width: 100%;
  aspect-ratio: 1;
  overflow: hidden;
  background: #e8ede9;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.product-info {
  padding: 32px 28px;
}

.product-name {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 10px 0;
  color: #1a1a1a;
  letter-spacing: -0.01em;
}

.product-detail {
  font-size: 15px;
  color: #6aa581;
  margin: 0;
  font-weight: 500;
}

/* ============================================
   HOW IT WORKS SECTION - Clean & Minimal
   ============================================ */
.how-it-works-section {
  padding: 120px 40px;
  background: #ffffff;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 48px;
  align-items: start;
  position: relative;
  margin-top: 64px;
  max-width: 1100px;
  margin-left: auto;
  margin-right: auto;
}

.step-card {
  background: #ffffff;
  padding: 40px 32px;
  border-radius: 16px;
  text-align: left;
  border: 1px solid #e5e7eb;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.step-card:hover {
  border-color: #6aa581;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.step-number {
  position: absolute;
  top: -16px;
  left: 32px;
  width: 48px;
  height: 48px;
  background: #6aa581;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(106, 165, 129, 0.25);
}

.step-icon {
  display: none;
}

.step-title {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 24px 0 12px 0;
  letter-spacing: -0.01em;
}

.step-description {
  font-size: 16px;
  line-height: 1.7;
  color: #666;
  margin: 0;
}

.step-connector {
  display: none;
}
.features-section {
  padding: 120px 40px;
  background: #ffffff;
}

.section-header {
  text-align: center;
  margin-bottom: 96px;
}

.section-title {
  font-size: 48px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  letter-spacing: -0.02em;
}

/* Features List - Simple & Clean */
.features-list {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 72px 100px;
}

.feature-item {
  position: relative;
}

.feature-number {
  font-size: 16px;
  font-weight: 700;
  color: #6aa581;
  margin-bottom: 16px;
  letter-spacing: 0.05em;
}

.feature-name {
  font-size: 26px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #1a1a1a;
  letter-spacing: -0.01em;
}

.feature-text {
  font-size: 16px;
  line-height: 1.7;
  color: #666;
  margin: 0;
}

/* ============================================
   CTA SECTION - Simple & Centered
   ============================================ */
.cta-section {
  padding: 140px 40px;
  background: #6aa581;
  text-align: center;
}

.cta-container {
  max-width: 900px;
  margin: 0 auto;
}

.cta-title {
  font-size: 52px;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 52px 0;
  color: #ffffff;
  letter-spacing: -0.025em;
}

.cta-button {
  display: inline-block;
  padding: 20px 48px;
  background: #ffffff;
  color: #2d5f4a;
  font-size: 18px;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.cta-button:hover {
  background: transparent;
  color: #ffffff;
  border-color: #ffffff;
}

.gradient-text {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  margin-top: 8px;
  font-weight: 900;
  word-wrap: break-word;
  overflow-wrap: break-word;
  /* Fallback untuk browser yang tidak support gradient text */
  color: #fef3c7;
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.2));
}

/* Support untuk gradient text */
@supports (background-clip: text) or (-webkit-background-clip: text) {
  .gradient-text {
    color: transparent;
  }
}

.hero-description {
  font-size: 20px;
  line-height: 1.75;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 10px rgba(0, 0, 0, 0.1);
}

.hero-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.btn-primary,
.btn-secondary {
  padding: 16px 32px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  letter-spacing: -0.01em;
}

.btn-primary {
  background: #ffffff;
  color: #059669;
  box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
  font-weight: 700;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(16, 185, 129, 0.05);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-primary:hover::before {
  opacity: 1;
}

.btn-primary:hover {
  background: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px 0 rgba(0, 0, 0, 0.25);
}

.btn-primary:focus-visible,
.btn-secondary:focus-visible {
  outline: 3px solid rgba(22, 163, 74, 0.4);
  outline-offset: 2px;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  border: 2px solid rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  font-weight: 600;
}

.btn-secondary::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: rgba(255, 255, 255, 0.25);
  transition: width 0.3s ease;
  z-index: -1;
}

.btn-secondary:hover::before {
  width: 100%;
}

.btn-secondary:hover {
  border-color: #ffffff;
  background: rgba(255, 255, 255, 0.2);
}

.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 32px;
  padding-top: 0;
  border-top: none;
}

.stat-item {
  text-align: left;
  padding: 24px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

.stat-item::before {
  display: none;
}

.stat-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.25);
}

.stat-item:hover::before {
  opacity: 0;
}

.stat-number {
  font-size: 40px;
  font-weight: 900;
  margin-bottom: 8px;
  color: #ffffff;
  letter-spacing: -0.03em;
  line-height: 1;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  line-height: 1.5;
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

/* Soft glow effect around the card */
.hero-image::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 520px;
  height: 520px;
  background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0.3) 40%, transparent 70%);
  border-radius: 50%;
  z-index: 0;
  pointer-events: none;
}

.image-card {
  width: 520px;
  height: 520px;
  background: white;
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  border: none;
  position: relative;
  overflow: hidden;
  z-index: 1;
  transition: all 0.4s ease;
}

.image-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
}

/* Simple image placeholder */
.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  overflow: hidden;
}

.hero-image-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.4s ease;
}

.image-card:hover .hero-image-photo {
  transform: scale(1.05);
}

.placeholder-icon {
  color: #16a34a;
  opacity: 0.6;
}

/* Floating badges - more subtle */
.floating-badge {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: white;
  border-radius: 50px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
  z-index: 2;
  border: 1px solid #e2e8f0;
}

.badge-ai {
  top: 30px;
  left: -10px;
  color: #16a34a;
}

.badge-ai svg {
  color: #16a34a;
}

.badge-accuracy {
  bottom: 50px;
  right: -10px;
  color: #0891b2;
}

.badge-accuracy svg {
  color: #0891b2;
}

/* Features Section - Clean & Minimal */
.features-section {
  padding: 120px 20px;
  background: #ffffff;
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 72px;
  max-width: 640px;
  margin-left: auto;
  margin-right: auto;
}

.section-title {
  font-size: 40px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 16px 0;
  letter-spacing: -0.03em;
  font-feature-settings: 'ss01' 1;
}

.section-description {
  font-size: 18px;
  color: #64748b;
  margin: 0;
  font-weight: 400;
  line-height: 1.7;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.feature-card {
  padding: 48px 40px;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #10b981 0%, #0d9488 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  border-color: #10b981;
  box-shadow: 0 12px 32px rgba(16, 185, 129, 0.15);
  transform: translateY(-8px);
}

.feature-icon {
  color: #16a34a;
  margin-bottom: 20px;
  display: flex;
}

.feature-title {
  font-size: 19px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 12px 0;
  letter-spacing: -0.01em;
}

.feature-description {
  font-size: 15px;
  line-height: 1.7;
  color: #64748b;
  margin: 0;
}

/* ============================================
   HOW IT WORKS SECTION - Clean & Minimal
   ============================================ */
.how-it-works-section {
  padding: 120px 40px;
  background: #ffffff;
}

.steps-grid,
.steps-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 48px;
  margin-top: 64px;
  max-width: 1100px;
  margin-left: auto;
  margin-right: auto;
}

.step-card,
.step-item {
  background: #f8faf9;
  padding: 40px 32px;
  border-radius: 16px;
  border: 1px solid #e8e8e8;
  position: relative;
  transition: all 0.3s ease;
  text-align: left;
}

.step-card:hover,
.step-item:hover {
  border-color: #6aa581;
  box-shadow: 0 8px 24px rgba(106, 165, 129, 0.12);
  transform: translateY(-4px);
}

.step-number,
.step-badge {
  position: absolute;
  top: -16px;
  left: 32px;
  width: 48px;
  height: 48px;
  background: #6aa581;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 20px;
  box-shadow: 0 4px 12px rgba(106, 165, 129, 0.25);
}

.step-icon {
  display: none;
}

.step-content {
  margin-top: 24px;
}

.step-title {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 12px 0;
  letter-spacing: -0.01em;
}

.step-description,
.step-text {
  font-size: 16px;
  line-height: 1.7;
  color: #666;
  margin: 0;
}

.step-connector {
  display: none;
}

/* ============================================
   CTA SECTION - Simple & Centered
   ============================================ */
.cta-section {
  padding: 140px 40px;
  background: #f8faf9;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 30% 50%, rgba(106, 165, 129, 0.04) 0%, transparent 50%);
  pointer-events: none;
}

.cta-container {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.cta-content {
  text-align: center;
}

.cta-title {
  font-size: 52px;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 52px 0;
  color: #1a3a2e;
  letter-spacing: -0.025em;
}

.cta-description {
  font-size: 19px;
  line-height: 1.7;
  color: rgba(0, 0, 0, 0.7);
  margin: 0 0 40px 0;
}

.cta-button {
  display: inline-block;
  padding: 20px 48px;
  background: #6aa581;
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  box-shadow: 0 4px 16px rgba(106, 165, 129, 0.25);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.cta-button:hover {
  background: #5a9470;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(106, 165, 129, 0.35);
}

.cta-button:focus-visible {
  outline: 3px solid rgba(106, 165, 129, 0.4);
  outline-offset: 2px;
}

/* ============================================
   RESPONSIVE
   ============================================ */

@media (max-width: 1200px) {
  .hero-container {
    gap: 80px;
    padding: 0 20px;
  }

  .hero-title {
    font-size: 64px;
  }

  .product-grid {
    gap: 32px;
  }

  .features-list {
    gap: 64px 80px;
  }
}

@media (max-width: 968px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 48px;
  }

  .hero-visual {
    justify-content: center;
    order: -1;
  }

  .hero-content {
    max-width: 100%;
    text-align: center;
  }

  .hero-title {
    font-size: 56px;
    margin-bottom: 32px;
  }

  .hero-action {
    margin-top: 32px;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .features-list {
    grid-template-columns: 1fr;
    gap: 48px;
  }

  .intro-title {
    font-size: 40px;
  }

  .section-title {
    font-size: 36px;
  }

  .cta-title {
    font-size: 40px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 120px 20px 100px;
    margin-top: -70px;
    padding-top: 130px;
  }

  .hero-title {
    font-size: 44px;
  }

  .btn-explore,
  .cta-button {
    padding: 16px 32px;
    font-size: 15px;
  }

  .intro-title {
    font-size: 32px;
  }

  .intro-text {
    font-size: 18px;
  }

  .product-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .product-name {
    font-size: 20px;
  }

  .feature-name {
    font-size: 22px;
  }

  .cta-title {
    font-size: 32px;
    margin-bottom: 32px;
  }

  .featured-section,
  .features-section {
    padding: 80px 20px;
  }

  .cta-section {
    padding: 80px 20px;
  }
}

@media (max-width: 640px) {
  .hero-section {
    padding: 100px 20px 100px;
    margin-top: -60px;
    padding-top: 120px;
  }

  .hero-title {
    font-size: 40px;
    line-height: 1.15;
    margin-bottom: 40px;
  }

  .visual-container {
    max-width: 100%;
    border-radius: 24px;
  }

  .section-intro {
    margin-bottom: 56px;
  }

  .intro-title {
    font-size: 32px;
    margin-bottom: 20px;
  }

  .intro-text {
    font-size: 17px;
  }

  .product-info {
    padding: 24px 20px;
  }

  .product-name {
    font-size: 20px;
  }

  .product-detail {
    font-size: 14px;
  }

  .feature-number {
    font-size: 14px;
  }

  .feature-name {
    font-size: 22px;
  }

  .feature-text {
    font-size: 16px;
  }

  .section-title {
    font-size: 32px;
  }

  .cta-title {
    font-size: 32px;
    line-height: 1.25;
    margin-bottom: 40px;
  }

  .btn-explore,
  .cta-button {
    width: 100%;
    max-width: 320px;
    padding: 18px 36px;
  }

  .featured-section,
  .features-section {
    padding: 80px 20px;
  }

  .cta-section {
    padding: 100px 20px;
  }
}
</style>
