<template>
  <footer class="app-footer">
    <div class="footer-container">
      <!-- Footer Main Content -->
      <div class="footer-main">
        <!-- Column 1 -->
        <div class="footer-section">
          <h4 class="footer-title">Produk</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/detection" class="footer-link">Deteksi Penyakit</router-link>
            </li>
            <li>
              <router-link to="/history" class="footer-link">Riwayat</router-link>
            </li>
          </ul>
        </div>

        <!-- Column 2 -->
        <div class="footer-section">
          <h4 class="footer-title">Bantuan</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/guide" class="footer-link">Panduan</router-link>
            </li>
            <li>
              <router-link to="/faq" class="footer-link">FAQ</router-link>
            </li>
          </ul>
        </div>

        <!-- Column 3 -->
        <div class="footer-section">
          <h4 class="footer-title">Perusahaan</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/" class="footer-link">Tentang Kami</router-link>
            </li>
          </ul>
        </div>

        <!-- Column 4 -->
        <div class="footer-section">
          <h4 class="footer-title">Legal</h4>
          <ul class="footer-links">
            <li>
              <router-link to="/privacy-policy" class="footer-link">Privasi</router-link>
            </li>
            <li>
              <router-link to="/terms" class="footer-link">Syarat</router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- Footer Bottom -->
      <div class="footer-bottom">
        <div class="footer-bottom-content">
          <p class="copyright">
            © {{ currentYear }} Grovia. All rights reserved.
          </p>
          <div class="social-links">
            <a href="https://facebook.com" target="_blank" rel="noopener" class="social-link" aria-label="Facebook">
              <Facebook :size="16" />
            </a>
            <a href="https://twitter.com" target="_blank" rel="noopener" class="social-link" aria-label="Twitter">
              <Twitter :size="16" />
            </a>
            <a href="https://instagram.com" target="_blank" rel="noopener" class="social-link" aria-label="Instagram">
              <Instagram :size="16" />
            </a>
            <a href="https://youtube.com" target="_blank" rel="noopener" class="social-link" aria-label="YouTube">
              <Youtube :size="16" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';
import {
  Leaf,
  Facebook,
  Twitter,
  Instagram,
  Youtube,
  Mail,
  Phone,
  MapPin
} from 'lucide-vue-next';

const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.app-footer {
  background: #5a9470;
  color: rgba(255, 255, 255, 0.85);
  margin-top: auto;
}

.footer-container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 48px 40px 24px;
}

/* Footer Main */
.footer-main {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 48px;
  margin-bottom: 40px;
  padding-bottom: 40px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.footer-section {
  display: flex;
  flex-direction: column;
}

/* Footer Titles */
.footer-title {
  font-size: 13px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #ffffff;
  letter-spacing: 0;
  text-transform: none;
}

/* Footer Links */
.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-link {
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  font-size: 13px;
  transition: color 0.2s ease;
  display: inline-block;
  font-weight: 400;
}

.footer-link:hover {
  color: #ffffff;
}

/* Footer Bottom */
.footer-bottom {
  padding: 0;
}

.footer-bottom-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.copyright {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
  font-weight: 400;
}

/* Social Links */
.social-links {
  display: flex;
  gap: 12px;
}

.social-link {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  text-decoration: none;
  transition: all 0.2s ease;
  color: rgba(255, 255, 255, 0.85);
}

.social-link:hover {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

/* Responsive */
@media (max-width: 1024px) {
  .footer-main {
    grid-template-columns: repeat(2, 1fr);
    gap: 32px;
  }
}

@media (max-width: 640px) {
  .footer-container {
    padding: 40px 20px 20px;
  }

  .footer-main {
    grid-template-columns: 1fr;
    gap: 28px;
    margin-bottom: 32px;
    padding-bottom: 32px;
  }

  .footer-bottom-content {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }

  .social-links {
    justify-content: center;
  }
}
</style>
