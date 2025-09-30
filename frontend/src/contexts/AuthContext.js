import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext();

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await api.get('/api/v1/me');
      setUser(response);
    } catch (error) {
      console.error('Error al obtener usuario:', error);
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      console.log('🔐 Intentando login con:', { username, password: '***' });
      
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      
      console.log('📤 Enviando datos:', formData.toString());
      
      const response = await api.post('/api/v1/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      console.log('✅ Login exitoso:', response);
      
      const { access_token } = response;
      localStorage.setItem('token', access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      await fetchUser();
      return { success: true };
    } catch (error) {
      console.error('❌ Error en login:', error);
      console.error('❌ Error response:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Error de autenticación' 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
