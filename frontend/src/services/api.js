import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Servicios para tareas
export const taskService = {
  getAll: (params = {}) => api.get('/api/v1/tasks', { params }),
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
