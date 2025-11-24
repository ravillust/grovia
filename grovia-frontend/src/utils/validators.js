// Batasan ukuran file: 5MB sesuai SRS
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB dalam bytes

// Format gambar yang didukung
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];

/**
 * Validasi file gambar untuk upload
 * @param {File} file - File yang akan divalidasi
 * @returns {Object} { valid: boolean, error: string }
 */
export function validateImageFile(file) {
  if (!file) {
    return {
      valid: false,
      error: 'Tidak ada file yang dipilih',
    };
  }

  // Validasi tipe file
  if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: 'Format file tidak didukung. Gunakan JPG, JPEG, PNG, atau WebP',
    };
  }

  // Validasi ukuran file (5MB max)
  if (file.size > MAX_FILE_SIZE) {
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    return {
      valid: false,
      error: `Ukuran file terlalu besar (${fileSizeMB}MB). Maksimal 5MB`,
    };
  }

  return {
    valid: true,
    error: null,
  };
}

/**
 * Validasi dimensi gambar minimum
 * @param {File} file - File gambar
 * @param {number} minWidth - Lebar minimum (default 224px untuk CNN)
 * @param {number} minHeight - Tinggi minimum (default 224px untuk CNN)
 * @returns {Promise<Object>} { valid: boolean, error: string, dimensions: {width, height} }
 */
export function validateImageDimensions(file, minWidth = 224, minHeight = 224) {
  return new Promise((resolve) => {
    const img = new Image();
    const url = URL.createObjectURL(file);

    img.onload = () => {
      URL.revokeObjectURL(url);

      if (img.width < minWidth || img.height < minHeight) {
        resolve({
          valid: false,
          error: `Resolusi gambar terlalu kecil. Minimal ${minWidth}x${minHeight}px`,
          dimensions: { width: img.width, height: img.height },
        });
      } else {
        resolve({
          valid: true,
          error: null,
          dimensions: { width: img.width, height: img.height },
        });
      }
    };

    img.onerror = () => {
      URL.revokeObjectURL(url);
      resolve({
        valid: false,
        error: 'Gagal memuat gambar. File mungkin rusak',
        dimensions: null,
      });
    };

    img.src = url;
  });
}

/**
 * Validasi email
 * @param {string} email - Email yang akan divalidasi
 * @returns {boolean}
 */
export function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validasi password (minimal 8 karakter, kombinasi huruf dan angka)
 * @param {string} password - Password yang akan divalidasi
 * @returns {Object} { valid: boolean, error: string }
 */
export function validatePassword(password) {
  if (!password || password.length < 8) {
    return {
      valid: false,
      error: 'Password minimal 8 karakter',
    };
  }

  const hasLetter = /[a-zA-Z]/.test(password);
  const hasNumber = /[0-9]/.test(password);

  if (!hasLetter || !hasNumber) {
    return {
      valid: false,
      error: 'Password harus mengandung huruf dan angka',
    };
  }

  return {
    valid: true,
    error: null,
  };
}

/**
 * Format ukuran file ke format readable
 * @param {number} bytes - Ukuran dalam bytes
 * @returns {string} Formatted size (e.g., "2.5 MB")
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
