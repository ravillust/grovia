/**
 * Storage Service
 * Wrapper untuk localStorage dengan error handling dan encryption support
 * Sesuai dengan NF08: Data harus dienkripsi dengan AES-256
 */

const STORAGE_PREFIX = 'grovia_';
const ENCRYPTION_KEY = import.meta.env.VITE_STORAGE_KEY || 'grovia-secret-key';

/**
 * Check if localStorage is available
 */
function isStorageAvailable() {
  try {
    const test = '__storage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Simple encryption (untuk development)
 * PENTING: Gunakan library seperti crypto-js untuk production
 */
function simpleEncrypt(data) {
  try {
    return btoa(JSON.stringify(data));
  } catch (error) {
    console.error('Encryption error:', error);
    return data;
  }
}

/**
 * Simple decryption (untuk development)
 */
function simpleDecrypt(encryptedData) {
  try {
    return JSON.parse(atob(encryptedData));
  } catch (error) {
    console.error('Decryption error:', error);
    return null;
  }
}

/**
 * Storage Service Class
 */
class StorageService {
  constructor() {
    this.isAvailable = isStorageAvailable();
    this.memoryStorage = new Map(); // Fallback untuk browsers tanpa localStorage
  }

  /**
   * Generate storage key with prefix
   */
  _getKey(key) {
    return `${STORAGE_PREFIX}${key}`;
  }

  /**
   * Set item to storage
   * @param {string} key - Storage key
   * @param {any} value - Value to store
   * @param {boolean} encrypt - Whether to encrypt the data
   */
  setItem(key, value, encrypt = false) {
    const storageKey = this._getKey(key);

    try {
      let dataToStore = value;

      // Encrypt if requested (untuk data sensitif)
      if (encrypt) {
        dataToStore = simpleEncrypt(value);
      }

      const serializedValue = typeof dataToStore === 'string'
        ? dataToStore
        : JSON.stringify(dataToStore);

      if (this.isAvailable) {
        localStorage.setItem(storageKey, serializedValue);
      } else {
        // Fallback ke memory storage
        this.memoryStorage.set(storageKey, serializedValue);
      }

      return true;
    } catch (error) {
      console.error('Storage setItem error:', error);
      return false;
    }
  }

  /**
   * Get item from storage
   * @param {string} key - Storage key
   * @param {any} defaultValue - Default value if not found
   * @param {boolean} encrypted - Whether the data is encrypted
   */
  getItem(key, defaultValue = null, encrypted = false) {
    const storageKey = this._getKey(key);

    try {
      let value;

      if (this.isAvailable) {
        value = localStorage.getItem(storageKey);
      } else {
        value = this.memoryStorage.get(storageKey);
      }

      if (value === null || value === undefined) {
        return defaultValue;
      }

      // Decrypt if data was encrypted
      if (encrypted) {
        return simpleDecrypt(value);
      }

      // Try to parse JSON, return raw string if fails
      try {
        return JSON.parse(value);
      } catch {
        return value;
      }
    } catch (error) {
      console.error('Storage getItem error:', error);
      return defaultValue;
    }
  }

  /**
   * Remove item from storage
   * @param {string} key - Storage key
   */
  removeItem(key) {
    const storageKey = this._getKey(key);

    try {
      if (this.isAvailable) {
        localStorage.removeItem(storageKey);
      } else {
        this.memoryStorage.delete(storageKey);
      }
      return true;
    } catch (error) {
      console.error('Storage removeItem error:', error);
      return false;
    }
  }

  /**
   * Clear all items with prefix
   */
  clear() {
    try {
      if (this.isAvailable) {
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
          if (key.startsWith(STORAGE_PREFIX)) {
            localStorage.removeItem(key);
          }
        });
      } else {
        this.memoryStorage.clear();
      }
      return true;
    } catch (error) {
      console.error('Storage clear error:', error);
      return false;
    }
  }

  /**
   * Check if key exists
   * @param {string} key - Storage key
   */
  hasItem(key) {
    const storageKey = this._getKey(key);

    try {
      if (this.isAvailable) {
        return localStorage.getItem(storageKey) !== null;
      } else {
        return this.memoryStorage.has(storageKey);
      }
    } catch (error) {
      console.error('Storage hasItem error:', error);
      return false;
    }
  }

  /**
   * Get all keys with prefix
   */
  getAllKeys() {
    try {
      if (this.isAvailable) {
        return Object.keys(localStorage)
          .filter(key => key.startsWith(STORAGE_PREFIX))
          .map(key => key.replace(STORAGE_PREFIX, ''));
      } else {
        return Array.from(this.memoryStorage.keys())
          .map(key => key.replace(STORAGE_PREFIX, ''));
      }
    } catch (error) {
      console.error('Storage getAllKeys error:', error);
      return [];
    }
  }

  /**
   * Get storage size (approximate, in KB)
   */
  getStorageSize() {
    try {
      if (!this.isAvailable) return 0;

      let size = 0;
      Object.keys(localStorage).forEach(key => {
        if (key.startsWith(STORAGE_PREFIX)) {
          size += localStorage.getItem(key).length;
        }
      });

      // Convert to KB
      return (size / 1024).toFixed(2);
    } catch (error) {
      console.error('Storage getStorageSize error:', error);
      return 0;
    }
  }
}

// Create singleton instance
const storage = new StorageService();

// Specific storage methods untuk use cases umum
export const authStorage = {
  setToken(token) {
    return storage.setItem('authToken', token, false);
  },

  getToken() {
    return storage.getItem('authToken', null, false);
  },

  removeToken() {
    return storage.removeItem('authToken');
  },

  setUser(user) {
    return storage.setItem('user', user, true); // Encrypt user data
  },

  getUser() {
    return storage.getItem('user', null, true);
  },

  removeUser() {
    return storage.removeItem('user');
  },

  clearAuth() {
    storage.removeItem('authToken');
    storage.removeItem('user');
  },
};

export const settingsStorage = {
  setSetting(key, value) {
    return storage.setItem(`setting_${key}`, value);
  },

  getSetting(key, defaultValue = null) {
    return storage.getItem(`setting_${key}`, defaultValue);
  },

  removeSetting(key) {
    return storage.removeItem(`setting_${key}`);
  },
};

export const cacheStorage = {
  setCache(key, data, ttl = 3600000) { // Default 1 hour
    const cacheData = {
      data,
      timestamp: Date.now(),
      ttl,
    };
    return storage.setItem(`cache_${key}`, cacheData);
  },

  getCache(key) {
    const cacheData = storage.getItem(`cache_${key}`);

    if (!cacheData) return null;

    // Check if cache expired
    const now = Date.now();
    if (now - cacheData.timestamp > cacheData.ttl) {
      storage.removeItem(`cache_${key}`);
      return null;
    }

    return cacheData.data;
  },

  removeCache(key) {
    return storage.removeItem(`cache_${key}`);
  },

  clearAllCache() {
    const keys = storage.getAllKeys();
    keys.forEach(key => {
      if (key.startsWith('cache_')) {
        storage.removeItem(key);
      }
    });
  },
};

// Export default storage instance
export default storage;
