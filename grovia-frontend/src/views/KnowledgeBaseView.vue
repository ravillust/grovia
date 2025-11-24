<template>
  <div class="knowledge-base-view">
    <div class="kb-container">
      <!-- Page Header -->
      <div class="page-header">
        <h1 class="page-title">Basis Pengetahuan Penyakit Tanaman</h1>
        <p class="page-description">
          Pelajari berbagai jenis penyakit tanaman, gejala, dan cara pencegahannya
        </p>
      </div>

      <!-- Search Bar -->
      <div class="search-section">
        <div class="search-box">
          <span class="search-icon"><Search :size="18" :stroke-width="1.6" /></span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari penyakit tanaman..."
            class="search-input"
            @input="handleSearch"
          />
          <button v-if="searchQuery" @click="clearSearch" class="clear-btn">
            <X :size="14" :stroke-width="2" />
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-container">
        <LoadingSpinner size="large" text="Memuat data penyakit..." />
      </div>

      <!-- Diseases List -->
      <div v-else-if="filteredDiseases.length > 0" class="diseases-list">
        <div
          v-for="disease in filteredDiseases"
          :key="disease.disease_id"
          class="disease-item"
        >
          <div class="disease-thumbnail">
            <img :src="disease.thumbnail || getPlaceholderImage()" :alt="disease.disease_name" />
          </div>
          <div class="disease-content">
            <div class="disease-main">
              <h3 class="disease-name">{{ disease.disease_name }}</h3>
              <p class="disease-scientific">{{ disease.scientific_name }}</p>
              <div class="disease-meta">
                <span class="category-badge" :class="`category-${disease.category}`">
                  {{ getCategoryLabel(disease.category) }}
                </span>
                <span class="severity-badge" :class="`severity-${disease.severity}`">
                  {{ getSeverityLabel(disease.severity) }}
                </span>
              </div>
            </div>
            <button @click="handleDiseaseClick(disease)" class="btn-view" title="Lihat Detail">
              <Eye :size="18" :stroke-width="1.6" />
              <span>Detail</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon"><Search :size="56" :stroke-width="1.6" /></div>
        <h3 class="empty-title">Tidak Ditemukan</h3>
        <p class="empty-description">
          Tidak ada penyakit yang sesuai dengan pencarian "{{ searchQuery }}".
          Coba kata kunci lain.
        </p>
      </div>

      <!-- Info Section -->
      <div class="info-section">
        <h2 class="info-title">Tentang Basis Pengetahuan</h2>
        <div class="info-cards">
          <div class="info-card">
            <div class="info-icon"><BookOpen :size="40" :stroke-width="1.6" /></div>
            <h3>50+ Penyakit</h3>
            <p>Database lengkap berbagai jenis penyakit tanaman</p>
          </div>
          <div class="info-card">
            <div class="info-icon"><Microscope :size="40" :stroke-width="1.6" /></div>
            <h3>Detail Lengkap</h3>
            <p>Informasi gejala, penyebab, dan cara penanganan</p>
          </div>
          <div class="info-card">
            <div class="info-icon"><Leaf :size="40" :stroke-width="1.6" /></div>
            <h3>Tips Pencegahan</h3>
            <p>Panduan mencegah penyakit tanaman sejak dini</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Disease Detail Modal -->
    <teleport to="body">
      <div v-if="selectedDisease" class="modal-backdrop" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2 class="modal-title">{{ selectedDisease.disease_name }}</h2>
            <button @click="closeModal" class="modal-close"><X :size="16" :stroke-width="2" /></button>
          </div>
          <div class="modal-body">
            <p class="modal-scientific">{{ selectedDisease.scientific_name }}</p>

            <div class="modal-section">
              <h3 class="section-title">Deskripsi</h3>
              <p>{{ selectedDisease.description || 'Deskripsi tidak tersedia.' }}</p>
            </div>

            <div class="modal-section">
              <h3 class="section-title">Gejala Umum</h3>
              <ul>
                <li v-for="(symptom, index) in selectedDisease.symptoms" :key="index">
                  {{ symptom }}
                </li>
              </ul>
            </div>

            <div class="modal-section">
              <h3 class="section-title">Tanaman yang Terpengaruh</h3>
              <div class="plant-tags">
                <span v-for="(plant, index) in selectedDisease.affected_plants" :key="index" class="plant-tag">
                  {{ plant }}
                </span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeModal" class="btn-close">Tutup</button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { knowledgeBaseAPI } from '@/services/api';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import { Search, BookOpen, Microscope, Leaf, FileText, X } from 'lucide-vue-next';

