<template>
  <div class="guide-view">
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1 class="page-title">Panduan Pengguna</h1>
        <p class="page-description">
          Pelajari cara menggunakan Grovia secara maksimal
        </p>
      </div>

      <!-- Quick Navigation -->
      <div class="quick-nav">
        <a
          v-for="section in sections"
          :key="section.id"
          :href="`#${section.id}`"
          class="nav-item"
        >
          {{ section.title }}
        </a>
      </div>

      <!-- Guide Content -->
      <div class="guide-content">
        <!-- Getting Started -->
        <section id="memulai" class="guide-section">
          <div class="section-icon">
            <Rocket :size="32" :stroke-width="2" />
          </div>
          <h2 class="section-title">Memulai dengan Grovia</h2>
          <div class="section-content">
            <h3>1. Membuat Akun</h3>
            <p>Untuk mulai menggunakan Grovia, Anda perlu membuat akun terlebih dahulu:</p>
            <ul>
              <li>Klik tombol "Daftar" di pojok kanan atas</li>
              <li>Masukkan nama lengkap, email, dan password Anda</li>
              <li>Klik "Daftar" untuk membuat akun</li>
              <li>Setelah berhasil, Anda akan langsung masuk ke dashboard</li>
            </ul>

            <h3>2. Login ke Akun</h3>
            <p>Jika sudah memiliki akun, Anda dapat login dengan:</p>
            <ul>
              <li>Klik tombol "Masuk" di pojok kanan atas</li>
              <li>Masukkan email dan password Anda</li>
              <li>Klik "Masuk" untuk mengakses dashboard</li>
            </ul>
          </div>
        </section>

        <!-- Detection Guide -->
        <section id="deteksi" class="guide-section">
          <div class="section-icon">
            <Search :size="32" :stroke-width="2" />
          </div>
          <h2 class="section-title">Melakukan Deteksi Penyakit</h2>
          <div class="section-content">
            <h3>Langkah-langkah Deteksi</h3>
            <ol>
              <li><strong>Pergi ke Halaman Deteksi</strong> - Klik menu "Deteksi Penyakit" di navigasi</li>
              <li><strong>Ambil atau Upload Foto</strong> - Pilih untuk mengambil foto langsung atau upload dari galeri</li>
              <li><strong>Tunggu Analisis</strong> - AI kami akan menganalisis foto dalam 3-10 detik</li>
              <li><strong>Lihat Hasil</strong> - Hasil deteksi akan menampilkan nama penyakit, tingkat kepercayaan, dan gejala</li>
              <li><strong>Lihat Rekomendasi</strong> - Klik "Lihat Rekomendasi Perawatan" untuk panduan penanganan</li>
            </ol>

            <h3>Tips Foto Terbaik</h3>
            <div class="tips-grid">
              <div class="tip-card">
                <Camera :size="24" />
                <h4>Pencahayaan Baik</h4>
                <p>Pastikan foto diambil dengan cahaya yang cukup, hindari bayangan gelap</p>
              </div>
              <div class="tip-card">
                <Leaf :size="24" />
                <h4>Fokus pada Daun</h4>
                <p>Ambil foto close-up dari daun yang menunjukkan gejala penyakit</p>
              </div>
              <div class="tip-card">
                <Maximize :size="24" />
                <h4>Resolusi Cukup</h4>
                <p>Gunakan foto minimal 224x224 piksel untuk hasil optimal</p>
              </div>
              <div class="tip-card">
                <Target :size="24" />
                <h4>Satu Daun per Foto</h4>
                <p>Fokus pada satu daun untuk akurasi deteksi yang lebih baik</p>
              </div>
            </div>
          </div>
        </section>

        <!-- History Guide -->
        <section id="riwayat" class="guide-section">
          <div class="section-icon">
            <FileText :size="32" :stroke-width="2" />
          </div>
          <h2 class="section-title">Mengelola Riwayat Deteksi</h2>
          <div class="section-content">
            <h3>Melihat Riwayat</h3>
            <p>Semua deteksi yang Anda lakukan akan tersimpan otomatis di halaman Riwayat:</p>
            <ul>
              <li>Klik menu "Riwayat" untuk melihat semua deteksi sebelumnya</li>
              <li>Setiap item menampilkan foto, nama penyakit, dan waktu deteksi</li>
              <li>Klik "Lihat Detail" untuk melihat informasi lengkap</li>
            </ul>

            <h3>Menghapus Riwayat</h3>
            <p>Untuk menghapus riwayat tertentu:</p>
            <ul>
              <li>Klik ikon tempat sampah pada item yang ingin dihapus</li>
              <li>Konfirmasi penghapusan pada dialog yang muncul</li>
              <li>Riwayat akan dihapus permanen</li>
            </ul>
          </div>
        </section>

        <!-- Knowledge Base -->
        <section id="pengetahuan" class="guide-section">
          <div class="section-icon">
            <BookOpen :size="32" :stroke-width="2" />
          </div>
          <h2 class="section-title">Basis Pengetahuan Penyakit</h2>
          <div class="section-content">
            <h3>Menjelajahi Database Penyakit</h3>
            <p>Grovia memiliki database lengkap tentang berbagai penyakit tanaman:</p>
            <ul>
              <li>Klik menu "Basis Pengetahuan" untuk mengakses</li>
              <li>Gunakan search bar untuk mencari penyakit spesifik</li>
              <li>Klik pada kartu penyakit untuk melihat detail lengkap</li>
              <li>Pelajari gejala, penyebab, dan cara penanganan</li>
            </ul>

            <h3>Informasi yang Tersedia</h3>
            <ul>
              <li>Nama ilmiah dan umum penyakit</li>
              <li>Deskripsi lengkap penyakit</li>
              <li>Gejala yang terlihat pada tanaman</li>
              <li>Tanaman yang terpengaruh</li>
              <li>Kategori penyakit (jamur, bakteri, virus, hama)</li>
              <li>Tingkat keparahan penyakit</li>
            </ul>
          </div>
        </section>

        <!-- Troubleshooting -->
        <section id="troubleshooting" class="guide-section">
          <div class="section-icon">
            <AlertCircle :size="32" :stroke-width="2" />
          </div>
          <h2 class="section-title">Pemecahan Masalah</h2>
          <div class="section-content">
            <h3>Hasil Deteksi Tidak Akurat</h3>
            <p>Jika hasil deteksi terasa kurang tepat:</p>
            <ul>
              <li>Coba ambil foto ulang dengan pencahayaan lebih baik</li>
              <li>Pastikan foto fokus dan tidak blur</li>
              <li>Ambil foto dari sudut yang berbeda</li>
              <li>Perhatikan tingkat kepercayaan (confidence score)</li>
              <li>Konsultasikan dengan ahli untuk verifikasi</li>
            </ul>

            <h3>Foto Tidak Bisa Diupload</h3>
            <p>Jika mengalami masalah saat upload foto:</p>
            <ul>
              <li>Pastikan format foto adalah JPG, JPEG, atau PNG</li>
              <li>Ukuran file maksimal 10MB</li>
              <li>Periksa koneksi internet Anda</li>
              <li>Coba refresh halaman dan upload ulang</li>
            </ul>

            <h3>Aplikasi Lambat atau Error</h3>
            <ul>
              <li>Clear cache dan cookies browser</li>
              <li>Pastikan menggunakan browser terbaru</li>
              <li>Periksa koneksi internet</li>
              <li>Hubungi support jika masalah berlanjut</li>
            </ul>
          </div>
        </section>
      </div>

      <!-- Support CTA -->
      <div class="support-cta">
        <h3>Butuh Bantuan Lebih Lanjut?</h3>
        <p>Tim support kami siap membantu Anda</p>
        <a href="mailto:support@grovia.com" class="btn-support">
          <Mail :size="18" />
          Hubungi Support
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Rocket, Search, Camera, Leaf, Maximize, Target, FileText, BookOpen, AlertCircle, Mail } from 'lucide-vue-next';

