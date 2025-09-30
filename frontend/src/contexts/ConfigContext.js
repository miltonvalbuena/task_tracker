import React, { createContext, useContext, useState, useEffect } from 'react';

const ConfigContext = createContext();

export const useConfig = () => {
  const context = useContext(ConfigContext);
  if (!context) {
    throw new Error('useConfig must be used within a ConfigProvider');
  }
  return context;
};

export const ConfigProvider = ({ children }) => {
  const [config, setConfig] = useState({
    // Configuración del logo
    logo: {
      companyName: 'Ko-Actuar',
      tagline: 'SISTEMAS DE GESTIÓN',
      primaryColor: '#28a745',
      secondaryColor: '#333'
    },
    // Configuración de la empresa
    company: {
      name: 'Ko-Actuar',
      nit: '',
      address: '',
      phone: '',
      email: '',
      website: ''
    },
    // Configuración del sistema
    system: {
      timezone: 'America/Bogota',
      language: 'es',
      maxUsers: 100,
      sessionTimeout: 30
    }
  });

  // Cargar configuración desde localStorage al inicializar
  useEffect(() => {
    const savedConfig = localStorage.getItem('systemConfig');
    if (savedConfig) {
      try {
        const parsedConfig = JSON.parse(savedConfig);
        setConfig(prevConfig => ({
          ...prevConfig,
          ...parsedConfig
        }));
      } catch (error) {
        console.error('Error loading config from localStorage:', error);
      }
    }
  }, []);

  // Guardar configuración en localStorage cuando cambie
  const updateConfig = (newConfig) => {
    setConfig(prevConfig => {
      const updatedConfig = {
        ...prevConfig,
        ...newConfig
      };
      localStorage.setItem('systemConfig', JSON.stringify(updatedConfig));
      return updatedConfig;
    });
  };

  // Actualizar configuración del logo
  const updateLogoConfig = (logoConfig) => {
    updateConfig({
      logo: {
        ...config.logo,
        ...logoConfig
      }
    });
  };

  // Actualizar configuración de la empresa
  const updateCompanyConfig = (companyConfig) => {
    updateConfig({
      company: {
        ...config.company,
        ...companyConfig
      }
    });
  };

  // Actualizar configuración del sistema
  const updateSystemConfig = (systemConfig) => {
    updateConfig({
      system: {
        ...config.system,
        ...systemConfig
      }
    });
  };

  const value = {
    config,
    updateConfig,
    updateLogoConfig,
    updateCompanyConfig,
    updateSystemConfig
  };

  return (
    <ConfigContext.Provider value={value}>
      {children}
    </ConfigContext.Provider>
  );
};





