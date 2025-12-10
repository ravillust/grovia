import { defineStore } from 'pinia';
import { detectionAPI } from '@/services/api';

export const useDetectionStore = defineStore('detection', {
  state: () => ({
    // Upload state
    isUploading: false,
    uploadProgress: 0,

    // Detection state
    isDetecting: false,
    detectionResult: null,
    detectionError: null,

    // Treatment recommendation
    treatmentRecommendation: null,
    isFetchingTreatment: false,

    // Current uploaded image
    uploadedImage: null,
    imagePreview: null,
  }),

  getters: {
    /**
     * Check apakah sedang dalam proses deteksi
     */
    isProcessing: (state) => state.isUploading || state.isDetecting,

    /**
     * Get confidence level dalam format persentase
     */
    confidencePercentage: (state) => {
      const confidence = state.detectionResult?.confidence;
      if (typeof confidence !== 'number' || isNaN(confidence)) return '0.0';
      return (confidence * 100).toFixed(1);
    },

    /**
     * Check apakah hasil deteksi memiliki confidence tinggi (>70%)
     */
    isHighConfidence: (state) => {
      const confidence = state.detectionResult?.confidence;
      if (typeof confidence !== 'number' || isNaN(confidence)) return false;
      return confidence > 0.7;
    },

    /**
     * Get status severity dari penyakit (untuk UI coloring)
     */
    diseaseSeverity: (state) => {
      if (!state.detectionResult) return null;

      const confidence = state.detectionResult.confidence;
      if (confidence > 0.8) return 'high';
      if (confidence > 0.5) return 'medium';
      return 'low';
    },
  },

  actions: {
    /**
     * Upload dan deteksi penyakit tanaman (UC04, UC05)
     * @param {File} imageFile - File gambar daun
     */
    async detectDisease(imageFile) {
      this.isUploading = true;
      this.isDetecting = true;
      this.detectionError = null;
      this.detectionResult = null;
      this.treatmentRecommendation = null; // Reset treatment data from previous detection
      this.uploadProgress = 0;

      try {
        // Setup listener untuk upload progress
        const progressHandler = (event) => {
          this.uploadProgress = event.detail;
        };
        window.addEventListener('upload-progress', progressHandler);

        // Store image preview
        this.uploadedImage = imageFile;
        this.imagePreview = URL.createObjectURL(imageFile);

        // Convert image to base64 for storage
        const base64Image = await this.convertImageToBase64(imageFile);

        // Kirim request ke API
        const response = await detectionAPI.detectDisease(imageFile);

        // Cleanup progress listener
        window.removeEventListener('upload-progress', progressHandler);


        // Handle different response structures
        let detectionData = response.data;

        // If response wrapped in { success: true, data: {...} }
        if (response.data.success && response.data.data) {
          detectionData = response.data.data;
        }

        // Extract prediction data - could be nested
        let predictionData = detectionData.prediction || detectionData;

        // If prediction is empty object, check other fields
        if (predictionData && Object.keys(predictionData).length === 0) {
          // Try detection_record
          predictionData = detectionData.detection_record || detectionData;
        }


        // Parse confidence - backend bisa kirim sebagai string "85.0" atau number 0.85
        let confidence = 0;
        const confidenceValue = predictionData.confidence || predictionData.confidence_score || 0;

        if (typeof confidenceValue === 'number') {
          // Jika sudah number, cek apakah dalam format 0-1 atau 0-100
          confidence = confidenceValue > 1
            ? confidenceValue / 100
            : confidenceValue;
        } else if (typeof confidenceValue === 'string') {
          // Jika string, parse dan convert ke 0-1
          const parsed = parseFloat(confidenceValue);
          confidence = !isNaN(parsed) ? (parsed > 1 ? parsed / 100 : parsed) : 0;
        }

        // Extract disease information from various possible fields
        const diseaseId = predictionData.disease_id || predictionData.id || detectionData.detection_id || 'unknown';
        const diseaseName = predictionData.disease_name || predictionData.name || predictionData.class_name || 'Penyakit tidak teridentifikasi';
        const scientificName = predictionData.scientific_name || predictionData.latin_name || '-';
        const description = predictionData.description || predictionData.detail || 'Tidak ada deskripsi tersedia';
        const symptoms = predictionData.symptoms || predictionData.symptom_list || [];

        // Extract recommendations from detection response (already included!)
        const recommendations = detectionData.recommendations || predictionData.recommendations || [];

        // Store hasil deteksi
        this.detectionResult = {
          diseaseId,
          diseaseName,
          scientificName,
          confidence,
          timestamp: new Date().toISOString(),
          imageUrl: base64Image, // Use base64 instead of blob URL
          description,
          symptoms: Array.isArray(symptoms) ? symptoms : [],
        };


        // Use recommendations from detection response instead of fetching separately
        if (Array.isArray(recommendations) && recommendations.length > 0) {
          this.treatmentRecommendation = {
            prevention: [],
            treatment: recommendations, // Use recommendations directly
            organicSolutions: [],
            chemicalSolutions: [],
            additionalTips: [],
          };
        }

        // REMOVED: Auto-fetch treatment recommendation (endpoint error)
        // await this.fetchTreatmentRecommendation(diseaseId);

        // Simpan ke history
        await this.saveToHistory();

        return this.detectionResult;
      } catch (error) {
        console.error('Detection error:', error);
        console.error('Error response:', error.response);
        console.error('Error code:', error.code);
        console.error('Error message:', error.message);

        // Handle timeout error
        if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
          this.detectionError = 'Proses deteksi memakan waktu terlalu lama. Ini bisa terjadi karena:\n' +
            '• Gambar terlalu besar (max 5MB)\n' +
            '• Koneksi internet lambat\n' +
            '• Server sedang sibuk\n\n' +
            'Silakan coba lagi dengan gambar yang lebih kecil atau tunggu beberapa saat.';
        }
        // Handle bad request - Read error message from backend
        else if (error.response?.status === 400) {
          // Try to get error detail from backend response
          const errorDetail = error.response.data?.detail ||
                              error.response.data?.message ||
                              'Format gambar tidak valid. Gunakan JPG, PNG, atau WebP.';
          this.detectionError = errorDetail;
        }
        // Handle server error
        else if (error.response?.status === 500) {
          const errorDetail = error.response.data?.detail ||
                              error.response.data?.message ||
                              'Server mengalami kendala. Silakan coba lagi dalam beberapa saat.';
          this.detectionError = errorDetail;
        }
        // Handle network error
        else if (!error.response) {
          this.detectionError = 'Tidak dapat terhubung ke server. Pastikan:\n' +
            '• Backend berjalan di http://localhost:8000\n' +
            '• Koneksi internet Anda stabil';
        }
        // Default error - try to read from backend first
        else {
          const errorDetail = error.response?.data?.detail ||
                              error.response?.data?.message ||
                              'Gagal mendeteksi penyakit. Silakan coba lagi.';
          this.detectionError = errorDetail;
        }

        throw error;
      } finally {
        this.isUploading = false;
        this.isDetecting = false;
        this.uploadProgress = 0;
      }
    },

    /**
     * Fetch rekomendasi perawatan (UC06)
     * DEPRECATED: Recommendations sudah included di detection response
     * Endpoint /treatment tidak digunakan lagi
     * @param {string} diseaseId - ID penyakit
     */
    /* COMMENTED OUT - Using recommendations from detection response instead
    async fetchTreatmentRecommendation(diseaseId) {
      this.isFetchingTreatment = true;

      try {
        const response = await detectionAPI.getTreatmentRecommendation(diseaseId);


        // Handle different response structures
        let treatmentData = response.data;

        // If response wrapped in { success: true, data: {...} }
        if (response.data.success && response.data.data) {
          treatmentData = response.data.data;
        }


        // Helper function to convert string to array if needed
        const ensureArray = (data) => {
          if (!data) {
            return [];
          }
          if (Array.isArray(data)) {
            return data;
          }
          if (typeof data === 'string') {
            const result = [data];
            return result;
          }
          return [];
        };


        // Backend sends different field names - handle both structures
        const prevention = ensureArray(treatmentData.prevention || treatmentData.recommendations);

        const treatment = ensureArray(treatmentData.treatment);

        const organicSolutions = ensureArray(treatmentData.organic_solutions || treatmentData.organicSolutions);

        const chemicalSolutions = ensureArray(treatmentData.chemical_solutions || treatmentData.chemicalSolutions);

        const additionalTips = ensureArray(treatmentData.additional_tips || treatmentData.additionalTips);

        this.treatmentRecommendation = {
          prevention,
          treatment,
          organicSolutions,
          chemicalSolutions,
          additionalTips,
        };


        // If detection result is empty but treatment has disease_name, use it
        if ((!this.detectionResult.diseaseName || this.detectionResult.diseaseName === 'Penyakit tidak teridentifikasi')
            && treatmentData.disease_name) {
          this.detectionResult.diseaseName = treatmentData.disease_name;
          this.detectionResult.description = treatmentData.treatment || treatmentData.description || this.detectionResult.description;

          // If it's healthy plant, set confidence to high
          if (treatmentData.disease_name.toLowerCase().includes('sehat') ||
              treatmentData.disease_name.toLowerCase().includes('healthy')) {
            this.detectionResult.confidence = 0.95;
          }
        }

        return this.treatmentRecommendation;
      } catch (error) {
        console.error('Failed to fetch treatment:', error);
        this.treatmentRecommendation = null;
      } finally {
        this.isFetchingTreatment = false;
      }
    },
    */

    /**
     * Convert image file to base64
     * @param {File} file - Image file
     * @returns {Promise<string>} Base64 string
     */
    convertImageToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    },

    /**
     * Simpan hasil deteksi ke history
     */
    async saveToHistory() {
      if (!this.detectionResult) return;

      try {
        const historyData = {
          disease_id: this.detectionResult.diseaseId,
          disease_name: this.detectionResult.diseaseName,
          confidence: this.detectionResult.confidence,
          image_url: this.detectionResult.imageUrl,
          timestamp: this.detectionResult.timestamp,
        };

        await detectionAPI.saveDetectionHistory(historyData);
      } catch (error) {
        // Logging error, tapi tidak throw karena ini bukan critical
        console.error('Failed to save history:', error);
      }
    },

    /**
     * Reset detection state
     */
    resetDetection() {
      // Cleanup image preview URL
      if (this.imagePreview) {
        URL.revokeObjectURL(this.imagePreview);
      }

      this.isUploading = false;
      this.uploadProgress = 0;
      this.isDetecting = false;
      this.detectionResult = null;
      this.detectionError = null;
      this.treatmentRecommendation = null;
      this.isFetchingTreatment = false;
      this.uploadedImage = null;
      this.imagePreview = null;
    },

    /**
     * Clear error message
     */
    clearError() {
      this.detectionError = null;
    },
  },
});
