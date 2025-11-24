/**
 * Formatters Utility
 * Helper functions untuk format data display
 */

/**
 * Format file size ke format readable
 * @param {number} bytes - Size dalam bytes
 * @param {number} decimals - Jumlah decimal places
 * @returns {string} Formatted size (e.g., "2.5 MB")
 */
export function formatFileSize(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  if (!bytes) return 'N/A';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Format tanggal ke format Indonesia
 * @param {string|Date} date - Tanggal
 * @param {Object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date
 */
export function formatDate(date, options = {}) {
  if (!date) return '-';

  const defaultOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    ...options,
  };

  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return new Intl.DateTimeFormat('id-ID', defaultOptions).format(dateObj);
  } catch (error) {
    console.error('Date formatting error:', error);
    return '-';
  }
}

/**
 * Format tanggal dengan waktu
 * @param {string|Date} date - Tanggal
 * @returns {string} Formatted date with time
 */
export function formatDateTime(date) {
  if (!date) return '-';

  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    return new Intl.DateTimeFormat('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(dateObj);
  } catch (error) {
    console.error('DateTime formatting error:', error);
    return '-';
  }
}

/**
 * Format relative time (e.g., "2 jam yang lalu")
 * @param {string|Date} date - Tanggal
 * @returns {string} Relative time
 */
export function formatRelativeTime(date) {
  if (!date) return '-';

  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;
    const now = new Date();
    const diffInMs = now - dateObj;
    const diffInSeconds = Math.floor(diffInMs / 1000);
    const diffInMinutes = Math.floor(diffInSeconds / 60);
    const diffInHours = Math.floor(diffInMinutes / 60);
    const diffInDays = Math.floor(diffInHours / 24);
    const diffInWeeks = Math.floor(diffInDays / 7);
    const diffInMonths = Math.floor(diffInDays / 30);
    const diffInYears = Math.floor(diffInDays / 365);

    if (diffInSeconds < 60) {
      return 'Baru saja';
    } else if (diffInMinutes < 60) {
      return `${diffInMinutes} menit yang lalu`;
    } else if (diffInHours < 24) {
      return `${diffInHours} jam yang lalu`;
    } else if (diffInDays < 7) {
      return `${diffInDays} hari yang lalu`;
    } else if (diffInWeeks < 4) {
      return `${diffInWeeks} minggu yang lalu`;
    } else if (diffInMonths < 12) {
      return `${diffInMonths} bulan yang lalu`;
    } else {
      return `${diffInYears} tahun yang lalu`;
    }
  } catch (error) {
    console.error('Relative time formatting error:', error);
    return '-';
  }
}

/**
 * Format number dengan separator ribuan
 * @param {number} number - Number to format
 * @param {number} decimals - Decimal places
 * @returns {string} Formatted number
 */
