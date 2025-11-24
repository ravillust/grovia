<template>
  <div class="cookie-policy">
    <div class="container">
      <!-- Header -->
      <div class="header">
        <Cookie :size="48" class="header-icon" />
        <h1>Kebijakan Cookie</h1>
        <p class="updated">Terakhir diperbarui: 31 Oktober 2025</p>
      </div>

      <!-- Introduction -->
      <section class="section">
        <p class="intro">
          Grovia menggunakan teknologi penyimpanan lokal (localStorage) di browser Anda untuk menyediakan 
          pengalaman yang lebih baik dan menjaga sesi login Anda. Kebijakan ini menjelaskan bagaimana kami 
          menggunakan teknologi penyimpanan ini.
        </p>
      </section>

      <!-- What We Use -->
      <section class="section">
        <div class="section-header">
          <Info :size="24" />
          <h2>Apa yang Kami Gunakan</h2>
        </div>
        
        <div class="info-box">
          <HardDrive :size="24" />
          <div>
            <h4>LocalStorage, Bukan Cookie Tradisional</h4>
            <p>
              Grovia menggunakan <strong>localStorage</strong> (HTML5 Web Storage) alih-alih cookie tradisional. 
              localStorage memungkinkan kami menyimpan data di browser Anda secara lokal, dengan keamanan yang lebih baik 
              dan tidak dikirim ke server pada setiap permintaan HTTP.
            </p>
          </div>
        </div>

        <div class="comparison">
          <h3>Perbedaan LocalStorage dan Cookie:</h3>
          <div class="comparison-grid">
            <div class="comparison-card local">
              <Check :size="24" />
              <h4>LocalStorage (Yang Kami Gunakan)</h4>
              <ul>
                <li>Data disimpan hanya di browser Anda</li>
                <li>Tidak dikirim ke server secara otomatis</li>
                <li>Kapasitas penyimpanan lebih besar (5-10MB)</li>
                <li>Hanya dapat diakses melalui JavaScript</li>
                <li>Tidak memiliki tanggal kedaluwarsa otomatis</li>
              </ul>
            </div>

            <div class="comparison-card cookie">
              <X :size="24" />
              <h4>Cookie (Tidak Kami Gunakan)</h4>
              <ul>
                <li>Data dikirim ke server pada setiap request</li>
                <li>Dapat digunakan untuk pelacakan</li>
                <li>Kapasitas terbatas (~4KB)</li>
                <li>Dapat diakses oleh server dan JavaScript</li>
                <li>Memiliki tanggal kedaluwarsa</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- What We Store -->
      <section class="section">
        <div class="section-header">
          <Database :size="24" />
          <h2>Data yang Kami Simpan</h2>
        </div>

        <div class="storage-list">
          <div class="storage-item">
            <div class="item-header">
              <Key :size="20" />
              <h4>Token Autentikasi</h4>
              <span class="badge essential">Penting</span>
            </div>
            <div class="item-details">
              <p><strong>Tujuan:</strong> Menjaga Anda tetap login tanpa harus memasukkan kredensial setiap kali</p>
              <p><strong>Durasi:</strong> Sampai Anda logout atau token kedaluwarsa</p>
              <p><strong>Dapat Dihapus:</strong> Ya, dengan logout atau clear browser data</p>
            </div>
          </div>

          <div class="storage-item">
            <div class="item-header">
              <User :size="20" />
              <h4>Informasi Pengguna</h4>
              <span class="badge essential">Penting</span>
            </div>
            <div class="item-details">
              <p><strong>Tujuan:</strong> Menampilkan nama, email, dan preferensi Anda di aplikasi</p>
              <p><strong>Durasi:</strong> Sampai Anda logout</p>
              <p><strong>Dapat Dihapus:</strong> Ya, dengan logout atau clear browser data</p>
            </div>
          </div>

          <div class="storage-item">
            <div class="item-header">
              <Settings :size="20" />
              <h4>Preferensi Aplikasi</h4>
              <span class="badge functional">Fungsional</span>
            </div>
            <div class="item-details">
              <p><strong>Tujuan:</strong> Menyimpan pengaturan UI, tema, atau preferensi tampilan</p>
              <p><strong>Durasi:</strong> Permanen sampai Anda mengubah atau menghapusnya</p>
              <p><strong>Dapat Dihapus:</strong> Ya, melalui pengaturan atau clear browser data</p>
            </div>
          </div>

          <div class="storage-item">
            <div class="item-header">
              <History :size="20" />
              <h4>Cache Sementara</h4>
              <span class="badge functional">Fungsional</span>
            </div>
            <div class="item-details">
              <p><strong>Tujuan:</strong> Menyimpan data sementara untuk meningkatkan kecepatan aplikasi</p>
              <p><strong>Durasi:</strong> Sampai kedaluwarsa atau browser cache dibersihkan</p>
              <p><strong>Dapat Dihapus:</strong> Ya, otomatis atau manual melalui clear browser data</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Purpose -->
      <section class="section">
        <div class="section-header">
          <Target :size="24" />
          <h2>Tujuan Penggunaan</h2>
        </div>

        <div class="purpose-grid">
          <div class="purpose-card">
            <div class="purpose-icon auth">
              <Lock :size="28" />
            </div>
            <h4>Autentikasi</h4>
            <p>Menjaga sesi login Anda agar tidak perlu login berulang kali</p>
          </div>

          <div class="purpose-card">
            <div class="purpose-icon ux">
              <Sparkles :size="28" />
            </div>
            <h4>Pengalaman Pengguna</h4>
            <p>Mengingat preferensi Anda untuk pengalaman yang personal</p>
          </div>

          <div class="purpose-card">
            <div class="purpose-icon perf">
              <Zap :size="28" />
            </div>
            <h4>Performa</h4>
            <p>Menyimpan data cache untuk loading yang lebih cepat</p>
          </div>

          <div class="purpose-card">
            <div class="purpose-icon secure">
              <ShieldCheck :size="28" />
            </div>
            <h4>Keamanan</h4>
            <p>Menyimpan token dengan aman untuk akses yang terproteksi</p>
          </div>
        </div>
      </section>

      <!-- No Third-Party -->
      <section class="section">
        <div class="section-header">
          <ShieldOff :size="24" />
          <h2>Tidak Ada Pelacakan Pihak Ketiga</h2>
        </div>

        <div class="info-box success">
          <CheckCircle :size="24" />
          <div>
            <h4>Privasi Anda Terlindungi</h4>
            <p>
              Grovia <strong>TIDAK menggunakan</strong> cookie pihak ketiga untuk pelacakan, iklan, atau analitik. 
              Semua data disimpan secara lokal di perangkat Anda dan hanya digunakan untuk fungsionalitas aplikasi.
            </p>
            <ul>
              <li>❌ Tidak ada Google Analytics</li>
              <li>❌ Tidak ada Facebook Pixel</li>
              <li>❌ Tidak ada tracking script pihak ketiga</li>
              <li>❌ Tidak ada iklan bertarget</li>
              <li>✅ 100% kontrol data ada di tangan Anda</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- How to Manage -->
      <section class="section">
        <div class="section-header">
          <Sliders :size="24" />
          <h2>Cara Mengelola Penyimpanan Lokal</h2>
        </div>

        <p>Anda memiliki kontrol penuh atas data yang disimpan di browser Anda. Berikut cara mengelolanya:</p>

        <div class="manage-tabs">
          <div class="manage-option">
            <div class="option-number">1</div>
            <div class="option-content">
              <h4>Logout dari Aplikasi</h4>
              <p>
                Cara termudah untuk menghapus token autentikasi dan data sesi. Klik tombol logout di menu pengguna.
              </p>
              <div class="code-block">
                Menu Pengguna → Logout
              </div>
            </div>
          </div>

          <div class="manage-option">
            <div class="option-number">2</div>
            <div class="option-content">
              <h4>Clear Browser Data (Chrome)</h4>
              <p>
                Menghapus semua data localStorage untuk Grovia atau semua website:
              </p>
              <div class="code-block">
                Settings → Privacy and Security → Clear Browsing Data → 
                Centang "Cookies and site data" → Clear Data
              </div>
            </div>
          </div>

          <div class="manage-option">
            <div class="option-number">3</div>
            <div class="option-content">
              <h4>Developer Tools (Manual)</h4>
              <p>
                Untuk pengguna advanced, Anda dapat menghapus item localStorage secara spesifik:
              </p>
              <div class="code-block">
                F12 (DevTools) → Application tab → Local Storage → 
                Pilih domain Grovia → Hapus item yang diinginkan
              </div>
            </div>
          </div>

          <div class="manage-option">
            <div class="option-number">4</div>
            <div class="option-content">
              <h4>Private/Incognito Mode</h4>
              <p>
                Gunakan mode penyamaran untuk sesi tanpa penyimpanan permanen. Data akan terhapus saat Anda menutup browser.
              </p>
              <div class="code-block">
                Chrome: Ctrl+Shift+N | Firefox: Ctrl+Shift+P
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Data Security -->
      <section class="section">
        <div class="section-header">
          <Lock :size="24" />
          <h2>Keamanan Data</h2>
        </div>

        <p>Kami menerapkan praktik keamanan terbaik untuk melindungi data di localStorage:</p>

        <div class="security-list">
          <div class="security-item">
            <ShieldCheck :size="20" />
            <div>
              <h4>Enkripsi Token</h4>
              <p>Token autentikasi dienkripsi sebelum disimpan di localStorage</p>
            </div>
          </div>

          <div class="security-item">
            <Clock :size="20" />
            <div>
              <h4>Expiry Time</h4>
              <p>Token memiliki waktu kedaluwarsa untuk mencegah akses tidak sah jangka panjang</p>
            </div>
          </div>

          <div class="security-item">
            <Eye :size="20" />
            <div>
              <h4>Same-Origin Policy</h4>
              <p>Data localStorage hanya dapat diakses oleh domain Grovia, bukan website lain</p>
            </div>
          </div>

          <div class="security-item">
            <AlertTriangle :size="20" />
            <div>
              <h4>Sensitive Data</h4>
              <p>Kami tidak pernah menyimpan password atau data sensitif lainnya di localStorage</p>
            </div>
          </div>
        </div>

        <div class="info-box warning">
          <AlertTriangle :size="24" />
          <div>
            <h4>Peringatan Komputer Publik</h4>
            <p>
              Jika Anda menggunakan komputer publik atau bersama, pastikan untuk <strong>logout</strong> setelah selesai. 
              Jangan centang "Remember Me" pada perangkat yang tidak Anda percayai.
            </p>
          </div>
        </div>
      </section>

      <!-- Your Rights -->
      <section class="section">
        <div class="section-header">
          <UserCheck :size="24" />
          <h2>Hak Anda</h2>
        </div>

        <div class="rights-grid">
          <div class="right-card">
            <Eye :size="24" />
            <h4>Lihat Data</h4>
            <p>Anda dapat melihat semua data yang disimpan melalui browser DevTools</p>
          </div>

          <div class="right-card">
            <Trash2 :size="24" />
            <h4>Hapus Data</h4>
            <p>Anda dapat menghapus semua data kapan saja dengan logout atau clear browser data</p>
          </div>

          <div class="right-card">
            <XCircle :size="24" />
            <h4>Tolak Penyimpanan</h4>
            <p>Anda dapat menonaktifkan localStorage di browser, namun aplikasi mungkin tidak berfungsi penuh</p>
          </div>

          <div class="right-card">
            <Download :size="24" />
            <h4>Export Data</h4>
            <p>Anda dapat mengekspor data localStorage untuk backup atau portabilitas</p>
          </div>
        </div>
      </section>

      <!-- Updates -->
      <section class="section">
        <div class="section-header">
          <RefreshCw :size="24" />
          <h2>Pembaruan Kebijakan</h2>
        </div>

        <p>
          Jika ada perubahan signifikan pada cara kami menggunakan localStorage atau teknologi penyimpanan lainnya, 
          kami akan memperbarui kebijakan ini dan memberi tahu Anda melalui notifikasi di aplikasi atau email.
        </p>
      </section>

      <!-- Related Policies -->
      <section class="section">
        <div class="section-header">
          <FileText :size="24" />
          <h2>Kebijakan Terkait</h2>
        </div>

        <div class="related-links">
          <router-link to="/privacy" class="related-card">
            <Shield :size="24" />
            <div>
              <h4>Kebijakan Privasi</h4>
              <p>Bagaimana kami mengumpulkan dan menggunakan data Anda</p>
            </div>
            <ArrowRight :size="20" />
          </router-link>

          <router-link to="/terms" class="related-card">
            <FileCheck :size="24" />
            <div>
              <h4>Syarat & Ketentuan</h4>
              <p>Aturan penggunaan layanan Grovia</p>
            </div>
            <ArrowRight :size="20" />
          </router-link>
        </div>
      </section>

      <!-- Contact -->
      <section class="section">
        <div class="section-header">
          <Mail :size="24" />
          <h2>Pertanyaan?</h2>
        </div>

        <p>Jika Anda memiliki pertanyaan tentang penggunaan localStorage atau kebijakan ini, hubungi kami:</p>

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
  Cookie, Info, HardDrive, Check, X, Database, Key, User, Settings, History,
  Target, Lock, Sparkles, Zap, ShieldCheck, ShieldOff, CheckCircle, Sliders,
  Clock, Eye, AlertTriangle, UserCheck, Trash2, XCircle, Download, RefreshCw,
  FileText, Shield, FileCheck, ArrowRight, Mail, MessageCircle, ArrowLeft
} from 'lucide-vue-next'
</script>

