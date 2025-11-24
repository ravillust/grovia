<template>
  <div class="privacy-policy">
    <div class="container">
      <!-- Header -->
      <div class="header">
        <Shield :size="48" class="header-icon" />
        <h1>Kebijakan Privasi</h1>
        <p class="updated">Terakhir diperbarui: 31 Oktober 2025</p>
      </div>

      <!-- Introduction -->
      <section class="section">
        <p class="intro">
          Grovia berkomitmen untuk melindungi privasi Anda. Kebijakan Privasi ini menjelaskan bagaimana kami mengumpulkan, 
          menggunakan, dan melindungi informasi pribadi Anda saat menggunakan layanan deteksi penyakit tanaman kami.
        </p>
      </section>

      <!-- Information We Collect -->
      <section class="section">
        <div class="section-header">
          <FileText :size="24" />
          <h2>Informasi yang Kami Kumpulkan</h2>
        </div>
        
        <div class="subsection">
          <h3>1. Informasi Akun</h3>
          <ul>
            <li><strong>Email:</strong> Digunakan untuk autentikasi dan komunikasi</li>
            <li><strong>Nama:</strong> Untuk personalisasi pengalaman Anda</li>
            <li><strong>Kata Sandi:</strong> Disimpan dalam bentuk terenkripsi (hashed)</li>
          </ul>
        </div>

        <div class="subsection">
          <h3>2. Data Deteksi</h3>
          <ul>
            <li><strong>Foto Tanaman:</strong> Gambar yang Anda unggah untuk analisis penyakit</li>
            <li><strong>Hasil Deteksi:</strong> Output dari model AI termasuk jenis penyakit dan tingkat kepercayaan</li>
            <li><strong>Metadata:</strong> Waktu deteksi, status, dan informasi teknis lainnya</li>
          </ul>
        </div>

        <div class="subsection">
          <h3>3. Informasi Teknis</h3>
          <ul>
            <li><strong>Token Autentikasi:</strong> Disimpan di localStorage browser untuk menjaga sesi login</li>
            <li><strong>Preferensi Pengguna:</strong> Pengaturan aplikasi yang Anda pilih</li>
            <li><strong>Riwayat Penggunaan:</strong> Log aktivitas untuk meningkatkan layanan</li>
          </ul>
        </div>
      </section>

      <!-- How We Use Information -->
      <section class="section">
        <div class="section-header">
          <Settings :size="24" />
          <h2>Bagaimana Kami Menggunakan Informasi Anda</h2>
        </div>
        
        <div class="usage-grid">
          <div class="usage-card">
            <Target :size="20" />
            <h4>Menyediakan Layanan</h4>
            <p>Memproses gambar Anda dan memberikan hasil deteksi penyakit tanaman yang akurat</p>
          </div>
          
          <div class="usage-card">
            <BarChart3 :size="20" />
            <h4>Meningkatkan Kualitas</h4>
            <p>Menganalisis data untuk meningkatkan akurasi model AI dan pengalaman pengguna</p>
          </div>
          
          <div class="usage-card">
            <Bell :size="20" />
            <h4>Komunikasi</h4>
            <p>Mengirim notifikasi penting tentang akun dan pembaruan layanan</p>
          </div>
          
          <div class="usage-card">
            <Lock :size="20" />
            <h4>Keamanan</h4>
            <p>Melindungi akun Anda dari akses tidak sah dan aktivitas mencurigakan</p>
          </div>
        </div>
      </section>

      <!-- Data Storage -->
      <section class="section">
        <div class="section-header">
          <Database :size="24" />
          <h2>Penyimpanan Data</h2>
        </div>
        
        <div class="storage-info">
          <div class="storage-item">
            <div class="storage-icon cloud">
              <Cloud :size="32" />
            </div>
            <div class="storage-content">
              <h4>Penyimpanan Cloud</h4>
              <p>Data akun dan riwayat deteksi disimpan di server kami yang aman dengan enkripsi standar industri.</p>
            </div>
          </div>
          
          <div class="storage-item">
            <div class="storage-icon local">
              <HardDrive :size="32" />
            </div>
            <div class="storage-content">
              <h4>Penyimpanan Lokal</h4>
              <p>Token autentikasi dan preferensi disimpan di localStorage browser Anda untuk kemudahan akses.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Your Rights -->
      <section class="section">
        <div class="section-header">
          <UserCheck :size="24" />
          <h2>Hak-Hak Anda</h2>
        </div>
        
        <div class="rights-list">
          <div class="right-item">
            <Eye :size="20" />
            <div>
              <h4>Akses Data</h4>
              <p>Anda berhak mengakses semua data pribadi yang kami simpan tentang Anda</p>
            </div>
          </div>
          
          <div class="right-item">
            <Edit :size="20" />
            <div>
              <h4>Koreksi Data</h4>
              <p>Anda dapat memperbarui atau memperbaiki informasi akun Anda kapan saja</p>
            </div>
          </div>
          
          <div class="right-item">
            <Trash2 :size="20" />
            <div>
              <h4>Hapus Data</h4>
              <p>Anda dapat menghapus akun dan semua data terkait dengan menghubungi kami</p>
            </div>
          </div>
          
          <div class="right-item">
            <Download :size="20" />
            <div>
              <h4>Portabilitas Data</h4>
              <p>Anda dapat meminta salinan data Anda dalam format yang dapat dibaca mesin</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Data Security -->
      <section class="section">
        <div class="section-header">
          <ShieldCheck :size="24" />
          <h2>Keamanan Data</h2>
        </div>
        
        <p>Kami menerapkan berbagai langkah keamanan untuk melindungi informasi Anda:</p>
        
        <div class="security-measures">
          <div class="measure">
            <div class="measure-icon">🔐</div>
            <h4>Enkripsi</h4>
            <p>Semua data sensitif dienkripsi saat transit (HTTPS) dan saat disimpan</p>
          </div>
          
          <div class="measure">
            <div class="measure-icon">🛡️</div>
            <h4>Hashing Kata Sandi</h4>
            <p>Kata sandi tidak pernah disimpan dalam bentuk teks biasa, hanya hash-nya</p>
          </div>
          
          <div class="measure">
            <div class="measure-icon">🔒</div>
            <h4>Akses Terbatas</h4>
            <p>Hanya personel yang berwenang yang dapat mengakses data pengguna</p>
          </div>
          
          <div class="measure">
            <div class="measure-icon">📊</div>
            <h4>Monitoring</h4>
            <p>Sistem kami dipantau 24/7 untuk mendeteksi aktivitas mencurigakan</p>
          </div>
        </div>
      </section>

      <!-- Data Sharing -->
      <section class="section">
        <div class="section-header">
          <Share2 :size="24" />
          <h2>Pembagian Data</h2>
        </div>
        
        <div class="info-box">
          <AlertCircle :size="24" />
          <div>
            <h4>Kami TIDAK menjual data Anda</h4>
            <p>
              Grovia tidak akan pernah menjual, menyewakan, atau membagikan informasi pribadi Anda kepada pihak ketiga 
              untuk tujuan pemasaran. Data Anda hanya dibagikan dalam kondisi berikut:
            </p>
            <ul>
              <li>Dengan persetujuan eksplisit Anda</li>
              <li>Untuk mematuhi kewajiban hukum</li>
              <li>Dengan penyedia layanan yang membantu operasi kami (dengan perjanjian kerahasiaan ketat)</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Data Retention -->
      <section class="section">
        <div class="section-header">
          <Clock :size="24" />
          <h2>Penyimpanan Data</h2>
        </div>
        
        <p>Kami menyimpan data Anda selama:</p>
        <ul>
          <li><strong>Data Akun:</strong> Selama akun Anda aktif atau sesuai kebutuhan untuk menyediakan layanan</li>
          <li><strong>Riwayat Deteksi:</strong> Hingga Anda menghapusnya atau menutup akun</li>
          <li><strong>Log Sistem:</strong> Maksimal 90 hari untuk tujuan keamanan dan troubleshooting</li>
        </ul>
        <p>
          Setelah Anda menghapus akun, kami akan menghapus atau menganonimkan data Anda dalam waktu 30 hari, 
          kecuali diwajibkan oleh hukum untuk menyimpannya lebih lama.
        </p>
      </section>

      <!-- Cookies and Tracking -->
      <section class="section">
        <div class="section-header">
          <Cookie :size="24" />
          <h2>Cookie dan Pelacakan</h2>
        </div>
        
        <p>
          Grovia menggunakan localStorage browser untuk menyimpan token autentikasi dan preferensi pengguna. 
          Kami tidak menggunakan cookie pihak ketiga untuk pelacakan atau iklan. 
          Untuk informasi lebih lanjut, lihat <router-link to="/cookies">Kebijakan Cookie</router-link> kami.
        </p>
      </section>

      <!-- Children's Privacy -->
      <section class="section">
        <div class="section-header">
          <Users :size="24" />
          <h2>Privasi Anak-anak</h2>
        </div>
        
        <p>
          Layanan kami tidak ditujukan untuk anak-anak di bawah 13 tahun. Kami tidak secara sadar mengumpulkan 
          informasi pribadi dari anak-anak. Jika Anda adalah orang tua atau wali dan mengetahui bahwa anak Anda 
          telah memberikan informasi pribadi kepada kami, silakan hubungi kami untuk menghapusnya.
        </p>
      </section>

      <!-- Changes to Policy -->
      <section class="section">
        <div class="section-header">
          <RefreshCw :size="24" />
          <h2>Perubahan Kebijakan</h2>
        </div>
        
        <p>
          Kami dapat memperbarui Kebijakan Privasi ini dari waktu ke waktu. Perubahan signifikan akan kami beritahukan 
          melalui email atau notifikasi di aplikasi. Kami mendorong Anda untuk meninjau halaman ini secara berkala 
          untuk informasi terbaru tentang praktik privasi kami.
        </p>
      </section>

      <!-- Contact -->
      <section class="section">
        <div class="section-header">
          <Mail :size="24" />
          <h2>Hubungi Kami</h2>
        </div>
        
        <p>
          Jika Anda memiliki pertanyaan, kekhawatiran, atau permintaan terkait Kebijakan Privasi ini atau 
          cara kami menangani data Anda, silakan hubungi kami:
        </p>
        
        <div class="contact-box">
          <div class="contact-item">
            <Mail :size="20" />
            <a href="mailto:privacy@grovia.com">privacy@grovia.com</a>
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
  Shield, FileText, Settings, Target, BarChart3, Bell, Lock, 
  Database, Cloud, HardDrive, UserCheck, Eye, Edit, Trash2, Download,
  ShieldCheck, Share2, AlertCircle, Clock, Cookie, Users, RefreshCw,
  Mail, MessageCircle, ArrowLeft
} from 'lucide-vue-next'
</script>

