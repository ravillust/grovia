<template>
  <div class="faq-view">
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1 class="page-title">Pertanyaan yang Sering Diajukan (FAQ)</h1>
        <p class="page-description">
          Temukan jawaban untuk pertanyaan umum tentang Grovia
        </p>
      </div>

      <!-- FAQ Categories -->
      <div class="faq-categories">
        <button
          v-for="category in categories"
          :key="category.id"
          @click="activeCategory = category.id"
          :class="['category-btn', { active: activeCategory === category.id }]"
        >
          {{ category.name }}
        </button>
      </div>

      <!-- FAQ Items -->
      <div class="faq-list">
        <div
          v-for="(item, index) in filteredFaqs"
          :key="index"
          class="faq-item"
          :class="{ open: openItems.includes(index) }"
        >
          <button @click="toggleItem(index)" class="faq-question">
            <span>{{ item.question }}</span>
            <ChevronDown :size="20" :stroke-width="2" class="chevron-icon" />
          </button>
          <div class="faq-answer">
            <p>{{ item.answer }}</p>
          </div>
        </div>
      </div>

      <!-- Contact CTA -->
      <div class="faq-cta">
        <h3>Tidak menemukan jawaban yang Anda cari?</h3>
        <p>Hubungi tim support kami untuk bantuan lebih lanjut</p>
        <a href="mailto:support@grovia.com" class="btn-contact">
          <Mail :size="18" :stroke-width="2" />
          Hubungi Support
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { ChevronDown, Mail } from 'lucide-vue-next';

const activeCategory = ref('umum');
const openItems = ref([]);

const categories = [
  { id: 'umum', name: 'Umum' },
  { id: 'deteksi', name: 'Deteksi Penyakit' },
  { id: 'akun', name: 'Akun & Keamanan' },
  { id: 'teknis', name: 'Teknis' },
];

const faqs = [
  {
    category: 'umum',
    question: 'Apa itu Grovia?',
    answer: 'Grovia adalah aplikasi berbasis kecerdasan buatan yang membantu mendeteksi penyakit tanaman melalui analisis foto daun. Aplikasi ini dirancang untuk membantu petani dan pecinta tanaman mengidentifikasi masalah kesehatan tanaman dengan cepat dan akurat.'
  },
  {
    category: 'umum',
    question: 'Apakah Grovia gratis digunakan?',
    answer: 'Ya, Grovia dapat digunakan secara gratis untuk semua pengguna. Anda dapat melakukan deteksi penyakit tanaman tanpa biaya berlangganan.'
  },
  {
    category: 'umum',
    question: 'Tanaman apa saja yang bisa dideteksi?',
    answer: 'Grovia saat ini mendukung deteksi penyakit untuk berbagai jenis tanaman, termasuk tomat, cabai, kentang, padi, jagung, dan tanaman pertanian populer lainnya. Database kami terus berkembang dengan penambahan jenis tanaman baru.'
  },
  {
    category: 'deteksi',
    question: 'Bagaimana cara melakukan deteksi penyakit?',
    answer: 'Untuk melakukan deteksi, klik menu "Deteksi Penyakit", kemudian ambil atau unggah foto daun tanaman yang ingin Anda periksa. Pastikan foto diambil dengan pencahayaan yang baik dan fokus pada daun yang menunjukkan gejala penyakit.'
  },
  {
    category: 'deteksi',
    question: 'Seberapa akurat hasil deteksi?',
    answer: 'Tingkat akurasi deteksi kami bervariasi antara 85-95%, tergantung pada kualitas foto dan kondisi tanaman. Setiap hasil deteksi dilengkapi dengan tingkat kepercayaan (confidence score) untuk membantu Anda menilai akurasi prediksi.'
  },
  {
    category: 'deteksi',
    question: 'Apa yang harus saya lakukan jika hasil deteksi tidak akurat?',
    answer: 'Jika Anda merasa hasil deteksi kurang akurat, coba ambil foto dengan pencahayaan yang lebih baik atau dari sudut yang berbeda. Anda juga dapat berkonsultasi dengan ahli pertanian untuk verifikasi lebih lanjut.'
  },
  {
    category: 'deteksi',
    question: 'Berapa lama waktu yang dibutuhkan untuk analisis?',
    answer: 'Proses analisis biasanya memakan waktu 3-10 detik, tergantung pada kecepatan koneksi internet dan ukuran file foto yang diunggah.'
  },
  {
    category: 'akun',
    question: 'Apakah saya harus membuat akun untuk menggunakan Grovia?',
    answer: 'Ya, Anda perlu membuat akun untuk menggunakan fitur deteksi dan menyimpan riwayat deteksi. Proses pendaftaran sangat mudah dan hanya memerlukan email dan password.'
  },
  {
    category: 'akun',
    question: 'Bagaimana cara mengatur ulang password?',
    answer: 'Jika Anda lupa password, klik "Lupa Password" pada halaman login, kemudian masukkan email Anda. Kami akan mengirimkan link untuk mengatur ulang password ke email Anda.'
  },
  {
    category: 'akun',
    question: 'Apakah data saya aman?',
    answer: 'Keamanan data pengguna adalah prioritas kami. Semua data disimpan dengan enkripsi dan kami tidak membagikan informasi pribadi Anda kepada pihak ketiga tanpa persetujuan Anda.'
  },
  {
    category: 'teknis',
    question: 'Format foto apa yang didukung?',
    answer: 'Grovia mendukung format foto JPG, JPEG, dan PNG. Ukuran file maksimal adalah 10MB dengan resolusi minimal 224x224 piksel untuk hasil terbaik.'
  },
  {
    category: 'teknis',
    question: 'Apakah Grovia tersedia dalam bentuk aplikasi mobile?',
    answer: 'Saat ini Grovia tersedia sebagai aplikasi web yang dapat diakses melalui browser di perangkat apapun. Versi aplikasi mobile native sedang dalam tahap pengembangan.'
  },
  {
    category: 'teknis',
    question: 'Bagaimana jika aplikasi error atau tidak berfungsi?',
    answer: 'Jika Anda mengalami masalah teknis, coba refresh halaman atau clear cache browser. Jika masalah berlanjut, hubungi support kami di support@grovia.com dengan deskripsi masalah yang detail.'
  },
];