const sections = [
  { id: 'memulai', title: 'Memulai' },
  { id: 'deteksi', title: 'Deteksi Penyakit' },
  { id: 'riwayat', title: 'Riwayat' },
  { id: 'pengetahuan', title: 'Basis Pengetahuan' },
  { id: 'troubleshooting', title: 'Troubleshooting' },
];
</script>

<style scoped>
.guide-view {
  min-height: 100vh;
  background: #f8fafc;
  padding: 40px 20px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 48px;
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: #0f172a;
}

.page-description {
  font-size: 17px;
  color: #64748b;
  margin: 0;
}

/* Quick Navigation */
.quick-nav {
  display: flex;
  gap: 12px;
  margin-bottom: 40px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex-wrap: wrap;
  justify-content: center;
}

.nav-item {
  padding: 8px 20px;
  background: #f1f5f9;
  border-radius: 6px;
  text-decoration: none;
  color: #475569;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
}

.nav-item:hover {
  background: #16a34a;
  color: white;
}

/* Guide Content */
.guide-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
  margin-bottom: 60px;
}

.guide-section {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-radius: 12px;
  color: #16a34a;
  margin-bottom: 20px;
}

.section-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 24px 0;
}

.section-content h3 {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  margin: 24px 0 12px 0;
}

.section-content h3:first-child {
  margin-top: 0;
}

.section-content p {
  font-size: 15px;
  line-height: 1.7;
  color: #475569;
  margin: 0 0 16px 0;
}

.section-content ul,
.section-content ol {
  margin: 0 0 20px 0;
  padding-left: 24px;
}

.section-content li {
  font-size: 15px;
  line-height: 1.7;
  color: #475569;
  margin-bottom: 8px;
}

/* Tips Grid */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.tip-card {
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.tip-card svg {
  color: #16a34a;
  margin-bottom: 12px;
}

.tip-card h4 {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.tip-card p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
  margin: 0;
}

/* Support CTA */
.support-cta {
  text-align: center;
  padding: 48px 32px;
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  border-radius: 16px;
  border: 1px solid #bbf7d0;
}

.support-cta h3 {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px 0;
}

.support-cta p {
  font-size: 16px;
  color: #475569;
  margin: 0 0 24px 0;
}

.btn-support {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: #16a34a;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.25);
}

.btn-support:hover {
  background: #15803d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
}

/* Responsive */
@media (max-width: 768px) {
  .guide-section {
    padding: 24px 20px;
  }

  .page-title {
    font-size: 28px;
  }

  .section-title {
    font-size: 24px;
  }

  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>