<style scoped>
.cookie-policy {
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

.info-box svg {
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
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.info-box li {
  padding: 0.25rem 0;
}

.info-box:not(.success):not(.warning) {
  background: #f0f9ff;
  border-left: 4px solid #3b82f6;
}

.info-box:not(.success):not(.warning) svg {
  color: #3b82f6;
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
}

/* Comparison */
.comparison {
  margin-top: 2rem;
}

.comparison h3 {
  color: #064e3b;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.comparison-card {
  padding: 1.5rem;
  border-radius: 12px;
  border: 2px solid;
}

.comparison-card svg {
  margin-bottom: 0.75rem;
}

.comparison-card h4 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.comparison-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.comparison-card li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
  line-height: 1.5;
  font-size: 0.9rem;
}

.comparison-card li::before {
  content: '•';
  position: absolute;
  left: 0;
  font-weight: bold;
}

.comparison-card.local {
  background: #f0fdf4;
  border-color: #16a34a;
}

.comparison-card.local svg {
  color: #16a34a;
}

.comparison-card.local h4 {
  color: #064e3b;
}

.comparison-card.local li {
  color: #166534;
}

.comparison-card.cookie {
  background: #fef2f2;
  border-color: #ef4444;
}

.comparison-card.cookie svg {
  color: #ef4444;
}

.comparison-card.cookie h4 {
  color: #991b1b;
}

.comparison-card.cookie li {
  color: #7f1d1d;
}

/* Storage List */
.storage-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.storage-item {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border-left: 4px solid #16a34a;
}

.item-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.item-header svg {
  color: #16a34a;
}

.item-header h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin: 0;
  flex: 1;
}