<style scoped>
.privacy-policy {
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

/* Subsections */
.subsection {
  margin-bottom: 2rem;
}

.subsection h3 {
  color: #064e3b;
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.subsection ul {
  list-style: none;
  padding: 0;
}

.subsection li {
  padding: 0.75rem 0;
  padding-left: 1.5rem;
  position: relative;
  line-height: 1.6;
  color: #4b5563;
}

.subsection li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: #16a34a;
  font-weight: bold;
}

.subsection strong {
  color: #064e3b;
}

/* Usage Grid */
.usage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.usage-card {
  padding: 1.5rem;
  background: #f0fdf4;
  border-radius: 12px;
  border: 2px solid #dcfce7;
  transition: all 0.3s ease;
}

.usage-card:hover {
  border-color: #16a34a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.1);
}

.usage-card svg {
  color: #16a34a;
  margin-bottom: 0.75rem;
}

.usage-card h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.usage-card p {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Storage Info */
.storage-info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.storage-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border-left: 4px solid #16a34a;
}

.storage-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
}

.storage-icon.cloud {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1e40af;
}

.storage-icon.local {
  background: linear-gradient(135deg, #fce7f3, #fbcfe8);
  color: #be185d;
}

.storage-content h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.storage-content p {
  color: #6b7280;
  line-height: 1.6;
}

/* Rights List */
.rights-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 1.5rem;
}