// State
const diseases = ref([]);
const searchQuery = ref('');
const isLoading = ref(false);
const selectedDisease = ref(null);

// Computed
const filteredDiseases = computed(() => {
  if (!diseases.value || !Array.isArray(diseases.value)) return [];
  if (!searchQuery.value) return diseases.value;

  const query = searchQuery.value.toLowerCase();
  return diseases.value.filter(disease =>
    disease?.disease_name?.toLowerCase().includes(query) ||
    disease?.scientific_name?.toLowerCase().includes(query)
  );
});

// Methods
async function fetchDiseases() {
  isLoading.value = true;
  try {
    const response = await knowledgeBaseAPI.getDiseases();
    diseases.value = response.data;
  } catch (error) {
    console.error('Failed to fetch diseases:', error);
    // Use mock data for demonstration
    diseases.value = generateMockDiseases();
  } finally {
    isLoading.value = false;
  }
}

function handleSearch() {
  // Search is reactive through computed property
}

function clearSearch() {
  searchQuery.value = '';
}

function handleDiseaseClick(disease) {
  selectedDisease.value = disease;
}

function closeModal() {
  selectedDisease.value = null;
}

function getCategoryLabel(category) {
  const labels = {
    fungal: 'Jamur',
    bacterial: 'Bakteri',
    viral: 'Virus',
    pest: 'Hama',
  };
  return labels[category] || category;
}

function getSeverityLabel(severity) {
  const labels = {
    high: 'Tinggi',
    medium: 'Sedang',
    low: 'Rendah',
  };
  return labels[severity] || severity;
}

function getPlaceholderImage() {
  return 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="300" height="200"%3E%3Crect fill="%23f7fafc" width="300" height="200"/%3E%3Ctext fill="%23a0aec0" font-family="sans-serif" font-size="18" x="50%25" y="50%25" text-anchor="middle" dominant-baseline="middle"%3ENo%20image%3C/text%3E%3C/svg%3E';
}

