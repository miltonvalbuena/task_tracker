import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useAuth } from '../contexts/AuthContext';
import { useConfig } from '../contexts/ConfigContext';
import { companyService } from '../services/api';
import toast from 'react-hot-toast';
import { Save, Settings, Database, Building, Shield, Users, Palette } from 'lucide-react';
import Logo from '../components/Logo';

function SystemConfig() {
  const { user } = useAuth();
  const { config, updateLogoConfig, updateCompanyConfig, updateSystemConfig } = useConfig();
  const queryClient = useQueryClient();

  const [systemConfig, setSystemConfig] = useState({
    company_name: config.company.name,
    company_nit: config.company.nit,
    company_address: config.company.address,
    company_phone: config.company.phone,
    company_email: config.company.email,
    company_website: config.company.website,
    database_host: '',
    database_port: '',
    database_name: '',
    database_user: '',
    system_timezone: config.system.timezone,
    system_language: config.system.language,
    max_users: config.system.maxUsers,
    session_timeout: config.system.sessionTimeout,
    backup_enabled: true,
    backup_frequency: 'daily',
    email_notifications: true,
    smtp_server: '',
    smtp_port: 587,
    smtp_user: '',
    smtp_password: '',
    system_maintenance_mode: false,
    // Configuración del logo
    logo_company_name: config.logo.companyName,
    logo_tagline: config.logo.tagline,
    logo_primary_color: config.logo.primaryColor,
    logo_secondary_color: config.logo.secondaryColor
  });

  const [activeTab, setActiveTab] = useState('logo');

  // Solo permitir acceso a administradores
  if (user?.role !== 'admin') {
    return (
      <div style={{ 
        width: '100%', 
        padding: '20px',
        background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{
          background: 'white',
          padding: '40px',
          borderRadius: '16px',
          boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
          textAlign: 'center',
          maxWidth: '500px'
        }}>
          <Shield size={64} style={{ color: '#dc3545', marginBottom: '20px' }} />
          <h2 style={{ color: '#dc3545', marginBottom: '16px' }}>Acceso Denegado</h2>
          <p style={{ color: '#6c757d', fontSize: '16px' }}>
            Solo los administradores pueden acceder a la configuración del sistema.
          </p>
        </div>
      </div>
    );
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSystemConfig(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Actualizar configuración del logo
    updateLogoConfig({
      companyName: systemConfig.logo_company_name,
      tagline: systemConfig.logo_tagline,
      primaryColor: systemConfig.logo_primary_color,
      secondaryColor: systemConfig.logo_secondary_color
    });
    
    // Actualizar configuración de la empresa
    updateCompanyConfig({
      name: systemConfig.company_name,
      nit: systemConfig.company_nit,
      address: systemConfig.company_address,
      phone: systemConfig.company_phone,
      email: systemConfig.company_email,
      website: systemConfig.company_website
    });
    
    // Actualizar configuración del sistema
    updateSystemConfig({
      timezone: systemConfig.system_timezone,
      language: systemConfig.system_language,
      maxUsers: systemConfig.max_users,
      sessionTimeout: systemConfig.session_timeout
    });
    
    toast.success('Configuración del sistema guardada exitosamente');
  };

  const tabs = [
    { id: 'logo', label: 'Logo', icon: Palette },
    { id: 'company', label: 'Empresa', icon: Building },
    { id: 'database', label: 'Base de Datos', icon: Database },
    { id: 'system', label: 'Sistema', icon: Settings },
    { id: 'users', label: 'Usuarios', icon: Users }
  ];

  return (
    <div style={{ 
      width: '100%', 
      padding: '20px',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      minHeight: '100vh'
    }}>
      {/* Header */}
      <div style={{ 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '24px',
        borderRadius: '12px',
        marginBottom: '30px',
        boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <Settings size={32} />
          <div>
            <h1 style={{ margin: 0, fontSize: '28px', fontWeight: 'bold' }}>
              Configuración del Sistema
            </h1>
            <p style={{ margin: '4px 0 0', opacity: 0.9, fontSize: '14px' }}>
              Configuración administrativa del sistema y la empresa
            </p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '0',
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        marginBottom: '20px'
      }}>
        <div style={{
          display: 'flex',
          borderBottom: '2px solid #f8f9fa',
          overflowX: 'auto'
        }}>
          {tabs.map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  background: 'none',
                  border: 'none',
                  padding: '16px 24px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  color: activeTab === tab.id ? '#007bff' : '#6c757d',
                  borderBottom: activeTab === tab.id ? '3px solid #007bff' : '3px solid transparent',
                  transition: 'all 0.3s ease',
                  whiteSpace: 'nowrap'
                }}
                onMouseOver={(e) => {
                  if (activeTab !== tab.id) {
                    e.target.style.color = '#007bff';
                    e.target.style.background = '#f8f9fa';
                  }
                }}
                onMouseOut={(e) => {
                  if (activeTab !== tab.id) {
                    e.target.style.color = '#6c757d';
                    e.target.style.background = 'none';
                  }
                }}
              >
                <Icon size={20} />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Tab Content */}
        <div style={{ padding: '32px' }}>
          <form onSubmit={handleSubmit}>
            {activeTab === 'logo' && (
              <div>
                <h2 style={{ 
                  color: '#333', 
                  marginBottom: '24px', 
                  fontSize: '20px',
                  fontWeight: '600',
                  borderBottom: '3px solid #6f42c1',
                  paddingBottom: '8px'
                }}>
                  Configuración del Logo
                </h2>
                
                {/* Vista previa del logo */}
                <div style={{
                  background: '#f8f9fa',
                  padding: '24px',
                  borderRadius: '12px',
                  marginBottom: '24px',
                  textAlign: 'center',
                  border: '2px solid #e9ecef'
                }}>
                  <h3 style={{ marginBottom: '16px', color: '#6c757d' }}>Vista Previa del Logo</h3>
                  <Logo size="large" />
                </div>
                
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
                  gap: '24px' 
                }}>
                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Nombre de la Empresa *
                    </label>
                    <input
                      type="text"
                      name="logo_company_name"
                      value={systemConfig.logo_company_name}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#6f42c1';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(111,66,193,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      required
                      placeholder="Nombre de la empresa"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Tagline / Eslogan
                    </label>
                    <input
                      type="text"
                      name="logo_tagline"
                      value={systemConfig.logo_tagline}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#6f42c1';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(111,66,193,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="SISTEMAS DE GESTIÓN"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Color Principal
                    </label>
                    <input
                      type="color"
                      name="logo_primary_color"
                      value={systemConfig.logo_primary_color}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        height: '48px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                      }}
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Color Secundario
                    </label>
                    <input
                      type="color"
                      name="logo_secondary_color"
                      value={systemConfig.logo_secondary_color}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        height: '48px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                      }}
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'company' && (
              <div>
                <h2 style={{ 
                  color: '#333', 
                  marginBottom: '24px', 
                  fontSize: '20px',
                  fontWeight: '600',
                  borderBottom: '3px solid #007bff',
                  paddingBottom: '8px'
                }}>
                  Información de la Empresa
                </h2>
                
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
                  gap: '24px' 
                }}>
                  <div style={{ gridColumn: '1 / -1' }}>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Nombre de la Empresa *
                    </label>
                    <input
                      type="text"
                      name="company_name"
                      value={systemConfig.company_name}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#007bff';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0,123,255,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      required
                      placeholder="Nombre de la empresa donde está instalado el software"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      NIT
                    </label>
                    <input
                      type="text"
                      name="company_nit"
                      value={systemConfig.company_nit}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#007bff';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0,123,255,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="Número de identificación tributaria"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Teléfono
                    </label>
                    <input
                      type="tel"
                      name="company_phone"
                      value={systemConfig.company_phone}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#007bff';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0,123,255,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="Número de teléfono"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Email
                    </label>
                    <input
                      type="email"
                      name="company_email"
                      value={systemConfig.company_email}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#007bff';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0,123,255,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="Correo electrónico"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Sitio Web
                    </label>
                    <input
                      type="url"
                      name="company_website"
                      value={systemConfig.company_website}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#007bff';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0,123,255,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="https://www.empresa.com"
                    />
                  </div>

                  <div style={{ gridColumn: '1 / -1' }}>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Dirección
                    </label>
                    <textarea
                      name="company_address"
                      value={systemConfig.company_address}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        minHeight: '100px',
                        resize: 'vertical',
                        fontFamily: 'inherit',
                        lineHeight: '1.5',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#007bff';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(0,123,255,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="Dirección completa de la empresa"
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'database' && (
              <div>
                <h2 style={{ 
                  color: '#333', 
                  marginBottom: '24px', 
                  fontSize: '20px',
                  fontWeight: '600',
                  borderBottom: '3px solid #28a745',
                  paddingBottom: '8px'
                }}>
                  Configuración de Base de Datos
                </h2>
                
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
                  gap: '24px' 
                }}>
                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Host de Base de Datos
                    </label>
                    <input
                      type="text"
                      name="database_host"
                      value={systemConfig.database_host}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#28a745';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(40,167,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="localhost"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Puerto
                    </label>
                    <input
                      type="number"
                      name="database_port"
                      value={systemConfig.database_port}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#28a745';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(40,167,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="5432"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Nombre de la Base de Datos
                    </label>
                    <input
                      type="text"
                      name="database_name"
                      value={systemConfig.database_name}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#28a745';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(40,167,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="tasktracker_db"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Usuario de Base de Datos
                    </label>
                    <input
                      type="text"
                      name="database_user"
                      value={systemConfig.database_user}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#28a745';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(40,167,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="postgres"
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'system' && (
              <div>
                <h2 style={{ 
                  color: '#333', 
                  marginBottom: '24px', 
                  fontSize: '20px',
                  fontWeight: '600',
                  borderBottom: '3px solid #ffc107',
                  paddingBottom: '8px'
                }}>
                  Configuración del Sistema
                </h2>
                
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
                  gap: '24px' 
                }}>
                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Zona Horaria
                    </label>
                    <select
                      name="system_timezone"
                      value={systemConfig.system_timezone}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#ffc107';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(255,193,7,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                    >
                      <option value="America/Bogota">Bogotá (UTC-5)</option>
                      <option value="America/Mexico_City">México (UTC-6)</option>
                      <option value="America/New_York">Nueva York (UTC-5)</option>
                      <option value="Europe/Madrid">Madrid (UTC+1)</option>
                    </select>
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Idioma del Sistema
                    </label>
                    <select
                      name="system_language"
                      value={systemConfig.system_language}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#ffc107';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(255,193,7,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                    >
                      <option value="es">Español</option>
                      <option value="en">English</option>
                      <option value="pt">Português</option>
                    </select>
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Máximo de Usuarios
                    </label>
                    <input
                      type="number"
                      name="max_users"
                      value={systemConfig.max_users}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#ffc107';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(255,193,7,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      min="1"
                      max="1000"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Timeout de Sesión (minutos)
                    </label>
                    <input
                      type="number"
                      name="session_timeout"
                      value={systemConfig.session_timeout}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#ffc107';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(255,193,7,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      min="5"
                      max="480"
                    />
                  </div>

                  <div style={{ gridColumn: '1 / -1' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '16px',
                      background: '#f8f9fa',
                      borderRadius: '8px',
                      border: '2px solid #e1e5e9'
                    }}>
                      <input
                        type="checkbox"
                        name="system_maintenance_mode"
                        checked={systemConfig.system_maintenance_mode}
                        onChange={handleChange}
                        style={{
                          width: '20px',
                          height: '20px',
                          cursor: 'pointer'
                        }}
                      />
                      <div>
                        <label style={{
                          fontWeight: '600',
                          color: '#333',
                          fontSize: '16px',
                          cursor: 'pointer'
                        }}>
                          Modo de Mantenimiento
                        </label>
                        <p style={{
                          margin: '4px 0 0',
                          color: '#6c757d',
                          fontSize: '14px'
                        }}>
                          Activar para realizar mantenimiento del sistema
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'users' && (
              <div>
                <h2 style={{ 
                  color: '#333', 
                  marginBottom: '24px', 
                  fontSize: '20px',
                  fontWeight: '600',
                  borderBottom: '3px solid #dc3545',
                  paddingBottom: '8px'
                }}>
                  Configuración de Usuarios
                </h2>
                
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
                  gap: '24px' 
                }}>
                  <div style={{ gridColumn: '1 / -1' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '16px',
                      background: '#f8f9fa',
                      borderRadius: '8px',
                      border: '2px solid #e1e5e9',
                      marginBottom: '16px'
                    }}>
                      <input
                        type="checkbox"
                        name="email_notifications"
                        checked={systemConfig.email_notifications}
                        onChange={handleChange}
                        style={{
                          width: '20px',
                          height: '20px',
                          cursor: 'pointer'
                        }}
                      />
                      <div>
                        <label style={{
                          fontWeight: '600',
                          color: '#333',
                          fontSize: '16px',
                          cursor: 'pointer'
                        }}>
                          Notificaciones por Email
                        </label>
                        <p style={{
                          margin: '4px 0 0',
                          color: '#6c757d',
                          fontSize: '14px'
                        }}>
                          Enviar notificaciones por correo electrónico
                        </p>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Servidor SMTP
                    </label>
                    <input
                      type="text"
                      name="smtp_server"
                      value={systemConfig.smtp_server}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#dc3545';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(220,53,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="smtp.gmail.com"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Puerto SMTP
                    </label>
                    <input
                      type="number"
                      name="smtp_port"
                      value={systemConfig.smtp_port}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#dc3545';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(220,53,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="587"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Usuario SMTP
                    </label>
                    <input
                      type="email"
                      name="smtp_user"
                      value={systemConfig.smtp_user}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#dc3545';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(220,53,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="usuario@empresa.com"
                    />
                  </div>

                  <div>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      Contraseña SMTP
                    </label>
                    <input
                      type="password"
                      name="smtp_password"
                      value={systemConfig.smtp_password}
                      onChange={handleChange}
                      style={{
                        width: '100%',
                        padding: '12px 16px',
                        border: '2px solid #e1e5e9',
                        borderRadius: '8px',
                        fontSize: '16px',
                        background: '#fafbfc',
                        transition: 'all 0.3s ease'
                      }}
                      onFocus={(e) => {
                        e.target.style.borderColor = '#dc3545';
                        e.target.style.background = 'white';
                        e.target.style.boxShadow = '0 0 0 3px rgba(220,53,69,0.1)';
                      }}
                      onBlur={(e) => {
                        e.target.style.borderColor = '#e1e5e9';
                        e.target.style.background = '#fafbfc';
                        e.target.style.boxShadow = 'none';
                      }}
                      placeholder="Contraseña del email"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Botones de acción */}
            <div style={{ 
              display: 'flex', 
              gap: '16px', 
              justifyContent: 'flex-end', 
              marginTop: '32px',
              paddingTop: '24px',
              borderTop: '2px solid #f8f9fa'
            }}>
              <button
                type="submit"
                style={{
                  background: 'linear-gradient(135deg, #007bff 0%, #0056b3 100%)',
                  color: 'white',
                  border: 'none',
                  padding: '12px 24px',
                  borderRadius: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  boxShadow: '0 4px 15px rgba(0,123,255,0.3)'
                }}
                onMouseOver={(e) => {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 6px 20px rgba(0,123,255,0.4)';
                }}
                onMouseOut={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = '0 4px 15px rgba(0,123,255,0.3)';
                }}
              >
                <Save size={16} />
                Guardar Configuración
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SystemConfig;
