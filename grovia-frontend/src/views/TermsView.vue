<template>
  <div class="terms">
    <div class="container">
      <!-- Header -->
      <div class="header">
        <FileCheck :size="48" class="header-icon" />
        <h1>Syarat dan Ketentuan</h1>
        <p class="updated">Terakhir diperbarui: 31 Oktober 2025</p>
      </div>

      <!-- Introduction -->
      <section class="section">
        <p class="intro">
          Selamat datang di Grovia! Dengan menggunakan layanan deteksi penyakit tanaman kami, Anda menyetujui 
          Syarat dan Ketentuan berikut. Harap baca dengan saksama sebelum menggunakan aplikasi.
        </p>
      </section>

      <!-- Acceptance -->
      <section class="section">
        <div class="section-header">
          <CheckCircle :size="24" />
          <h2>Penerimaan Ketentuan</h2>
        </div>
        
        <p>
          Dengan mengakses atau menggunakan Grovia, Anda setuju untuk terikat oleh Syarat dan Ketentuan ini. 
          Jika Anda tidak setuju dengan bagian mana pun dari ketentuan ini, Anda tidak boleh menggunakan layanan kami.
        </p>
        
        <div class="info-box success">
          <CheckCircle :size="24" />
          <div>
            <h4>Persetujuan Anda Berarti:</h4>
            <ul>
              <li>Anda telah membaca dan memahami ketentuan ini</li>
              <li>Anda berusia minimal 13 tahun atau mendapat izin orang tua/wali</li>
              <li>Anda akan menggunakan layanan sesuai dengan ketentuan yang berlaku</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Service Description -->
      <section class="section">
        <div class="section-header">
          <Info :size="24" />
          <h2>Deskripsi Layanan</h2>
        </div>
        
        <p>Grovia menyediakan layanan deteksi penyakit tanaman menggunakan teknologi kecerdasan buatan (AI) yang meliputi:</p>
        
        <div class="service-list">
          <div class="service-item">
            <Camera :size="20" />
            <div>
              <h4>Deteksi Penyakit</h4>
              <p>Analisis gambar tanaman untuk mengidentifikasi penyakit dengan tingkat kepercayaan tertentu</p>
            </div>
          </div>
          
          <div class="service-item">
            <History :size="20" />
            <div>
              <h4>Riwayat Deteksi</h4>
              <p>Penyimpanan hasil deteksi untuk referensi dan pemantauan jangka panjang</p>
            </div>
          </div>
          
          <div class="service-item">
            <BookOpen :size="20" />
            <div>
              <h4>Basis Pengetahuan</h4>
              <p>Informasi komprehensif tentang berbagai penyakit tanaman dan penanganannya</p>
            </div>
          </div>
          
          <div class="service-item">
            <Pill :size="20" />
            <div>
              <h4>Rekomendasi Perawatan</h4>
              <p>Saran penanganan dan pencegahan berdasarkan hasil deteksi</p>
            </div>
          </div>
        </div>
      </section>

      <!-- User Obligations -->
      <section class="section">
        <div class="section-header">
          <UserCheck :size="24" />
          <h2>Kewajiban Pengguna</h2>
        </div>
        
        <div class="subsection">
          <h3>Anda Setuju Untuk:</h3>
          <ul class="check-list">
            <li>Memberikan informasi akun yang akurat dan lengkap</li>
            <li>Menjaga kerahasiaan kata sandi Anda</li>
            <li>Menggunakan layanan hanya untuk tujuan yang sah dan legal</li>
            <li>Tidak menyalahgunakan atau mencoba merusak sistem</li>
            <li>Menghormati hak kekayaan intelektual Grovia</li>
            <li>Mematuhi semua hukum dan peraturan yang berlaku</li>
          </ul>
        </div>

        <div class="subsection">
          <h3>Anda Tidak Boleh:</h3>
          <ul class="x-list">
            <li>Mengunggah konten yang melanggar hukum, menyesatkan, atau berbahaya</li>
            <li>Menggunakan layanan untuk spam atau penipuan</li>
            <li>Mencoba mengakses akun pengguna lain tanpa izin</li>
            <li>Melakukan reverse engineering terhadap sistem kami</li>
            <li>Menggunakan bot atau otomasi tanpa izin tertulis</li>
            <li>Menjual kembali atau mengomersialkan layanan tanpa persetujuan</li>
          </ul>
        </div>
      </section>

      <!-- Disclaimer -->
      <section class="section">
        <div class="section-header">
          <AlertTriangle :size="24" />
          <h2>Penafian (Disclaimer)</h2>
        </div>
        
        <div class="info-box warning">
          <AlertTriangle :size="24" />
          <div>
            <h4>Penting untuk Diketahui:</h4>
            <p>
              Grovia adalah alat bantu deteksi yang menggunakan AI dan <strong>tidak menggantikan konsultasi profesional</strong>. 
              Hasil deteksi bersifat prediktif dan mungkin tidak 100% akurat. Untuk keputusan penting terkait pertanian atau 
              kesehatan tanaman, kami sangat menyarankan konsultasi dengan ahli pertanian, agronomis, atau pakar penyakit tanaman.
            </p>
          </div>
        </div>

        <div class="disclaimer-points">
          <div class="disclaimer-point">
            <span class="number">1</span>
            <div>
              <h4>Akurasi Tidak Dijamin</h4>
              <p>
                Meskipun kami berusaha keras untuk meningkatkan akurasi model AI, hasil deteksi mungkin tidak selalu tepat. 
                Faktor seperti kualitas gambar, pencahayaan, dan sudut pengambilan dapat mempengaruhi hasil.
              </p>
            </div>
          </div>

          <div class="disclaimer-point">
            <span class="number">2</span>
            <div>
              <h4>Tidak untuk Keputusan Kritis</h4>
              <p>
                Jangan mengandalkan Grovia sebagai satu-satunya sumber informasi untuk keputusan penting yang dapat 
                mempengaruhi kesehatan tanaman, hasil panen, atau keamanan pangan.
              </p>
            </div>
          </div>

          <div class="disclaimer-point">
            <span class="number">3</span>
            <div>
              <h4>Layanan "As Is"</h4>
              <p>
                Layanan disediakan "sebagaimana adanya" tanpa jaminan apa pun, baik tersurat maupun tersirat, 
                termasuk namun tidak terbatas pada jaminan kelayakan untuk tujuan tertentu.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Intellectual Property -->
      <section class="section">
        <div class="section-header">
          <Copyright :size="24" />
          <h2>Hak Kekayaan Intelektual</h2>
        </div>
        
        <p>
          Semua konten di Grovia, termasuk namun tidak terbatas pada teks, grafik, logo, ikon, gambar, klip audio, 
          unduhan digital, kompilasi data, model AI, dan perangkat lunak, adalah milik Grovia atau pemberi lisensinya 
          dan dilindungi oleh hukum hak cipta internasional.
        </p>

        <div class="ip-grid">
          <div class="ip-card">
            <Code :size="24" />
            <h4>Kode Sumber</h4>
            <p>Kode sumber dan algoritma adalah milik eksklusif Grovia</p>
          </div>

          <div class="ip-card">
            <Database :size="24" />
            <h4>Model AI</h4>
            <p>Model deteksi dan data training dilindungi hak cipta</p>
          </div>

          <div class="ip-card">
            <Leaf :size="24" />
            <h4>Logo & Brand</h4>
            <p>Logo Grovia dan merek dagang terdaftar</p>
          </div>

          <div class="ip-card">
            <FileText :size="24" />
            <h4>Konten</h4>
            <p>Artikel, panduan, dan basis pengetahuan</p>
          </div>
        </div>
      </section>

      <!-- User Content -->
      <section class="section">
        <div class="section-header">
          <Upload :size="24" />
          <h2>Konten Pengguna</h2>
        </div>
        
        <p>Ketika Anda mengunggah gambar atau konten lain ke Grovia:</p>

        <div class="content-terms">
          <div class="term-item">
            <Shield :size="20" />
            <div>
              <h4>Anda Tetap Memiliki Hak</h4>
              <p>Anda mempertahankan semua hak atas konten yang Anda unggah</p>
            </div>
          </div>

          <div class="term-item">
            <Share2 :size="20" />
            <div>
              <h4>Lisensi Terbatas</h4>
              <p>Anda memberikan kami lisensi non-eksklusif untuk memproses dan menyimpan konten Anda guna menyediakan layanan</p>
            </div>
          </div>

          <div class="term-item">
            <Zap :size="20" />
            <div>
              <h4>Peningkatan Layanan</h4>
              <p>Data Anda dapat digunakan secara anonim untuk meningkatkan akurasi model AI</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Limitation of Liability -->
      <section class="section">
        <div class="section-header">
          <ShieldOff :size="24" />
          <h2>Batasan Tanggung Jawab</h2>
        </div>
        
        <p>
          Sejauh diizinkan oleh hukum yang berlaku, Grovia dan afiliasinya tidak bertanggung jawab atas:
        </p>

        <ul class="liability-list">
          <li>Kerugian langsung, tidak langsung, insidental, atau konsekuensial yang timbul dari penggunaan layanan</li>
          <li>Kehilangan keuntungan, data, atau peluang bisnis</li>
          <li>Kegagalan panen atau kerugian pertanian yang didasarkan pada hasil deteksi</li>
          <li>Gangguan layanan, kesalahan, atau ketidaktersediaan sistem</li>
          <li>Keputusan yang dibuat berdasarkan informasi yang diberikan oleh layanan</li>
        </ul>

        <div class="info-box error">
          <XCircle :size="24" />
          <div>
            <h4>Batas Maksimal Tanggung Jawab</h4>
            <p>
              Dalam hal apa pun, tanggung jawab total kami kepada Anda untuk semua klaim yang timbul dari atau 
              terkait dengan layanan tidak akan melebihi jumlah yang Anda bayarkan kepada kami dalam 12 bulan 
              terakhir, atau Rp 100.000 (mana yang lebih besar).
            </p>
          </div>
        </div>
      </section>

      <!-- Service Availability -->
      <section class="section">
        <div class="section-header">
          <Globe :size="24" />
          <h2>Ketersediaan Layanan</h2>
        </div>
        
        <p>
          Kami berusaha menjaga layanan tetap tersedia 24/7, namun kami tidak menjamin akses tanpa gangguan. 
          Layanan mungkin tidak tersedia karena:
        </p>

        <div class="availability-grid">
          <div class="availability-item">
            <Wrench :size="20" />
            <p>Pemeliharaan terjadwal atau darurat</p>
          </div>
          <div class="availability-item">
            <Wifi :size="20" />
            <p>Masalah koneksi internet atau jaringan</p>
          </div>
          <div class="availability-item">
            <Server :size="20" />
            <p>Kegagalan server atau perangkat keras</p>
          </div>
          <div class="availability-item">
            <Zap :size="20" />
            <p>Keadaan kahar (force majeure)</p>
          </div>
        </div>
      </section>

      <!-- Account Termination -->
      <section class="section">
        <div class="section-header">
          <UserX :size="24" />
          <h2>Penangguhan dan Penghentian</h2>
        </div>
        
        <p>Kami berhak menangguhkan atau menghentikan akun Anda jika:</p>

        <ul class="termination-list">
          <li>Anda melanggar Syarat dan Ketentuan ini</li>
          <li>Kami mencurigai aktivitas penipuan atau penyalahgunaan</li>
          <li>Anda memberikan informasi palsu atau menyesatkan</li>
          <li>Atas permintaan Anda sendiri</li>
          <li>Diwajibkan oleh hukum atau otoritas pemerintah</li>
        </ul>

        <p>
          Anda dapat menghapus akun Anda kapan saja dengan menghubungi dukungan pelanggan. 
          Setelah penghapusan, data Anda akan dihapus sesuai <router-link to="/privacy">Kebijakan Privasi</router-link> kami.
        </p>
      </section>

      <!-- Changes to Terms -->
      <section class="section">
        <div class="section-header">
          <RefreshCw :size="24" />
          <h2>Perubahan Ketentuan</h2>
        </div>
        
        <p>
          Kami dapat merevisi Syarat dan Ketentuan ini dari waktu ke waktu. Perubahan signifikan akan kami beritahukan 
          melalui email atau notifikasi di aplikasi. Dengan terus menggunakan layanan setelah perubahan berlaku, 
          Anda menyetujui ketentuan yang diperbarui.
        </p>
      </section>

      <!-- Governing Law -->
      <section class="section">
        <div class="section-header">
          <Scale :size="24" />
          <h2>Hukum yang Berlaku</h2>
        </div>
        
        <p>
          Syarat dan Ketentuan ini diatur oleh dan ditafsirkan sesuai dengan hukum Republik Indonesia. 
          Setiap perselisihan yang timbul dari atau terkait dengan ketentuan ini akan diselesaikan di 
          pengadilan yang berwenang di Indonesia.
        </p>
      </section>

      <!-- Contact -->
      <section class="section">
        <div class="section-header">
          <Mail :size="24" />
          <h2>Hubungi Kami</h2>
        </div>
        
        <p>
          Jika Anda memiliki pertanyaan tentang Syarat dan Ketentuan ini, silakan hubungi kami:
        </p>
        
        <div class="contact-box">
          <div class="contact-item">
            <Mail :size="20" />
            <a href="mailto:legal@grovia.com">legal@grovia.com</a>
          </div>
          <div class="contact-item">
            <MessageCircle :size="20" />
            <router-link to="/faq">FAQ - Pertanyaan Umum</router-link>
          </div>
        </div>
      </section>

      <!-- Back to Home -->
      <div class="back-link">
        <router-link to="/">
          <ArrowLeft :size="20" />
          Kembali ke Beranda
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  FileCheck, CheckCircle, Info, Camera, History, BookOpen, Pill,
  UserCheck, AlertTriangle, Copyright, Code, Database, Leaf, FileText,
  Upload, Shield, Share2, Zap, ShieldOff, XCircle, Globe, Wrench,
  Wifi, Server, UserX, RefreshCw, Scale, Mail, MessageCircle, ArrowLeft
} from 'lucide-vue-next'
</script>

