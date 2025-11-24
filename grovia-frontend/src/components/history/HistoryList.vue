<template>
  <div class="history-list">
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <LoadingSpinner size="large" text="Memuat riwayat deteksi..." />
    </div>

    <!-- Empty State -->
    <div v-else-if="isEmpty" class="empty-state">
      <div class="empty-icon"><Clipboard :size="56" :stroke-width="1.6" /></div>
      <h3 class="empty-title">Belum Ada Riwayat</h3>
      <p class="empty-description">
        Anda belum melakukan deteksi. Mulai deteksi penyakit tanaman untuk melihat riwayat di sini.
      </p>
      <router-link to="/detection" class="btn-start-detection">
        <Search :size="16" :stroke-width="1.6" style="margin-right:8px; vertical-align:middle;" /> Mulai Deteksi
      </router-link>
    </div>

    <!-- History Items -->
    <div v-else class="history-content">
      <!-- List Header -->
      <div class="list-header">
        <div class="header-info">
          <h3 class="list-title">Riwayat Deteksi</h3>
          <p class="list-count">{{ paginationInfo }}</p>
        </div>

        <!-- Sorting -->
        <div class="header-actions">
          <select
            v-model="sortBy"
            @change="handleSortChange"
            class="sort-select"
          >
            <option value="newest">Terbaru</option>
            <option value="oldest">Terlama</option>
          </select>
          <button @click="handleRefresh" class="btn-refresh" title="Refresh">
            <span class="refresh-icon" :class="{ spinning: isRefreshing }">
              <RefreshCw :size="18" :stroke-width="1.6" />
            </span>
          </button>
        </div>
      </div>

      <!-- Items Grid -->
      <div class="history-grid">
        <HistoryItem
          v-for="item in items"
          :key="item.history_id"
          :item="item"
          @view="handleViewDetail"
          @delete="handleDelete"
        />
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          @click="handlePreviousPage"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          ← Sebelumnya
        </button>

        <div class="pagination-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="handleGoToPage(page)"
            :class="['pagination-number', { active: page === currentPage }]"
          >
            {{ page }}
          </button>
        </div>

        <button
          @click="handleNextPage"
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          Selanjutnya →
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <teleport to="body">
      <div v-if="showDeleteModal" class="modal-backdrop" @click="closeDeleteModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">Konfirmasi Hapus</h3>
            <button @click="closeDeleteModal" class="modal-close"><X :size="14" :stroke-width="2" /></button>
          </div>
          <div class="modal-body">
            <p>Apakah Anda yakin ingin menghapus riwayat deteksi ini?</p>
            <p class="modal-warning">Tindakan ini tidak dapat dibatalkan.</p>
          </div>
          <div class="modal-footer">
            <button @click="closeDeleteModal" class="btn-cancel">
              Batal
            </button>
            <button
              @click="confirmDelete"
              :disabled="isDeleting"
              class="btn-delete"
            >
              <span v-if="!isDeleting">Hapus</span>
              <span v-else>Menghapus...</span>
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useHistoryStore } from '@/stores/history';
import HistoryItem from './HistoryItem.vue';
import LoadingSpinner from '@/components/common/LoadingSpinner.vue';
import { Search, Clipboard, RefreshCw, X } from 'lucide-vue-next';

const router = useRouter();
const historyStore = useHistoryStore();

// Local state
const sortBy = ref('newest');
const isRefreshing = ref(false);
const showDeleteModal = ref(false);
const itemToDelete = ref(null);

// Computed
const items = computed(() => historyStore.items);
const isLoading = computed(() => historyStore.isLoading);
const isEmpty = computed(() => historyStore.isEmpty);
const currentPage = computed(() => historyStore.currentPage);
const totalPages = computed(() => historyStore.totalPages);
const paginationInfo = computed(() => historyStore.paginationInfo);

// Calculate visible page numbers
const visiblePages = computed(() => {
  const total = totalPages.value;
  const current = currentPage.value;
  const pages = [];

  if (total <= 7) {
    // Show all pages if total is 7 or less
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    // Always show first page
    pages.push(1);

    if (current > 3) {
      pages.push('...');
    }

    // Show pages around current
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i);
    }

    if (current < total - 2) {
      pages.push('...');
    }

    // Always show last page
    pages.push(total);
  }

  return pages;
});

// Methods
async function handleSortChange() {
  await historyStore.changeSortOrder(sortBy.value);
}

async function handleRefresh() {
  isRefreshing.value = true;
  try {
    await historyStore.refresh();
  } finally {
    setTimeout(() => {
      isRefreshing.value = false;
    }, 500);
  }
}

function handleViewDetail(item) {
  router.push(`/history/${item.history_id}`);
}

