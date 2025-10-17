import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { User, Lock, Eye, EyeOff, Shield, Users, BarChart3, FileText } from 'lucide-react';
import Logo from '../components/Logo';

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
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
      width: '100vw',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
      padding: '0',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Elementos decorativos de fondo */}
      <div style={{
        position: 'absolute',
        top: '-50%',
        left: '-50%',
        width: '200%',
        height: '200%',
        background: 'radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px)',
        backgroundSize: '50px 50px',
        animation: 'float 20s ease-in-out infinite',
        zIndex: 0
      }}></div>
      
      <div style={{
        position: 'absolute',
        top: '10%',
        right: '10%',
        width: '300px',
        height: '300px',
        background: 'linear-gradient(45deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05))',
        borderRadius: '50%',
        filter: 'blur(40px)',
        zIndex: 0
      }}></div>
      
      <div style={{
        position: 'absolute',
        bottom: '10%',
        left: '10%',
        width: '200px',
        height: '200px',
        background: 'linear-gradient(45deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05))',
        borderRadius: '50%',
        filter: 'blur(30px)',
        zIndex: 0
      }}></div>

      <div style={{ 
        position: 'relative',
        zIndex: 1,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        padding: '0'
      }}>
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(20px)',
          borderRadius: '0',
          boxShadow: '0 25px 50px rgba(0, 0, 0, 0.15)',
          overflow: 'hidden',
          width: '100%',
          height: '100vh',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr'
        }}>
          {/* Columna izquierda - Información */}
          <div style={{ 
            background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
            color: 'white',
            padding: '60px 50px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            position: 'relative'
          }}>
            <div style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'url("data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.05"%3E%3Ccircle cx="30" cy="30" r="2"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
              opacity: 0.3
            }}></div>
            
            <div style={{ 
              position: 'relative',
              zIndex: 2,
              margin: '0 auto 40px',
              background: 'rgba(255,255,255,0.15)',
              padding: '40px',
              borderRadius: '20px',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255,255,255,0.2)'
            }}>
              <Logo size="large" style={{ color: 'white' }} />
            </div>
            
            <div style={{ position: 'relative', zIndex: 2 }}>
              <h1 style={{ 
                margin: 0, 
                fontSize: '42px', 
                fontWeight: '800',
                textShadow: '0 4px 8px rgba(0,0,0,0.3)',
                marginBottom: '20px',
                background: 'linear-gradient(45deg, #ffffff, #f0f0f0)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                Task Tracker
              </h1>
              <p style={{ 
                margin: '0', 
                opacity: 0.95,
                fontSize: '20px',
                lineHeight: '1.6',
                fontWeight: '300'
              }}>
                Sistema de Gestión de Tareas Empresariales
              </p>
            </div>
            
            <div style={{
              position: 'relative',
              zIndex: 2,
              marginTop: '50px',
              padding: '30px',
              background: 'rgba(255,255,255,0.1)',
              borderRadius: '16px',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255,255,255,0.2)',
              width: '100%'
            }}>
              <h3 style={{ margin: '0 0 24px', fontSize: '22px', fontWeight: '600' }}>
                🚀 Características Principales
              </h3>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: '1fr 1fr', 
                gap: '16px',
                textAlign: 'left'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
                  <Shield size={20} style={{ marginRight: '12px', color: '#4ade80' }} />
                  <span>Gestión de tareas por cliente</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
                  <Users size={20} style={{ marginRight: '12px', color: '#4ade80' }} />
                  <span>Seguimiento de ARL</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
                  <BarChart3 size={20} style={{ marginRight: '12px', color: '#4ade80' }} />
                  <span>Dashboard en tiempo real</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
                  <FileText size={20} style={{ marginRight: '12px', color: '#4ade80' }} />
                  <span>Reportes detallados</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Columna derecha - Formulario */}
          <div style={{ 
            padding: '60px 50px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            background: 'white',
            position: 'relative'
          }}>
            <div style={{
              position: 'absolute',
              top: '20px',
              right: '20px',
              width: '100px',
              height: '100px',
              background: 'linear-gradient(45deg, #3b82f6, #1d4ed8)',
              borderRadius: '50%',
              opacity: 0.1,
              filter: 'blur(20px)'
            }}></div>
            
            <div style={{ position: 'relative', zIndex: 2 }}>
              <h2 style={{ 
                margin: '0 0 30px', 
                fontSize: '32px', 
                fontWeight: '700',
                color: '#1a202c',
                textAlign: 'center',
                background: 'linear-gradient(135deg, #0f172a, #1e293b)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                Iniciar Sesión
              </h2>
              
              <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '24px' }}>
                  <label style={{ 
                    fontWeight: '600', 
                    color: '#2d3748',
                    marginBottom: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    fontSize: '16px'
                  }}>
                    <User size={20} style={{ marginRight: '12px', color: '#3b82f6' }} />
                    Usuario
                  </label>
                  <div style={{ position: 'relative' }}>
                    <input
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      required
                      placeholder="Ingresa tu usuario"
                      style={{
                        padding: '18px 20px',
                        border: '2px solid #e2e8f0',
                        borderRadius: '12px',
                        fontSize: '16px',
                        transition: 'all 0.3s ease',
                        width: '100%',
                        background: '#f8fafc',
                        outline: 'none'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#3b82f6';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e2e8f0';
                        e.target.style.background = '#f8fafc';
                        e.target.style.boxShadow = 'none';
                      }}
                    />
                  </div>
                </div>
                
                <div style={{ marginBottom: '32px' }}>
                  <label style={{ 
                    fontWeight: '600', 
                    color: '#2d3748',
                    marginBottom: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    fontSize: '16px'
                  }}>
                    <Lock size={20} style={{ marginRight: '12px', color: '#3b82f6' }} />
                    Contraseña
                  </label>
                  <div style={{ position: 'relative' }}>
                    <input
                      type={showPassword ? "text" : "password"}
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      placeholder="Ingresa tu contraseña"
                      style={{
                        padding: '18px 50px 18px 20px',
                        border: '2px solid #e2e8f0',
                        borderRadius: '12px',
                        fontSize: '16px',
                        transition: 'all 0.3s ease',
                        width: '100%',
                        background: '#f8fafc',
                        outline: 'none'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#3b82f6';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e2e8f0';
                        e.target.style.background = '#f8fafc';
                        e.target.style.boxShadow = 'none';
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      style={{
                        position: 'absolute',
                        right: '15px',
                        top: '50%',
                        transform: 'translateY(-50%)',
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        color: '#a0aec0',
                        padding: '4px'
                      }}
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                </div>
                
                <button
                  type="submit"
                  style={{ 
                    width: '100%', 
                    padding: '18px',
                    fontSize: '16px',
                    fontWeight: '700',
                    borderRadius: '12px',
                    background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                    border: 'none',
                    boxShadow: '0 8px 25px rgba(59, 130, 246, 0.4)',
                    transition: 'all 0.3s ease',
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                    color: 'white',
                    cursor: 'pointer',
                    position: 'relative',
                    overflow: 'hidden'
                  }}
                  disabled={loading}
                  onMouseEnter={(e) => {
                    if (!loading) {
                      e.currentTarget.style.transform = 'translateY(-2px)';
                      e.currentTarget.style.boxShadow = '0 12px 35px rgba(59, 130, 246, 0.5)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '0 8px 25px rgba(59, 130, 246, 0.4)';
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
              
              {/* Credenciales de Prueba */}
              <div style={{ 
                marginTop: '40px',
                padding: '24px',
                backgroundColor: '#f7fafc',
                borderRadius: '16px',
                border: '1px solid #e2e8f0',
                position: 'relative'
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  marginBottom: '20px'
                }}>
                  <div style={{
                    width: '32px',
                    height: '32px',
                    background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginRight: '12px',
                    fontSize: '16px',
                    color: 'white'
                  }}>
                    ℹ️
                  </div>
                  <strong style={{ color: '#2d3748', fontSize: '16px', fontWeight: '700' }}>
                    Credenciales de Prueba
                  </strong>
                </div>
                
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: '1fr 1fr', 
                  gap: '16px',
                  marginBottom: '20px'
                }}>
                  <div style={{
                    padding: '16px',
                    background: 'white',
                    borderRadius: '12px',
                    border: '2px solid #3b82f6',
                    boxShadow: '0 4px 12px rgba(59, 130, 246, 0.1)',
                    transition: 'transform 0.2s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
                  onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
                  >
                    <div style={{ 
                      fontWeight: '700', 
                      color: '#3b82f6', 
                      marginBottom: '8px',
                      fontSize: '14px',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      👑 Administrador
                    </div>
                    <div style={{ color: '#2d3748', lineHeight: '1.5', fontSize: '14px' }}>
                      <div style={{ marginBottom: '4px' }}>
                        <strong>Usuario:</strong> admin
                      </div>
                      <div>
                        <strong>Contraseña:</strong> admin123
                      </div>
                    </div>
                  </div>
                  
                  <div style={{
                    padding: '16px',
                    background: 'white',
                    borderRadius: '12px',
                    border: '2px solid #48bb78',
                    boxShadow: '0 4px 12px rgba(72, 187, 120, 0.1)',
                    transition: 'transform 0.2s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
                  onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
                  >
                    <div style={{ 
                      fontWeight: '700', 
                      color: '#48bb78', 
                      marginBottom: '8px',
                      fontSize: '14px',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      👥 Usuarios
                    </div>
                    <div style={{ color: '#2d3748', lineHeight: '1.5', fontSize: '14px' }}>
                      <div style={{ marginBottom: '4px' }}>
                        <strong>Empresa:</strong> COLMENA ARL
                      </div>
                      <div>
                        <strong>Contraseña:</strong> user123
                      </div>
                    </div>
                  </div>
                </div>
                
                <div style={{
                  padding: '12px',
                  background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                  color: 'white',
                  borderRadius: '12px',
                  fontSize: '13px',
                  textAlign: 'center',
                  fontWeight: '500'
                }}>
                  💡 <strong>Tip:</strong> Accede como admin para ver todas las empresas y tareas
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(180deg); }
        }
      `}</style>
    </div>
  );
}

export default Login;
