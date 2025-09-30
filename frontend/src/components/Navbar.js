import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LogOut, User } from 'lucide-react';
import Logo from './Logo';

function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div style={{ width: '100%', padding: '0 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link to="/dashboard" className="navbar-brand" style={{ 
            display: 'flex', 
            alignItems: 'center', 
            textDecoration: 'none',
            color: 'inherit'
          }}>
            <Logo size="small" />
          </Link>
          
          <ul className="navbar-nav">
            <li>
              <Link 
                to="/dashboard" 
                className={isActive('/dashboard') ? 'active' : ''}
              >
                Dashboard
              </Link>
            </li>
            <li>
              <Link 
                to="/tasks" 
                className={isActive('/tasks') ? 'active' : ''}
              >
                Tareas
              </Link>
            </li>
            <li>
              <Link 
                to="/users" 
                className={isActive('/users') ? 'active' : ''}
              >
                Usuarios
              </Link>
            </li>
            {user?.role === 'admin' && (
              <>
                <li>
                  <Link 
                    to="/companies" 
                    className={isActive('/companies') ? 'active' : ''}
                  >
                    Empresas
                  </Link>
                </li>
                <li>
                  <Link 
                    to="/system-config" 
                    className={isActive('/system-config') ? 'active' : ''}
                  >
                    Configuración
                  </Link>
                </li>
              </>
            )}
            <li>
              <Link 
                to="/reports" 
                className={isActive('/reports') ? 'active' : ''}
              >
                Reportes
              </Link>
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <User size={16} />
              <span>{user?.full_name}</span>
              <button 
                onClick={logout}
                className="btn btn-secondary"
                style={{ padding: '4px 8px', fontSize: '12px' }}
              >
                <LogOut size={14} />
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