export function formatNumber(number, decimals = 0) {
  if (number === null || number === undefined) return '0';

  try {
    return new Intl.NumberFormat('id-ID', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(number);
  } catch (error) {
    console.error('Number formatting error:', error);
    return String(number);
  }
}

/**
 * Format currency (Rupiah)
 * @param {number} amount - Amount to format
 * @returns {string} Formatted currency
 */
export function formatCurrency(amount) {
  if (amount === null || amount === undefined) return 'Rp 0';

  try {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  } catch (error) {
    console.error('Currency formatting error:', error);
    return `Rp ${amount}`;
  }
}

/**
 * Format percentage
 * @param {number} value - Value (0-1 atau 0-100)
 * @param {number} decimals - Decimal places
 * @param {boolean} isDecimal - Apakah input dalam format decimal (0-1)
 * @returns {string} Formatted percentage
 */
export function formatPercentage(value, decimals = 1, isDecimal = true) {
  if (value === null || value === undefined) return '0%';

  try {
    const percentValue = isDecimal ? value * 100 : value;
    return `${percentValue.toFixed(decimals)}%`;
  } catch (error) {
    console.error('Percentage formatting error:', error);
    return '0%';
  }
}

/**
 * Format confidence score untuk deteksi
 * @param {number} confidence - Confidence value (0-1)
 * @returns {Object} Formatted confidence dengan label dan class
 */
export function formatConfidence(confidence) {
  if (confidence === null || confidence === undefined) {
    return {
      percentage: '0%',
      label: 'Tidak Diketahui',
      class: 'unknown',
    };
  }

  const percentage = (confidence * 100).toFixed(1);
  let label, className;

  if (confidence >= 0.8) {
    label = 'Sangat Tinggi';
    className = 'high';
  } else if (confidence >= 0.6) {
    label = 'Tinggi';
    className = 'medium-high';
  } else if (confidence >= 0.4) {
    label = 'Sedang';
    className = 'medium';
  } else if (confidence >= 0.2) {
    label = 'Rendah';
    className = 'low';
  } else {
    label = 'Sangat Rendah';
    className = 'very-low';
  }

  return {
    percentage: `${percentage}%`,
    label,
    class: className,
    value: confidence,
  };
}

/**
 * Truncate text dengan ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @param {string} suffix - Suffix to add (default: '...')
 * @returns {string} Truncated text
 */
export function truncateText(text, maxLength = 100, suffix = '...') {
  if (!text) return '';
  if (text.length <= maxLength) return text;

  return text.substring(0, maxLength - suffix.length) + suffix;
}

/**
 * Format phone number Indonesia
 * @param {string} phone - Phone number
 * @returns {string} Formatted phone number
 */
export function formatPhoneNumber(phone) {
  if (!phone) return '-';

  // Remove non-numeric characters
  const cleaned = phone.replace(/\D/g, '');

  // Format: 0812-3456-7890 atau +62 812-3456-7890
  if (cleaned.startsWith('62')) {
    // International format
    const match = cleaned.match(/^(\d{2})(\d{3})(\d{4})(\d{4})$/);
    if (match) {
      return `+${match[1]} ${match[2]}-${match[3]}-${match[4]}`;
    }
  } else {
    // Local format
    const match = cleaned.match(/^(\d{4})(\d{4})(\d{4})$/);
    if (match) {
      return `${match[1]}-${match[2]}-${match[3]}`;
    }
  }

  return phone;
}

/**
 * Capitalize first letter
 * @param {string} text - Text to capitalize
 * @returns {string} Capitalized text
 */
export function capitalize(text) {
  if (!text) return '';
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

/**
 * Capitalize each word
 * @param {string} text - Text to capitalize
 * @returns {string} Title cased text
 */
export function titleCase(text) {
  if (!text) return '';
  return text
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Format duration (seconds to readable format)
 * @param {number} seconds - Duration in seconds
 * @returns {string} Formatted duration
 */
export function formatDuration(seconds) {
  if (!seconds || seconds < 0) return '0 detik';

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);

  const parts = [];
  if (hours > 0) parts.push(`${hours} jam`);
  if (minutes > 0) parts.push(`${minutes} menit`);
  if (secs > 0 || parts.length === 0) parts.push(`${secs} detik`);

  return parts.join(' ');
}

/**
 * Format array to sentence (e.g., ["a", "b", "c"] => "a, b, dan c")
 * @param {Array} array - Array of items
 * @param {string} conjunction - Conjunction word (default: 'dan')
 * @returns {string} Formatted sentence
 */
export function formatArrayToSentence(array, conjunction = 'dan') {
  if (!array || array.length === 0) return '';
  if (array.length === 1) return array[0];
  if (array.length === 2) return `${array[0]} ${conjunction} ${array[1]}`;

  const last = array[array.length - 1];
  const rest = array.slice(0, -1);
  return `${rest.join(', ')}, ${conjunction} ${last}`;
}

/**
 * Slug generator untuk URL
 * @param {string} text - Text to slugify
 * @returns {string} Slugified text
 */
export function slugify(text) {
  if (!text) return '';

  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')        // Replace spaces with -
    .replace(/[^\w\-]+/g, '')    // Remove non-word chars
    .replace(/\-\-+/g, '-')      // Replace multiple - with single -
    .replace(/^-+/, '')          // Trim - from start
    .replace(/-+$/, '');         // Trim - from end
}

/**
 * Parse query string to object
 * @param {string} queryString - Query string
 * @returns {Object} Parsed object
 */
export function parseQueryString(queryString) {
  if (!queryString) return {};

  const params = new URLSearchParams(queryString);
  const result = {};

  for (const [key, value] of params) {
    result[key] = value;
  }

  return result;
}

/**
 * Object to query string
 * @param {Object} obj - Object to convert
 * @returns {string} Query string
 */
export function objectToQueryString(obj) {
  if (!obj || typeof obj !== 'object') return '';

  const params = new URLSearchParams();

  Object.keys(obj).forEach(key => {
    const value = obj[key];
    if (value !== null && value !== undefined) {
      params.append(key, value);
    }
  });

  return params.toString();
}

/**
 * Format severity level
 * @param {string} severity - Severity level (high, medium, low)
 * @returns {Object} Formatted severity dengan label dan icon
 */
export function formatSeverity(severity) {
  const severityMap = {
    high: {
      label: 'Tinggi',
      icon: '🔴',
      class: 'severity-high',
      color: '#e53e3e',
    },
    medium: {
      label: 'Sedang',
      icon: '🟡',
      class: 'severity-medium',
      color: '#d69e2e',
    },
    low: {
      label: 'Rendah',
      icon: '🟢',
      class: 'severity-low',
      color: '#38a169',
    },
  };

  return severityMap[severity] || {
    label: 'Tidak Diketahui',
    icon: '⚪',
    class: 'severity-unknown',
    color: '#a0aec0',
  };
}

/**
 * Export all formatters as default object
 */
export default {
  formatFileSize,
  formatDate,
  formatDateTime,
  formatRelativeTime,
  formatNumber,
  formatCurrency,
  formatPercentage,
  formatConfidence,
  truncateText,
  formatPhoneNumber,
  capitalize,
  titleCase,
  formatDuration,
  formatArrayToSentence,
  slugify,
  parseQueryString,
  objectToQueryString,
  formatSeverity,
};