<style scoped>
.terms {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  padding: 2rem 1rem;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  padding: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 3rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #f0fdf4;
}

.header-icon {
  color: #16a34a;
  margin-bottom: 1rem;
}

.header h1 {
  font-size: 2.5rem;
  color: #064e3b;
  margin-bottom: 0.5rem;
}

.updated {
  color: #6b7280;
  font-size: 0.9rem;
}

/* Sections */
.section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  color: #064e3b;
}

.section-header svg {
  color: #16a34a;
  flex-shrink: 0;
}

.section h2 {
  font-size: 1.75rem;
  color: #064e3b;
  margin: 0;
}

.intro {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #374151;
}

.section p {
  line-height: 1.8;
  color: #4b5563;
  margin-bottom: 1rem;
}

/* Info Boxes */
.info-box {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  border-radius: 12px;
  margin-top: 1.5rem;
}

.info-box.success {
  background: #f0fdf4;
  border-left: 4px solid #16a34a;
}

.info-box.success svg {
  color: #16a34a;
}

.info-box.warning {
  background: #fffbeb;
  border-left: 4px solid #f59e0b;
}

.info-box.warning svg {
  color: #f59e0b;
  flex-shrink: 0;
}

.info-box.error {
  background: #fef2f2;
  border-left: 4px solid #ef4444;
}

