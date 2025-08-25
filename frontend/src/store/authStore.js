import { create } from 'zustand';
import { api } from '../lib/api';
import { useToast } from '../context/ToastContext';

const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,

  // Register a new user
  register: async (userData) => {
    set({ loading: true, error: null });
    try {
      const response = await api.post('/register/', userData);
      set({ loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.response?.data?.error || 'Registration failed', loading: false });
      throw error;
    }
  },

  // Login user
  login: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const response = await api.post('/login/', credentials);
      const { token, user } = response.data;
      
      // Store token in localStorage
      localStorage.setItem('token', token);
      
      set({ user, isAuthenticated: true, loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.response?.data?.error || 'Login failed', loading: false });
      throw error;
    }
  },

  // Logout user
  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, isAuthenticated: false });
  },

  // Check authentication status
  checkAuthStatus: async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        // Verify the token with the backend
        const response = await api.get('/verify-token/');
        if (response.data.valid) {
          set({ user: response.data.user, isAuthenticated: true });
        } else {
          localStorage.removeItem('token');
          set({ isAuthenticated: false });
        }
      } catch (error) {
        localStorage.removeItem('token');
        set({ isAuthenticated: false });
      }
    }
  },
}));

export { useAuthStore };