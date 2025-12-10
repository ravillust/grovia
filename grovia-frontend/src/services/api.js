import axios from 'axios';

// Base URL untuk FastAPI backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Timeout untuk API biasa: 10 detik
const API_TIMEOUT = 10000;

// Timeout untuk detection API: 60 detik (proses AI bisa lama)
const DETECTION_TIMEOUT = 60000;

// Function untuk check backend status
const checkBackendConnection = async () => {
  try {
    await axios.get(`${API_BASE_URL}/health-check`, { timeout: 5000 });
    return true;
  } catch (error) {
    console.error('Backend connection error:', error.message);
    return false;
  }
};

// Instance axios dengan konfigurasi default
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Interceptor untuk menambahkan token autentikasi
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor untuk handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired atau invalid
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API Services
export const detectionAPI = {
  /**
   * Upload dan deteksi penyakit tanaman (UC04, UC05)
   * @param {File} imageFile - File gambar daun
   * @returns {Promise} Response dengan hasil deteksi
   */
  async detectDisease(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);

    return apiClient.post('/detection/detect', formData, {
      timeout: DETECTION_TIMEOUT, // 60 detik untuk proses AI
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      // Progress tracking untuk user feedback
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        // Emit event untuk update progress bar
        window.dispatchEvent(
          new CustomEvent('upload-progress', { detail: percentCompleted })
        );
      },
    });
  },

  /**
   * Dapatkan rekomendasi perawatan (UC06)
   * @param {string} diseaseId - ID penyakit yang terdeteksi
   * @returns {Promise} Response dengan rekomendasi perawatan
   */
  async getTreatmentRecommendation(diseaseId) {
    return apiClient.get(`/detection/treatment/${diseaseId}`);
  },

  /**
   * Simpan hasil deteksi ke history
   * @param {Object} detectionData - Data hasil deteksi
   * @returns {Promise}
   */
  async saveDetectionHistory(detectionData) {
    return apiClient.post('/detection/history', detectionData);
  },
};

export const historyAPI = {
  /**
   * Ambil riwayat deteksi user (UC07)
   * @param {Object} params - Query parameters (page, limit, etc)
   * @returns {Promise} List riwayat deteksi
   */
  async getHistory(params = {}) {
    return apiClient.get('/history', { params });
  },

  /**
   * Ambil detail riwayat spesifik
   * @param {string} historyId - ID riwayat
   * @returns {Promise}
   */
  async getHistoryDetail(historyId) {
    return apiClient.get(`/history/${historyId}`);
  },

  /**
   * Hapus riwayat deteksi
   * @param {string} historyId - ID riwayat
   * @returns {Promise}
   */
  async deleteHistory(historyId) {
    return apiClient.delete(`/history/${historyId}`);
  },
};

export const authAPI = {
  /**
   * Login user
   * @param {Object} credentials - Username dan password
   * @returns {Promise}
   */
  async login(credentials) {
    return apiClient.post('/auth/login', credentials);
  },

  /**
   * Register user baru
   * @param {Object} userData - Data registrasi
   * @returns {Promise}
   */
  async register(userData) {
    return apiClient.post('/auth/register', userData);
  },

  /**
   * Logout user
   * @returns {Promise}
   */
  async logout() {
    return apiClient.post('/auth/logout');
  },

  /**
   * Get current user data
   * @returns {Promise}
   */
  async getCurrentUser() {
    return apiClient.get('/auth/me');
  },

  /**
   * Update user profile
   * @param {Object} userData - Updated profile data
   * @returns {Promise}
   */
  async updateProfile(userData) {
    return apiClient.put('/auth/profile', userData);
  },

  /**
   * Change password
   * @param {Object} passwords - Password data
   * @returns {Promise}
   */
  async changePassword(passwords) {
    return apiClient.post('/auth/change-password', passwords);
  },
    /**
     * Forgot password
     * @param {string} email - Email user
     * @returns {Promise}
     */
    async forgotPassword(email) {
      return apiClient.post('/auth/forgot-password', { email });
    },
    /**
     * Resend verification email
     * @param {Object} emailData - Object containing email
     * @returns {Promise}
     */
    async resendVerification(emailData) {
      return apiClient.post('/auth/resend-verification', emailData);
    },
    /**
     * Google Sign-In
     * @param {string} credential - Google ID token
     * @returns {Promise}
     */
    async googleSignIn(credential) {
      return apiClient.post('/auth/google-signin', { token: credential });
    },
};

export const knowledgeBaseAPI = {
  /**
   * Ambil daftar penyakit
   * @returns {Promise}
   */
  async getDiseases() {
    return apiClient.get('/knowledge/diseases');
  },

  /**
   * Ambil detail penyakit spesifik
   * @param {string} diseaseId - ID penyakit
   * @returns {Promise}
   */
  async getDiseaseDetail(diseaseId) {
    return apiClient.get(`/knowledge/diseases/${diseaseId}`);
  },
};

export default apiClient;
