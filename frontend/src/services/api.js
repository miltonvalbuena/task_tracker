import axios from 'axios';

// Determinar la URL base según el entorno
const getBaseURL = () => {
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // En producción (Railway), usar URL relativa
  if (process.env.NODE_ENV === 'production') {
    return '';
  }
  
  // En desarrollo, usar localhost
  return 'http://localhost:8000';
};

export const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response?.status === 401) {
      // No redirigir automáticamente si estamos en la página de login
      if (!window.location.pathname.includes('/login')) {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        window.location.href = '/login';
      }
    }
    // Mantener la estructura del error para que los componentes puedan acceder a response.data
    return Promise.reject(error);
  }
);

// Servicios para tareas
export const taskService = {
  getAll: (params = {}) => {
    return api.get('/api/v1/tasks', { params });
  },
  getById: (id) => api.get(`/api/v1/tasks/${id}`),
  create: (data) => api.post('/api/v1/tasks', data),
  update: (id, data) => api.put(`/api/v1/tasks/${id}`, data),
  delete: (id) => api.delete(`/api/v1/tasks/${id}`),
};

// Servicios para usuarios
export const userService = {
  getAll: (params = {}) => api.get('/api/v1/users/', { params }),
  getById: (id) => api.get(`/api/v1/users/${id}`),
  create: (data) => api.post('/api/v1/users/', data),
  update: (id, data) => api.put(`/api/v1/users/${id}`, data),
  delete: (id) => api.delete(`/api/v1/users/${id}`),
};

// Servicios para clientes
export const clientService = {
  getAll: (params = {}) => api.get('/api/v1/clients/', { params }),
  getById: (id) => api.get(`/api/v1/clients/${id}`),
  create: (data) => api.post('/api/v1/clients/', data),
  update: (id, data) => api.put(`/api/v1/clients/${id}`, data),
  delete: (id) => api.delete(`/api/v1/clients/${id}`),
};

// Servicios para ARL
export const arlService = {
  getAll: () => api.get('/api/v1/arls'),
  getById: (id) => api.get(`/api/v1/arls/${id}`),
  create: (data) => api.post('/api/v1/arls', data),
  update: (id, data) => api.put(`/api/v1/arls/${id}`, data),
  delete: (id) => api.delete(`/api/v1/arls/${id}`),
};

// Servicios para dashboard
export const dashboardService = {
  getStats: (clientId) => api.get('/api/v1/dashboard/stats', { 
    params: clientId ? { client_id: clientId } : {} 
  }),
  getClientStats: () => api.get('/api/v1/dashboard/client-stats'),
  getUserTaskStats: (userId) => api.get(`/api/v1/dashboard/user-tasks/${userId}`),
};
