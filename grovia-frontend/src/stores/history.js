import { defineStore } from 'pinia';
import { historyAPI } from '@/services/api';

export const useHistoryStore = defineStore('history', {
  state: () => ({
    // History list
    items: [],
    isLoading: false,
    error: null,

    // Pagination
    currentPage: 1,
    totalPages: 1,
    totalItems: 0,
    itemsPerPage: 10,

    // Sorting
    sortBy: 'newest', // 'newest' | 'oldest'

    // Selected history detail
    selectedHistory: null,
    isLoadingDetail: false,
  }),

  getters: {
    /**
     * Check if there are more pages to load
     */
    hasMorePages: (state) => state.currentPage < state.totalPages,

    /**
     * Check if history is empty
     */
    isEmpty: (state) => !state.isLoading && state.items.length === 0,

    /**
     * Get formatted items with date grouping
     */
    groupedItems: (state) => {
      const groups = {};

      state.items.forEach(item => {
        const date = new Date(item.detected_at);
        const dateKey = date.toLocaleDateString('id-ID', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        });

        if (!groups[dateKey]) {
          groups[dateKey] = [];
        }
        groups[dateKey].push(item);
      });

      return groups;
    },

    /**
     * Get pagination information text
     */
    paginationInfo: (state) => {
      if (state.totalItems === 0) {
        return 'Tidak ada data';
      }
      const start = (state.currentPage - 1) * state.itemsPerPage + 1;
      const end = Math.min(state.currentPage * state.itemsPerPage, state.totalItems);
      return `Menampilkan ${start}-${end} dari ${state.totalItems} riwayat`;
    },
  },

  actions: {
    /**
     * Fetch history list (UC07)
     * @param {Object} options - { page, limit, sort, reset }
     */
    async fetchHistory(options = {}) {
      const {
        page = this.currentPage,
        limit = this.itemsPerPage,
        sort = this.sortBy,
        reset = false,
      } = options;

      // Reset items if starting fresh
      if (reset) {
        this.items = [];
        this.currentPage = 1;
      }

      this.isLoading = true;
      this.error = null;

      try {
        const response = await historyAPI.getHistory({
          page,
          limit,
          sort,
        });

        let items = [];
        let pagination = {
          current_page: 1,
          total_pages: 1,
          total_items: 0,
          items_per_page: limit,
        };

        // Handle different response structures
        if (Array.isArray(response.data)) {
          items = response.data;
          pagination.total_items = items.length;
        } else if (response.data?.items && Array.isArray(response.data.items)) {
          items = response.data.items;
          pagination = response.data.pagination || pagination;
        } else if (response.data?.data && Array.isArray(response.data.data)) {
          items = response.data.data;
          pagination = response.data.pagination || pagination;
        } else if (response.data?.success && response.data?.data) {
          const dataObj = response.data.data;
          if (Array.isArray(dataObj.records)) {
            items = dataObj.records;
          } else if (Array.isArray(dataObj.detections)) {
            items = dataObj.detections;
          } else if (Array.isArray(dataObj.history)) {
            items = dataObj.history;
          } else if (Array.isArray(dataObj.items)) {
            items = dataObj.items;
          }

          pagination = dataObj.pagination || response.data.pagination || pagination;
        }

        // Append or replace items
        if (reset || page === 1) {
          this.items = items;
        } else {
          this.items = [...this.items, ...items];
        }

        // Update pagination
        this.currentPage = pagination.current_page || 1;
        this.totalPages = pagination.total_pages || 1;
        this.totalItems = pagination.total_items || items.length;
        this.itemsPerPage = pagination.items_per_page || limit;
        this.sortBy = sort;

        return items;
      } catch (error) {
        console.error('Failed to fetch history:', error);

        this.items = [];
        this.currentPage = 1;
        this.totalPages = 1;
        this.totalItems = 0;
        this.itemsPerPage = limit;

        if (error.response?.status === 401) {
          this.error = 'Sesi Anda telah berakhir. Silakan login kembali.';
        } else {
          this.error = 'Gagal memuat riwayat. Silakan coba lagi.';
        }

        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Load more history items (pagination)
     */
    async loadMore() {
      if (!this.hasMorePages || this.isLoading) return;

      await this.fetchHistory({
        page: this.currentPage + 1,
        reset: false,
      });
    },

    /**
     * Refresh history list
     */
    async refresh() {
      await this.fetchHistory({ reset: true });
    },

    /**
     * Change sort order
     * @param {string} sortBy - 'newest' | 'oldest'
     */
    async changeSortOrder(sortBy) {
      if (this.sortBy === sortBy) return;

      await this.fetchHistory({
        sort: sortBy,
        reset: true,
      });
    },

    /**
     * Fetch history detail
     * @param {string} historyId - History ID
     */
    async fetchHistoryDetail(historyId) {
      this.isLoadingDetail = true;

      try {
        const response = await historyAPI.getHistoryDetail(historyId);
        this.selectedHistory = response.data;
        return response.data;
      } catch (error) {
        console.error('Failed to fetch history detail:', error);

        if (error.response?.status === 404) {
          throw new Error('Riwayat tidak ditemukan');
        } else {
          throw new Error('Gagal memuat detail riwayat');
        }
      } finally {
        this.isLoadingDetail = false;
      }
    },

    /**
     * Delete history item
     * @param {string} historyId - History ID
     */
    async deleteHistory(historyId) {
      try {
        await historyAPI.deleteHistory(historyId);

        // Remove from local state
        this.items = this.items.filter(item => item.history_id !== historyId);
        this.totalItems -= 1;

        // If selected history is deleted, clear it
        if (this.selectedHistory?.history_id === historyId) {
          this.selectedHistory = null;
        }

        return true;
      } catch (error) {
        console.error('Failed to delete history:', error);
        throw new Error('Gagal menghapus riwayat');
      }
    },

    /**
     * Clear selected history
     */
    clearSelectedHistory() {
      this.selectedHistory = null;
    },

    /**
     * Clear all history data
     */
    clearHistory() {
      this.items = [];
      this.currentPage = 1;
      this.totalPages = 1;
      this.totalItems = 0;
      this.selectedHistory = null;
      this.error = null;
    },

    /**
     * Search history by disease name
     * @param {string} query - Search query
     */
    searchHistory(query) {
      if (!query) return this.items;

      const lowerQuery = query.toLowerCase();
      return this.items.filter(item =>
        item.disease_name.toLowerCase().includes(lowerQuery)
      );
    },

    /**
     * Filter history by confidence level
     * @param {string} level - 'high' | 'medium' | 'low'
     */
    filterByConfidence(level) {
      let min = 0;
      let max = 1;

      switch (level) {
        case 'high':
          min = 0.8;
          max = 1;
          break;
        case 'medium':
          min = 0.6;
          max = 0.8;
          break;
        case 'low':
          min = 0;
          max = 0.6;
          break;
      }

      return this.items.filter(
        item => item.confidence >= min && item.confidence < max
      );
    },
  },
});