.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.essential {
  background: #dcfce7;
  color: #166534;
}

.badge.functional {
  background: #dbeafe;
  color: #1e40af;
}

.item-details p {
  color: #6b7280;
  font-size: 0.9rem;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.item-details strong {
  color: #374151;
}

/* Purpose Grid */
.purpose-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.purpose-card {
  text-align: center;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
}

.purpose-card:hover {
  border-color: #16a34a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.1);
}

.purpose-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.purpose-icon.auth {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1e40af;
}

.purpose-icon.ux {
  background: linear-gradient(135deg, #fce7f3, #fbcfe8);
  color: #be185d;
}

.purpose-icon.perf {
  background: linear-gradient(135deg, #fef9c3, #fde047);
  color: #a16207;
}

.purpose-icon.secure {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  color: #166534;
}

.purpose-card h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.purpose-card p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

/* Manage Options */
.manage-tabs {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.manage-option {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.option-number {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #16a34a;
  color: white;
  border-radius: 50%;
  font-weight: bold;
  font-size: 1.2rem;
}

.option-content h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.75rem;
}

.option-content p {
  color: #6b7280;
  margin-bottom: 0.75rem;
}

.code-block {
  padding: 1rem;
  background: #1f2937;
  color: #86efac;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
  overflow-x: auto;
}

/* Security List */
.security-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 1.5rem;
}

.security-item {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background: #f0fdf4;
  border-radius: 8px;
  border: 1px solid #dcfce7;
}

.security-item svg {
  color: #16a34a;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.security-item h4 {
  color: #064e3b;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.security-item p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

/* Rights Grid */
.rights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.right-card {
  text-align: center;
  padding: 1.5rem;
  background: #f0fdf4;
  border-radius: 12px;
  border: 2px solid #dcfce7;
  transition: all 0.3s ease;
}

.right-card:hover {
  border-color: #16a34a;
  transform: translateY(-2px);
}

.right-card svg {
  color: #16a34a;
  margin: 0 auto 0.75rem;
}

.right-card h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.right-card p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

/* Related Links */
.related-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
}

.related-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #f0fdf4;
  border-radius: 12px;
  border: 2px solid #dcfce7;
  text-decoration: none;
  transition: all 0.3s ease;
}

.related-card:hover {
  border-color: #16a34a;
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.1);
}

.related-card svg:first-child {
  color: #16a34a;
  flex-shrink: 0;
}

.related-card > div {
  flex: 1;
}

.related-card h4 {
  color: #064e3b;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.related-card p {
  color: #6b7280;
  font-size: 0.9rem;
  margin: 0;
}

.related-card svg:last-child {
  color: #16a34a;
  flex-shrink: 0;
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

  .comparison-grid,
  .purpose-grid,
  .rights-grid {
    grid-template-columns: 1fr;
  }

  .info-box,
  .manage-option {
    flex-direction: column;
  }

  .option-number {
    margin: 0 auto;
  }
}
</style>