.info-box.error svg {
  color: #ef4444;
  flex-shrink: 0;
}

.info-box h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}

.info-box p {
  margin-bottom: 0.75rem;
}

.info-box ul {
  list-style: disc;
  padding-left: 1.5rem;
  margin: 0;
}

.info-box li {
  margin-bottom: 0.5rem;
}

/* Service List */
.service-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 1.5rem;
}

.service-item {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: #f0fdf4;
  border-radius: 8px;
  border: 1px solid #dcfce7;
}

.service-item svg {
  color: #16a34a;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.service-item h4 {
  color: #064e3b;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.service-item p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

/* Subsections */
.subsection {
  margin-bottom: 2rem;
}

.subsection h3 {
  color: #064e3b;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.check-list {
  list-style: none;
  padding: 0;
}

.check-list li {
  padding: 0.75rem 0;
  padding-left: 2rem;
  position: relative;
  line-height: 1.6;
  color: #4b5563;
}

.check-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #16a34a;
  font-weight: bold;
  font-size: 1.2rem;
}

.x-list {
  list-style: none;
  padding: 0;
}

.x-list li {
  padding: 0.75rem 0;
  padding-left: 2rem;
  position: relative;
  line-height: 1.6;
  color: #4b5563;
}

.x-list li::before {
  content: '✕';
  position: absolute;
  left: 0;
  color: #ef4444;
  font-weight: bold;
  font-size: 1.2rem;
}