function generateMockDiseases() {
  return [
    // Penyakit Jamur (Fungal)
    {
      disease_id: '1',
      disease_name: 'Hawar Daun',
      scientific_name: 'Phytophthora infestans',
      category: 'fungal',
      severity: 'high',
      thumbnail: null,
      description: 'Penyakit jamur yang sangat merusak, menyerang daun, batang, dan umbi. Berkembang cepat dalam kondisi lembab dan sejuk.',
      symptoms: ['Bercak coklat kehitaman pada daun', 'Daun mengering dan mati', 'Pertumbuhan terhambat', 'Lapisan putih di bawah daun', 'Busuk pada umbi'],
      affected_plants: ['Tomat', 'Kentang', 'Terong', 'Cabai'],
    },
    {
      disease_id: '2',
      disease_name: 'Bercak Daun Cercospora',
      scientific_name: 'Cercospora spp.',
      category: 'fungal',
      severity: 'medium',
      thumbnail: null,
      description: 'Infeksi jamur yang menyebabkan bercak bulat pada daun. Umum terjadi pada berbagai tanaman dalam kondisi lembab.',
      symptoms: ['Bercak bulat dengan pusat keabu-abuan', 'Tepi bercak berwarna coklat tua', 'Daun menguning dan rontok', 'Defoliasi prematur'],
      affected_plants: ['Padi', 'Jagung', 'Kedelai', 'Bit', 'Singkong'],
    },
    {
      disease_id: '3',
      disease_name: 'Embun Tepung',
      scientific_name: 'Erysiphe cichoracearum',
      category: 'fungal',
      severity: 'medium',
      thumbnail: null,
      description: 'Penyakit jamur yang membentuk lapisan tepung putih pada permukaan daun. Berkembang pada kondisi hangat dan kering.',
      symptoms: ['Lapisan putih seperti tepung', 'Daun mengkerut dan menggulung', 'Pertumbuhan terhambat', 'Daun menguning'],
      affected_plants: ['Mentimun', 'Labu', 'Zucchini', 'Terong', 'Tomat', 'Mawar'],
    },
    {
      disease_id: '4',
      disease_name: 'Karat Daun',
      scientific_name: 'Puccinia spp.',
      category: 'fungal',
      severity: 'high',
      thumbnail: null,
      description: 'Penyakit jamur yang menghasilkan pustula berwarna karat/coklat kemerahan pada daun. Sangat menular dan merusak.',
      symptoms: ['Pustula kecil berwarna oranye-coklat', 'Daun menguning', 'Defoliasi dini', 'Penurunan hasil panen'],
      affected_plants: ['Kopi', 'Gandum', 'Jagung', 'Kacang-kacangan', 'Mawar'],
    },
    {
      disease_id: '5',
      disease_name: 'Antraknosa',
      scientific_name: 'Colletotrichum spp.',
      category: 'fungal',
      severity: 'high',
      thumbnail: null,
      description: 'Penyakit jamur yang menyebabkan lesi cekung pada daun, batang, dan buah. Berkembang dalam kondisi hangat dan lembab.',
      symptoms: ['Bercak gelap cekung', 'Lesi dengan lingkaran konsentris', 'Busuk pada buah', 'Daun gugur prematur'],
      affected_plants: ['Cabai', 'Tomat', 'Mangga', 'Pepaya', 'Stroberi'],
    },
    {
      disease_id: '6',
      disease_name: 'Busuk Daun Alternaria',
      scientific_name: 'Alternaria solani',
      category: 'fungal',
      severity: 'medium',
      thumbnail: null,
      description: 'Jamur yang menyebabkan bercak target pada daun tua. Umum pada tanaman solanaceae dalam cuaca hangat.',
      symptoms: ['Bercak coklat dengan pola target', 'Halo kuning di sekitar bercak', 'Daun tua paling terpengaruh', 'Defoliasi dari bawah ke atas'],
      affected_plants: ['Tomat', 'Kentang', 'Terong', 'Paprika'],
    },
    {
      disease_id: '7',
      disease_name: 'Busuk Daun Phytophthora',
      scientific_name: 'Phytophthora capsici',
      category: 'fungal',
      severity: 'high',
      thumbnail: null,
      description: 'Penyakit jamur air yang sangat destruktif, menyerang akar, batang, dan buah. Berkembang cepat dalam tanah basah.',
      symptoms: ['Layu mendadak', 'Busuk pada pangkal batang', 'Daun menguning dan gugur', 'Busuk pada buah'],
      affected_plants: ['Cabai', 'Tomat', 'Paprika', 'Mentimun', 'Labu'],
    },
    {
      disease_id: '8',
      disease_name: 'Bercak Coklat',
      scientific_name: 'Bipolaris oryzae',
      category: 'fungal',
      severity: 'high',
      thumbnail: null,
      description: 'Penyakit utama pada padi yang menyebabkan bercak coklat lonjong pada daun. Menurunkan kualitas gabah.',
      symptoms: ['Bercak lonjong berwarna coklat', 'Pusat bercak keabu-abuan', 'Daun mengering', 'Gabah hampa'],
      affected_plants: ['Padi', 'Gandum', 'Barley'],
    },
    {
      disease_id: '9',
      disease_name: 'Downy Mildew',
      scientific_name: 'Peronospora spp.',
      category: 'fungal',
      severity: 'high',
      thumbnail: null,
      description: 'Jamur obligat yang menyebabkan pertumbuhan berbulu di bawah daun. Berkembang dalam kondisi dingin dan lembab.',
      symptoms: ['Bercak kuning pada permukaan atas daun', 'Pertumbuhan putih keabu-abuan di bawah daun', 'Daun mengkerut', 'Pertumbuhan terhambat'],
      affected_plants: ['Anggur', 'Mentimun', 'Selada', 'Bayam', 'Bawang'],
    },
    {
      disease_id: '10',
      disease_name: 'Bercak Septoria',
      scientific_name: 'Septoria lycopersici',
      category: 'fungal',
      severity: 'medium',
      thumbnail: null,
      description: 'Penyakit jamur yang menghasilkan bercak kecil dengan titik hitam di tengah. Umum pada tanaman tomat.',
      symptoms: ['Bercak bulat kecil dengan pusat putih', 'Titik hitam (piknidia) di tengah', 'Daun menguning dan gugur', 'Dimulai dari daun bawah'],
      affected_plants: ['Tomat', 'Terong', 'Kentang'],
    },

    // Penyakit Bakteri (Bacterial)
    {
      disease_id: '11',
      disease_name: 'Busuk Daun Bakteri',
      scientific_name: 'Xanthomonas campestris',
      category: 'bacterial',
      severity: 'high',
      thumbnail: null,
      description: 'Infeksi bakteri yang menyebabkan pembusukan daun dengan bau khas. Menyebar melalui air dan alat pertanian.',
      symptoms: ['Daun membusuk dengan bau tidak sedap', 'Lesi basah berwarna gelap', 'Perubahan warna kuning di sekitar lesi', 'Defoliasi'],
      affected_plants: ['Kubis', 'Brokoli', 'Kale', 'Sawi', 'Lobak'],
    },
    {
      disease_id: '12',
      disease_name: 'Hawar Daun Bakteri',
      scientific_name: 'Pseudomonas syringae',
      category: 'bacterial',
      severity: 'high',
      thumbnail: null,
      description: 'Bakteri yang menyebabkan bercak nekrotik pada daun. Masuk melalui luka dan stomata dalam kondisi lembab.',
      symptoms: ['Bercak coklat kehitaman dengan halo kuning', 'Lesi angular mengikuti tulang daun', 'Eksudasi bakteri', 'Kematian jaringan'],
      affected_plants: ['Tomat', 'Kacang', 'Kubis', 'Kedelai'],
    },
    {
      disease_id: '13',
      disease_name: 'Kanker Bakteri',
      scientific_name: 'Clavibacter michiganensis',
      category: 'bacterial',
      severity: 'high',
      thumbnail: null,
      description: 'Penyakit bakteri sistemik yang menginfeksi sistem vaskular. Sangat destruktif dan sulit dikendalikan.',
      symptoms: ['Layu pada satu sisi tanaman', 'Bercak putih pada buah', 'Kanker pada batang', 'Daun menggulung dan mati'],
      affected_plants: ['Tomat', 'Paprika', 'Terong'],
    },
    {
      disease_id: '14',
      disease_name: 'Bercak Daun Bakteri',
      scientific_name: 'Xanthomonas vesicatoria',
      category: 'bacterial',
      severity: 'medium',
      thumbnail: null,
      description: 'Bakteri yang menyebabkan bercak kecil pada daun dan buah. Umum pada tanaman solanaceae dan cucurbitaceae.',
      symptoms: ['Bercak kecil cekung dengan halo kuning', 'Lesi pada buah', 'Defoliasi prematur', 'Penurunan kualitas buah'],
      affected_plants: ['Tomat', 'Paprika', 'Cabai', 'Terong'],
    },
    {
      disease_id: '15',
      disease_name: 'Busuk Lunak Bakteri',
      scientific_name: 'Erwinia carotovora',
      category: 'bacterial',
      severity: 'high',
      thumbnail: null,
      description: 'Bakteri yang menyebabkan pembusukan jaringan lunak dengan cepat. Menghasilkan enzim pektinase yang merusak dinding sel.',
      symptoms: ['Jaringan lunak dan berair', 'Bau busuk yang kuat', 'Pembusukan cepat', 'Warna jaringan berubah coklat'],
      affected_plants: ['Kentang', 'Wortel', 'Kubis', 'Tomat', 'Bawang'],
    },

    // Penyakit Virus (Viral)
    {
      disease_id: '16',
      disease_name: 'Mosaik Daun',
      scientific_name: 'Tobacco Mosaic Virus (TMV)',
      category: 'viral',
      severity: 'high',
      thumbnail: null,
      description: 'Virus yang menyebabkan pola mosaik pada daun. Ditularkan secara mekanis dan sangat stabil di lingkungan.',
      symptoms: ['Pola mosaik hijau terang dan gelap', 'Daun mengkerut dan menggulung', 'Pertumbuhan terhambat', 'Buah berbintik'],
      affected_plants: ['Tomat', 'Tembakau', 'Paprika', 'Terung', 'Mentimun'],
    },
    {
      disease_id: '17',
      disease_name: 'Keriting Daun',
      scientific_name: 'Tomato Yellow Leaf Curl Virus (TYLCV)',
      category: 'viral',
      severity: 'high',
      thumbnail: null,
      description: 'Virus yang ditularkan kutu kebul, menyebabkan daun menggulung dan menguning. Sangat merusak produksi tomat.',
      symptoms: ['Daun menggulung ke atas', 'Daun menguning', 'Pertumbuhan kerdil', 'Penurunan drastis hasil'],
      affected_plants: ['Tomat', 'Cabai', 'Terong', 'Kacang'],
    },
    {
      disease_id: '18',
      disease_name: 'Belang Daun',
      scientific_name: 'Cucumber Mosaic Virus (CMV)',
      category: 'viral',
      severity: 'medium',
      thumbnail: null,
      description: 'Virus dengan kisaran inang luas, ditularkan oleh kutu daun. Menyebabkan mosaik dan distorsi pada daun.',
      symptoms: ['Mosaik kuning-hijau', 'Daun terdistorsi', 'Bunga terdistorsi (broke flower)', 'Buah belang'],
      affected_plants: ['Mentimun', 'Labu', 'Tomat', 'Paprika', 'Bayam'],
    },
    {
      disease_id: '19',
      disease_name: 'Kerdil Daun',
      scientific_name: 'Rice Tungro Virus',
      category: 'viral',
      severity: 'high',
      thumbnail: null,
      description: 'Penyakit virus paling merusak pada padi. Ditularkan oleh wereng hijau, menyebabkan kerdil dan menguning.',
      symptoms: ['Daun menguning dari ujung', 'Pertumbuhan sangat kerdil', 'Jumlah anakan berkurang', 'Gabah hampa atau tidak keluar'],
      affected_plants: ['Padi'],
    },
    {
      disease_id: '20',
      disease_name: 'Daun Bergaris',
      scientific_name: 'Barley Yellow Dwarf Virus (BYDV)',
      category: 'viral',
      severity: 'medium',
      thumbnail: null,
      description: 'Virus yang ditularkan kutu daun pada tanaman sereal. Menyebabkan menguning dan kerdil.',
      symptoms: ['Garis kuning atau merah pada daun', 'Pertumbuhan kerdil', 'Daun kaku dan tegak', 'Penurunan hasil biji'],
      affected_plants: ['Gandum', 'Barley', 'Jagung', 'Padi'],
    },

    // Penyakit Hama (Pest)
    {
      disease_id: '21',
      disease_name: 'Kerusakan Ulat Grayak',
      scientific_name: 'Spodoptera litura',
      category: 'pest',
      severity: 'high',
      thumbnail: null,
      description: 'Hama ulat yang sangat rakus, memakan daun hingga tinggal tulang daun. Aktif pada malam hari.',
      symptoms: ['Daun berlubang besar', 'Hanya tulang daun tersisa', 'Kotoran ulat pada daun', 'Kerusakan cepat dalam semalam'],
      affected_plants: ['Kubis', 'Kedelai', 'Tomat', 'Cabai', 'Tembakau'],
    },
    {
      disease_id: '22',
      disease_name: 'Serangan Kutu Daun',
      scientific_name: 'Aphis spp.',
      category: 'pest',
      severity: 'medium',
      thumbnail: null,
      description: 'Serangga kecil yang menghisap cairan tanaman. Menularkan virus dan mengeluarkan embun madu.',
      symptoms: ['Daun menggulung dan mengeriting', 'Embun madu dan jelaga hitam', 'Daun menguning', 'Pertumbuhan terhambat'],
      affected_plants: ['Kubis', 'Tomat', 'Cabai', 'Terong', 'Mentimun'],
    },
    {
      disease_id: '23',
      disease_name: 'Tungau Laba-laba',
      scientific_name: 'Tetranychus urticae',
      category: 'pest',
      severity: 'medium',
      thumbnail: null,
      description: 'Tungau mikroskopis yang membuat jaring halus dan menghisap cairan sel daun. Berkembang cepat dalam kondisi panas kering.',
      symptoms: ['Bintik kuning pada daun', 'Jaring laba-laba halus', 'Daun kusam dan kering', 'Daun rontok'],
      affected_plants: ['Tomat', 'Paprika', 'Terong', 'Mentimun', 'Stroberi'],
    },
    {
      disease_id: '24',
      disease_name: 'Penggerek Daun',
      scientific_name: 'Liriomyza spp.',
      category: 'pest',
      severity: 'medium',
      thumbnail: null,
      description: 'Larva lalat kecil yang membuat terowongan di dalam jaringan daun. Merusak fotosintesis tanaman.',
      symptoms: ['Terowongan berliku pada daun', 'Titik-titik tusukan kecil', 'Daun menguning', 'Daun gugur prematur'],
      affected_plants: ['Tomat', 'Kentang', 'Kacang', 'Mentimun', 'Selada'],
    },
    {
      disease_id: '25',
      disease_name: 'Kerusakan Thrips',
      scientific_name: 'Thrips tabaci',
      category: 'pest',
      severity: 'medium',
      thumbnail: null,
      description: 'Serangga kecil yang menghisap cairan sel dan menularkan virus. Sulit dikendalikan karena ukurannya kecil.',
      symptoms: ['Bercak keperakan pada daun', 'Daun terdistorsi', 'Bunga rontok', 'Buah cacat'],
      affected_plants: ['Bawang', 'Tomat', 'Cabai', 'Mentimun', 'Stroberi'],
    },
    {
      disease_id: '26',
      disease_name: 'Kerusakan Kepik',
      scientific_name: 'Nezara viridula',
      category: 'pest',
      severity: 'low',
      thumbnail: null,
      description: 'Kepik yang menghisap cairan dari daun, batang, dan buah. Menyebabkan bercak dan deformasi.',
      symptoms: ['Bercak coklat pada daun', 'Buah cacat dan berbintik', 'Biji keriput', 'Daun berlubang kecil'],
      affected_plants: ['Kedelai', 'Jagung', 'Tomat', 'Kacang', 'Okra'],
    },
    {
      disease_id: '27',
      disease_name: 'Kerusakan Walang Sangit',
      scientific_name: 'Leptocorisa oratorius',
      category: 'pest',
      severity: 'high',
      thumbnail: null,
      description: 'Hama utama padi yang menghisap bulir padi saat masih muda. Menyebabkan gabah hampa.',
      symptoms: ['Gabah hampa', 'Bulir padi berwarna coklat', 'Bau tidak sedap', 'Penurunan kualitas gabah'],
      affected_plants: ['Padi'],
    },
    {
      disease_id: '28',
      disease_name: 'Kerusakan Belalang',
      scientific_name: 'Locusta migratoria',
      category: 'pest',
      severity: 'high',
      thumbnail: null,
      description: 'Hama pemakan daun yang sangat rakus, dapat menghabiskan tanaman dalam waktu singkat.',
      symptoms: ['Daun dimakan dari tepi', 'Lubang besar tidak beraturan', 'Kerusakan masif', 'Kotoran hijau pada daun'],
      affected_plants: ['Padi', 'Jagung', 'Kedelai', 'Sayuran'],
    },
  ];
}

