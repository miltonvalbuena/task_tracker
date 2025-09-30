import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { User, Lock } from 'lucide-react';
import Logo from '../components/Logo';

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await login(formData.username, formData.password);
      if (result.success) {
        toast.success('Inicio de sesión exitoso');
        navigate('/dashboard');
      } else {
        toast.error(result.error);
      }
    } catch (error) {
      toast.error('Error al iniciar sesión');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: '#f5f5f5',
      padding: '20px'
    }}>
      <div className="card" style={{ 
        width: '450px', 
        maxWidth: '90vw',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        border: 'none',
        borderRadius: '12px'
      }}>
        <div className="card-header" style={{ 
          textAlign: 'center',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          border: 'none',
          borderRadius: '12px 12px 0 0',
          padding: '30px 20px'
        }}>
          <div style={{ 
            margin: '0 auto 20px',
            background: 'rgba(255,255,255,0.1)',
            padding: '20px',
            borderRadius: '12px',
            backdropFilter: 'blur(10px)'
          }}>
            <Logo size="large" style={{ color: 'white' }} />
          </div>
          <h1 style={{ 
            margin: 0, 
            fontSize: '28px', 
            fontWeight: 'bold',
            textShadow: '0 2px 4px rgba(0,0,0,0.3)'
          }}>
            Task Tracker
          </h1>
          <p style={{ 
            margin: '8px 0 0', 
            opacity: 0.9,
            fontSize: '16px'
          }}>
            Sistema de Gestión de Tareas Empresariales
          </p>
        </div>
        
        <div style={{ padding: '30px' }}>
          <form onSubmit={handleSubmit}>
            <div className="form-group" style={{ marginBottom: '20px' }}>
              <label className="form-label" style={{ 
                fontWeight: '600', 
                color: '#333',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center'
              }}>
                <User size={18} style={{ marginRight: '10px', color: '#667eea' }} />
                Usuario
              </label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                className="form-control"
                required
                placeholder="Ingresa tu usuario"
                style={{
                  padding: '12px 16px',
                  border: '2px solid #e1e5e9',
                  borderRadius: '8px',
                  fontSize: '16px',
                  transition: 'border-color 0.3s ease'
                }}
                onFocus={(e) => e.target.style.borderColor = '#667eea'}
                onBlur={(e) => e.target.style.borderColor = '#e1e5e9'}
              />
            </div>
            
            <div className="form-group" style={{ marginBottom: '24px' }}>
              <label className="form-label" style={{ 
                fontWeight: '600', 
                color: '#333',
                marginBottom: '8px',
                display: 'flex',
                alignItems: 'center'
              }}>
                <Lock size={18} style={{ marginRight: '10px', color: '#667eea' }} />
                Contraseña
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="form-control"
                required
                placeholder="Ingresa tu contraseña"
                style={{
                  padding: '12px 16px',
                  border: '2px solid #e1e5e9',
                  borderRadius: '8px',
                  fontSize: '16px',
                  transition: 'border-color 0.3s ease'
                }}
                onFocus={(e) => e.target.style.borderColor = '#667eea'}
                onBlur={(e) => e.target.style.borderColor = '#e1e5e9'}
              />
            </div>
            
            <button
              type="submit"
              className="btn btn-primary"
              style={{ 
                width: '100%', 
                padding: '14px',
                fontSize: '16px',
                fontWeight: '600',
                borderRadius: '8px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                border: 'none',
                boxShadow: '0 4px 12px rgba(102, 126, 234, 0.4)',
                transition: 'transform 0.2s ease, box-shadow 0.2s ease'
              }}
              disabled={loading}
              onMouseOver={(e) => {
                if (!loading) {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 6px 16px rgba(102, 126, 234, 0.5)';
                }
              }}
              onMouseOut={(e) => {
                e.target.style.transform = 'translateY(0)';
                e.target.style.boxShadow = '0 4px 12px rgba(102, 126, 234, 0.4)';
              }}
            >
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <span style={{ 
                    width: '20px', 
                    height: '20px', 
                    border: '2px solid rgba(255,255,255,0.3)',
                    borderTop: '2px solid white',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite',
                    marginRight: '8px'
                  }}></span>
                  Iniciando sesión...
                </span>
              ) : (
                'Iniciar Sesión'
              )}
            </button>
          </form>
        </div>
        
        <div style={{ 
          margin: '0',
          padding: '20px 30px 30px',
          backgroundColor: '#f8f9fa',
          borderRadius: '0 0 12px 12px',
          borderTop: '1px solid #e1e5e9'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            marginBottom: '12px'
          }}>
            <span style={{
              width: '24px',
              height: '24px',
              background: '#667eea',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginRight: '10px',
              fontSize: '12px',
              color: 'white'
            }}>
              ℹ️
            </span>
            <strong style={{ color: '#333', fontSize: '14px' }}>
              Credenciales de Prueba
            </strong>
          </div>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: '1fr 1fr', 
            gap: '12px',
            fontSize: '13px'
          }}>
            <div style={{
              padding: '12px',
              background: 'white',
              borderRadius: '8px',
              border: '1px solid #e1e5e9'
            }}>
              <div style={{ fontWeight: '600', color: '#667eea', marginBottom: '4px' }}>
                👑 Administrador
              </div>
              <div style={{ color: '#666' }}>
                <strong>Usuario:</strong> admin<br />
                <strong>Contraseña:</strong> admin123
              </div>
            </div>
            
            <div style={{
              padding: '12px',
              background: 'white',
              borderRadius: '8px',
              border: '1px solid #e1e5e9'
            }}>
              <div style={{ fontWeight: '600', color: '#28a745', marginBottom: '4px' }}>
                👥 Usuarios
              </div>
              <div style={{ color: '#666' }}>
                <strong>Empresa:</strong> COLMENA ARL<br />
                <strong>Contraseña:</strong> password123
              </div>
            </div>
          </div>
          
          <div style={{
            marginTop: '12px',
            padding: '8px 12px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: '6px',
            fontSize: '12px',
            textAlign: 'center'
          }}>
            💡 <strong>Tip:</strong> Accede como admin para ver todas las empresas y tareas
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