function handleDelete(item) {
  itemToDelete.value = item;
  showDeleteModal.value = true;
}

function closeDeleteModal() {
  showDeleteModal.value = false;
  itemToDelete.value = null;
}

async function confirmDelete() {
  if (!itemToDelete.value) return;

  try {
    await historyStore.deleteHistory(itemToDelete.value.history_id);
    closeDeleteModal();
  } catch (error) {
    console.error('Failed to delete:', error);
    alert('Gagal menghapus riwayat. Silakan coba lagi.');
  }
}

async function handlePreviousPage() {
  if (currentPage.value <= 1) return;
  await historyStore.fetchHistory({
    page: currentPage.value - 1,
    reset: true
  });
}

async function handleNextPage() {
  if (currentPage.value >= totalPages.value) return;
  await historyStore.fetchHistory({
    page: currentPage.value + 1,
    reset: true
  });
}

async function handleGoToPage(page) {
  if (page === '...' || page === currentPage.value) return;
  await historyStore.fetchHistory({
    page: page,
    reset: true
  });
}

// Lifecycle
onMounted(async () => {
  console.log('HistoryList mounted, fetching history...');
  try {
    await historyStore.fetchHistory({ reset: true });
    console.log('History fetched:', historyStore.items);
  } catch (error) {
    console.error('Error fetching history:', error);
  }
});
</script>

<style scoped>
.history-list {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0;
}

/* Loading */
.loading-container {
  display: flex;
  justify-content: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
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
  color: #6aa581;
}

.empty-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a3a2e;
  margin: 0 0 12px 0;
  letter-spacing: -0.015em;
}

.empty-description {
  font-size: 16px;
  color: rgba(0, 0, 0, 0.6);
  margin: 0 0 32px 0;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.btn-start-detection {
  display: inline-block;
  padding: 14px 32px;
  background: #6aa581;
  color: white;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(106, 165, 129, 0.25);
}

.btn-start-detection:hover {
  transform: translateY(-2px);
  background: #5a9470;
  box-shadow: 0 6px 16px rgba(106, 165, 129, 0.35);
}

/* List Header */
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 24px 28px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.header-info {
  flex: 1;
}

.list-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a3a2e;
  margin: 0 0 6px 0;
  letter-spacing: -0.01em;
}

.list-count {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.6);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.sort-select {
  padding: 10px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #1a3a2e;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-select:hover {
  border-color: #6aa581;
}

.sort-select:focus {
  outline: none;
  border-color: #6aa581;
  box-shadow: 0 0 0 3px rgba(106, 165, 129, 0.1);
}

.btn-refresh {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  color: rgba(0, 0, 0, 0.6);
}

.btn-refresh:hover {
  border-color: #6aa581;
  background: #f8faf9;
  color: #6aa581;
}

.refresh-icon {
  font-size: 20px;
  display: block;
  transition: transform 0.3s;
}

.refresh-icon svg {
  display: block;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* History Grid */
.history-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.pagination-btn {
  padding: 10px 20px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1a3a2e;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  border-color: #6aa581;
  color: #6aa581;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-numbers {
  display: flex;
  gap: 8px;
}

.pagination-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #1a3a2e;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-number:hover {
  border-color: #6aa581;
  color: #6aa581;
}

.pagination-number.active {
  background: #6aa581;
  border-color: transparent;
  color: white;
}

/* Delete Modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(26, 58, 46, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  backdrop-filter: blur(8px);
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 450px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 1px solid #e5e7eb;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a3a2e;
  margin: 0;
  letter-spacing: -0.01em;
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
}

.modal-close svg {
  display: block;
}

.modal-close:hover {
  background: #f7fafc;
}

.modal-body {
  padding: 24px;
}

.modal-body p {
  font-size: 15px;
  color: rgba(0, 0, 0, 0.7);
  line-height: 1.6;
  margin: 0 0 12px 0;
}

.modal-warning {
  font-size: 14px;
  color: #dc2626;
  font-weight: 500;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel,
.btn-delete {
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: white;
  border: 2px solid #e5e7eb;
  color: #1a3a2e;
}

.btn-cancel:hover {
  background: #f8faf9;
  border-color: #6aa581;
}

.btn-delete {
  background: #dc2626;
  border: none;
  color: white;
}

.btn-delete:hover:not(:disabled) {
  background: #b91c1c;
}

.btn-delete:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
    padding: 20px;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .sort-select {
    flex: 1;
  }

  .pagination {
    flex-wrap: wrap;
  }

  .pagination-numbers {
    order: 3;
    width: 100%;
    justify-content: center;
    margin-top: 12px;
  }
}
</style>
