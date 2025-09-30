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
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // No redirigir automáticamente si estamos en la página de login
      if (!window.location.pathname.includes('/login')) {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Servicios para tareas
export const taskService = {
  getAll: (params = {}) => {
    console.log('🔍 Obteniendo tareas con params:', params);
    return api.get('/api/v1/tasks', { params }).then(response => {
      console.log('📋 Respuesta de tareas:', response);
      console.log('📋 Tipo de respuesta:', typeof response);
      console.log('📋 Es array:', Array.isArray(response));
      if (response && typeof response === 'object' && !Array.isArray(response)) {
        console.log('⚠️ Respuesta no es array, claves:', Object.keys(response));
      }
      return response;
    });
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

// Servicios para empresas
export const companyService = {
  getAll: (params = {}) => api.get('/api/v1/companies/', { params }),
  getById: (id) => api.get(`/api/v1/companies/${id}`),
  create: (data) => api.post('/api/v1/companies/', data),
  update: (id, data) => api.put(`/api/v1/companies/${id}`, data),
  delete: (id) => api.delete(`/api/v1/companies/${id}`),
};

// Servicios para dashboard
export const dashboardService = {
  getStats: (companyId) => api.get('/api/v1/dashboard/stats', { 
    params: companyId ? { company_id: companyId } : {} 
  }),
  getCompanyStats: () => api.get('/api/v1/dashboard/company-stats'),
  getUserTaskStats: (userId) => api.get(`/api/v1/dashboard/user-tasks/${userId}`),
};