// Lifecycle
onMounted(() => {
  fetchDiseases();
});
</script>

<style scoped>
.knowledge-base-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 40px 0;
}

.kb-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: 56px;
}

.page-title {
  font-size: 48px;
  font-weight: 800;
  color: #1a3a2e;
  margin: 0 0 16px 0;
  letter-spacing: -0.03em;
}

.page-description {
  font-size: 19px;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

/* Search Section */
.search-section {
  margin-bottom: 56px;
}

.search-box {
  max-width: 600px;
  margin: 0 auto;
  position: relative;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.search-icon {
  font-size: 24px;
  margin-right: 12px;
}

.search-icon svg {
  display: block;
  color: #64748b;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 16px;
  color: #2d3748;
}

.search-input::placeholder {
  color: #a0aec0;
}

.clear-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7fafc;
  border: none;
  border-radius: 50%;
  color: #718096;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: #e2e8f0;
}

/* Loading */
.loading-container {
  display: flex;
  justify-content: center;
  padding: 60px 20px;
}

/* Diseases List */
.diseases-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 60px;
}

.disease-item {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px;
}

.disease-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #6aa581;
}

.disease-thumbnail {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 10px;
  overflow: hidden;
  background: #f8faf9;
}

.disease-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.disease-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  min-width: 0;
}

