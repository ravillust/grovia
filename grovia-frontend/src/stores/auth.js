import { defineStore } from 'pinia';
import { authAPI } from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    /**
     * Check if user is authenticated
     */
    isAuthenticated: (state) => !!state.token && !!state.user,

    /**
     * Get user full name
     */
    userName: (state) => state.user?.name || '',

    /**
     * Get user email
     */
    userEmail: (state) => state.user?.email || '',

    /**
     * Get user ID
     */
    userId: (state) => state.user?.user_id || null,
  },

  actions: {
    /**
     * Initialize auth state from localStorage
     */
    initAuth() {
      const token = localStorage.getItem('authToken');
      const userStr = localStorage.getItem('authUser');

      if (token && userStr) {
        try {
          this.token = token;
          this.user = JSON.parse(userStr);
        } catch (error) {
          console.error('Failed to parse user data:', error);
          this.clearAuth();
        }
      }
    },

    /**
     * Login user
     * @param {Object} credentials - { email, password }
     */
    async login(credentials) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await authAPI.login(credentials);

        console.log('Login API response:', response);
        console.log('Response data:', response.data);

        // Handle different response structures
        let token, user;

        // Structure 1: { success: true, data: { token, user } }
        if (response.data.success && response.data.data) {
          token = response.data.data.token || response.data.data.access_token;
          user = response.data.data.user;
        }
        // Structure 2: { token, user }
        else if (response.data.token && response.data.user) {
          token = response.data.token;
          user = response.data.user;
        }
        // Structure 3: { access_token, user }
        else if (response.data.access_token) {
          token = response.data.access_token;
          user = response.data.user || {
            email: credentials.email,
            name: response.data.name || credentials.email.split('@')[0]
          };
        }
        // Structure 4: Direct data without wrapper
        else if (response.data.data && response.data.data.token) {
          token = response.data.data.token;
          user = response.data.data.user;
        }
        else {
          console.error('Unexpected response structure:', response.data);
          this.error = 'Format response server tidak valid';
          throw new Error('Invalid response structure');
        }

        if (!token || !user) {
          console.error('Missing token or user:', { token, user });
          this.error = 'Data login tidak lengkap';
          throw new Error('Invalid response structure');
        }

        console.log('Extracted token:', token);
        console.log('Extracted user:', user);

        // Store in state
        this.token = token;
        this.user = user;

        // Persist to localStorage
        localStorage.setItem('authToken', token);
        localStorage.setItem('authUser', JSON.stringify(user));

        console.log('Auth state updated:', {
          token: this.token,
          user: this.user,
          isAuthenticated: this.isAuthenticated
        });

        return { success: true, user };
      } catch (error) {
        console.error('Login error:', error);
        console.error('Error response:', error.response);

        if (error.response?.status === 401) {
          this.error = 'Email atau password salah';
        } else if (error.response?.status === 429) {
          this.error = 'Terlalu banyak percobaan login. Coba lagi nanti.';
        } else if (error.message === 'Invalid response structure') {
          // Error message already set above
        } else {
          this.error = error.response?.data?.message || 'Gagal login. Periksa koneksi internet Anda.';
        }

        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Register new user
     * @param {Object} userData - { full_name, email, username, password, confirm_password }
     */
    async register(userData) {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await authAPI.register(userData);

        console.log('Register API response:', response);
        console.log('Response data:', response.data);

        // Handle different response structures - same as login
        let token, user;

        // Structure 1: { success: true, data: { token, user } }
        if (response.data.success && response.data.data) {
          token = response.data.data.token || response.data.data.access_token;
          user = response.data.data.user;
        }
        // Structure 2: { token, user }
        else if (response.data.token && response.data.user) {
          token = response.data.token;
          user = response.data.user;
        }
        // Structure 3: { access_token, user }
        else if (response.data.access_token) {
          token = response.data.access_token;
          user = response.data.user;
        }

        // Only auto-login if we have token and user
        if (token && user) {
          console.log('Auto-login after registration');
          this.token = token;
          this.user = user;

          // Persist to localStorage
          localStorage.setItem('authToken', token);
          localStorage.setItem('authUser', JSON.stringify(user));
        } else {
          console.log('Registration successful but no auto-login data');
        }

        return { success: true, data: response.data };
      } catch (error) {
        console.error('Register error:', error);

        if (error.response?.status === 400) {
          if (error.response.data.detail) {
            // Handle FastAPI validation errors
            if (Array.isArray(error.response.data.detail)) {
              this.error = error.response.data.detail[0].msg;
            } else {
              this.error = error.response.data.detail;
            }
          } else {
            this.error = error.response.data.message || 'Data registrasi tidak valid';
          }
        } else if (error.response?.status === 409) {
          this.error = 'Email sudah terdaftar';
        } else if (error.response?.status === 422) {
          this.error = 'Format data tidak sesuai';
        } else {
          this.error = error.response?.data?.message || 'Gagal mendaftar. Silakan coba lagi.';
        }

        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Logout user
     */
    async logout() {
      try {
        // Call API to invalidate token on server
        await authAPI.logout();
      } catch (error) {
        console.error('Logout API error:', error);
        // Continue with local logout even if API fails
      } finally {
        this.clearAuth();
      }
    },

    /**
     * Clear authentication data
     */
    clearAuth() {
      this.user = null;
      this.token = null;
      this.error = null;

      localStorage.removeItem('authToken');
      localStorage.removeItem('authUser');
    },

    /**
     * Update user profile
     * @param {Object} userData - Updated user data
     */
    updateUser(userData) {
      this.user = { ...this.user, ...userData };
      localStorage.setItem('authUser', JSON.stringify(this.user));
    },

    /**
     * Clear error message
     */
    clearError() {
      this.error = null;
    },

    /**
     * Check if token is expired
     * @returns {boolean}
     */
    isTokenExpired() {
      if (!this.token) return true;

      try {
        // Decode JWT token (simple base64 decode)
        const payload = JSON.parse(atob(this.token.split('.')[1]));
        const expiry = payload.exp * 1000; // Convert to milliseconds

        return Date.now() >= expiry;
      } catch (error) {
        console.error('Failed to decode token:', error);
        return true;
      }
    },

    /**
     * Refresh authentication if needed
     */
    async refreshAuth() {
      if (this.isTokenExpired()) {
        this.clearAuth();
        return false;
      }
      return true;
    },
  },
});