/* Disclaimer Points */
.disclaimer-points {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.disclaimer-point {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border-left: 4px solid #16a34a;
}

.disclaimer-point .number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #16a34a;
  color: white;
  border-radius: 50%;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.disclaimer-point h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.disclaimer-point p {
  color: #6b7280;
  margin: 0;
}

/* IP Grid */
.ip-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.ip-card {
  text-align: center;
  padding: 1.5rem;
  background: #f0fdf4;
  border-radius: 12px;
  border: 2px solid #dcfce7;
  transition: all 0.3s ease;
}

.ip-card:hover {
  border-color: #16a34a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.1);
}

.ip-card svg {
  color: #16a34a;
  margin: 0 auto 0.75rem;
}

.ip-card h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.ip-card p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

/* Content Terms */
.content-terms {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 1.5rem;
}

.term-item {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: #f9fafb;
  border-radius: 8px;
}

.term-item svg {
  color: #16a34a;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.term-item h4 {
  color: #064e3b;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.term-item p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

/* Lists */
.liability-list,
.termination-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.liability-list li,
.termination-list li {
  padding: 0.75rem 0;
  padding-left: 2rem;
  position: relative;
  line-height: 1.6;
  color: #4b5563;
}

.liability-list li::before,
.termination-list li::before {
  content: '•';
  position: absolute;
  left: 0.5rem;
  color: #16a34a;
  font-weight: bold;
  font-size: 1.5rem;
}

/* Availability Grid */
.availability-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.availability-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.availability-item svg {
  color: #16a34a;
  flex-shrink: 0;
}

.availability-item p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

/* Contact Box */
.contact-box {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: #f0fdf4;
  border-radius: 12px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.contact-item svg {
  color: #16a34a;
}

.contact-item a {
  color: #16a34a;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.contact-item a:hover {
  color: #15803d;
  text-decoration: underline;
}

/* Back Link */
.back-link {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid #f0fdf4;
  text-align: center;
}

.back-link a {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #16a34a;
  text-decoration: none;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.back-link a:hover {
  background: #f0fdf4;
  color: #15803d;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 2rem 1.5rem;
  }

  .header h1 {
    font-size: 2rem;
  }

  .section h2 {
    font-size: 1.5rem;
  }

  .ip-grid,
  .availability-grid {
    grid-template-columns: 1fr;
  }

  .info-box,
  .disclaimer-point {
    flex-direction: column;
  }

  .disclaimer-point .number {
    margin: 0 auto;
  }
}
</style>