.disease-main {
  flex: 1;
  min-width: 0;
}

.disease-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a3a2e;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  letter-spacing: -0.01em;
}

.disease-scientific {
  font-size: 13px;
  font-style: italic;
  color: #64748b;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.disease-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-view {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: #6aa581;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-view:hover {
  background: #5a9470;
  transform: translateY(-2px);
}

.btn-view svg {
  display: block;
}

.category-badge,
.severity-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.category-fungal {
  background: #fed7e2;
  color: #97266d;
}

.category-bacterial {
  background: #fef3c7;
  color: #78350f;
}

.category-viral {
  background: #dbeafe;
  color: #1e40af;
}

.category-pest {
  background: #fee2e2;
  color: #991b1b;
}

.severity-high {
  background: #fed7d7;
  color: #742a2a;
}

.severity-medium {
  background: #feebc8;
  color: #7c2d12;
}

.severity-low {
  background: #c6f6d5;
  color: #22543d;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 60px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 24px;
  opacity: 0.5;
  display:flex;
  align-items:center;
  justify-content:center;
}

.empty-icon svg {
  color: #a0aec0;
}

.empty-title {
  font-size: 28px;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 12px 0;
}

.empty-description {
  font-size: 16px;
  color: #718096;
  margin: 0;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

/* Info Section */
.info-section {
  margin-top: 60px;
  text-align: center;
}

.info-title {
  font-size: 32px;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 40px 0;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.info-card {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.info-icon {
  font-size: 48px;
  margin-bottom: 16px;
  display:flex;
  align-items:center;
  justify-content:center;
}

.info-icon svg {
  color: #16a34a;
}

.info-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 12px 0;
}

.info-card p {
  font-size: 15px;
  color: #718096;
  line-height: 1.6;
  margin: 0;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  overflow-y: auto;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
  flex: 1;
  padding-right: 16px;
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  border-radius: 8px;
  font-size: 20px;
  color: #718096;
  cursor: pointer;
  transition: background-color 0.2s;
  flex-shrink: 0;
}

.modal-close:hover {
  background: #f7fafc;
}

.modal-body {
  padding: 24px;
}

.modal-scientific {
  font-size: 16px;
  font-style: italic;
  color: #718096;
  margin: 0 0 24px 0;
}

.modal-section {
  margin-bottom: 24px;
}

.modal-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 12px 0;
}

.modal-section p {
  font-size: 15px;
  color: #4a5568;
  line-height: 1.7;
  margin: 0;
}

.modal-section ul {
  margin: 0;
  padding-left: 20px;
}

.modal-section li {
  font-size: 15px;
  color: #4a5568;
  line-height: 1.7;
  margin-bottom: 8px;
}

.plant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.plant-tag {
  padding: 6px 14px;
  background: #edf2f7;
  color: #2d3748;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
}

.modal-footer {
  padding: 24px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
}

.btn-close {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-close:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .page-title {
    font-size: 32px;
  }

  .page-description {
    font-size: 16px;
  }

  .disease-item {
    flex-direction: column;
    align-items: flex-start;
    padding: 12px;
  }

  .disease-thumbnail {
    width: 100%;
    height: 140px;
  }

  .disease-content {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .disease-name,
  .disease-scientific {
    white-space: normal;
  }

  .btn-view {
    width: 100%;
    justify-content: center;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }

  .modal-content {
    max-height: 95vh;
  }
}
</style>