.right-item {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: #f0fdf4;
  border-radius: 8px;
  border: 1px solid #dcfce7;
}

.right-item svg {
  color: #16a34a;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.right-item h4 {
  color: #064e3b;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.right-item p {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Security Measures */
.security-measures {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.measure {
  text-align: center;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
}

.measure:hover {
  border-color: #16a34a;
  transform: translateY(-2px);
}

.measure-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.measure h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.measure p {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* Info Box */
.info-box {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #fffbeb;
  border-radius: 12px;
  border-left: 4px solid #f59e0b;
  margin-top: 1.5rem;
}

.info-box svg {
  color: #f59e0b;
  flex-shrink: 0;
}

.info-box h4 {
  color: #92400e;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.info-box p {
  color: #78350f;
  line-height: 1.6;
  margin-bottom: 0.75rem;
}

.info-box ul {
  list-style: disc;
  padding-left: 1.5rem;
  color: #78350f;
}

.info-box li {
  margin-bottom: 0.5rem;
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

  .usage-grid,
  .security-measures {
    grid-template-columns: 1fr;
  }

  .storage-item {
    flex-direction: column;
    text-align: center;
  }

  .storage-icon {
    margin: 0 auto;
  }

  .info-box {
    flex-direction: column;
  }
}
</style>