const filteredFaqs = computed(() => {
  return faqs.filter(faq => faq.category === activeCategory.value);
});

function toggleItem(index) {
  const itemIndex = openItems.value.indexOf(index);
  if (itemIndex > -1) {
    openItems.value.splice(itemIndex, 1);
  } else {
    openItems.value.push(index);
  }
}
</script>

<style scoped>
.faq-view {
  min-height: 100vh;
  background: #f8fafc;
  padding: 40px 20px;
}

.container {
  max-width: 900px;
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
  letter-spacing: -0.02em;
}

.page-description {
  font-size: 17px;
  margin: 0;
  color: #64748b;
}

/* Categories */
.faq-categories {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
  justify-content: center;
}

.category-btn {
  padding: 10px 24px;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.category-btn:hover {
  border-color: #16a34a;
  color: #16a34a;
}

.category-btn.active {
  background: #16a34a;
  border-color: #16a34a;
  color: white;
}

/* FAQ List */
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 60px;
}

.faq-item {
  background: white;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  transition: all 0.2s;
}

.faq-item:hover {
  border-color: #cbd5e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.faq-question {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: none;
  border: none;
  text-align: left;
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  cursor: pointer;
  transition: color 0.2s;
}

.faq-question:hover {
  color: #16a34a;
}

.chevron-icon {
  flex-shrink: 0;
  transition: transform 0.3s;
  color: #64748b;
}

.faq-item.open .chevron-icon {
  transform: rotate(180deg);
  color: #16a34a;
}

.faq-answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.faq-item.open .faq-answer {
  max-height: 500px;
}

.faq-answer p {
  padding: 0 24px 24px;
  margin: 0;
  color: #475569;
  line-height: 1.7;
  font-size: 15px;
}

/* CTA */
.faq-cta {
  text-align: center;
  padding: 48px 32px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 16px;
  border: 1px solid #bbf7d0;
}

.faq-cta h3 {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 12px 0;
}

.faq-cta p {
  font-size: 16px;
  color: #475569;
  margin: 0 0 24px 0;
}

.btn-contact {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: #16a34a;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 15px;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(22, 163, 74, 0.25);
}

.btn-contact:hover {
  background: #15803d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(22, 163, 74, 0.35);
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 28px;
  }

  .faq-categories {
    gap: 8px;
  }

  .category-btn {
    padding: 8px 16px;
    font-size: 13px;
  }

  .faq-question {
    padding: 16px 20px;
    font-size: 15px;
  }

  .faq-answer p {
    padding: 0 20px 20px;
    font-size: 14px;
  }
}
</style>
