import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useAuth } from '../contexts/AuthContext';
import { userService, companyService } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit, Trash2, User as UserIcon } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

function Users() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
    password: '',
    role: 'user',
    company_id: user?.company_id || '',
  });

  const { data: users, isLoading } = useQuery(
    'users',
    () => userService.getAll(),
    {
      enabled: !!user,
    }
  );

  const { data: companies } = useQuery(
    'companies',
    () => companyService.getAll(),
    {
      enabled: user?.role === 'admin',
    }
  );

  const createMutation = useMutation(
    (data) => userService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('users');
        toast.success('Usuario creado exitosamente');
        resetForm();
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Error al crear el usuario');
      },
    }
  );

  const updateMutation = useMutation(
    (data) => userService.update(editingUser.id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('users');
        toast.success('Usuario actualizado exitosamente');
        resetForm();
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Error al actualizar el usuario');
      },
    }
  );

  const deleteMutation = useMutation(
    (id) => userService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('users');
        toast.success('Usuario eliminado exitosamente');
      },
      onError: () => {
        toast.error('Error al eliminar el usuario');
      },
    }
  );

  const resetForm = () => {
    setFormData({
      email: '',
      username: '',
      full_name: '',
      password: '',
      role: 'user',
      company_id: user?.company_id || '',
    });
    setShowForm(false);
    setEditingUser(null);
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    setFormData({
      email: user.email,
      username: user.username,
      full_name: user.full_name,
      password: '',
      role: user.role,
      company_id: user.company_id,
    });
    setShowForm(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const submitData = {
      ...formData,
      company_id: parseInt(formData.company_id),
    };

    // No enviar password vacío en actualizaciones
    if (editingUser && !submitData.password) {
      delete submitData.password;
    }

    if (editingUser) {
      updateMutation.mutate(submitData);
    } else {
      createMutation.mutate(submitData);
    }
  };

  const getRoleBadge = (role) => {
    const roleMap = {
      admin: 'badge-danger',
      manager: 'badge-warning',
      user: 'badge-secondary',
    };
    return `badge ${roleMap[role] || 'badge-secondary'}`;
  };

  if (isLoading) {
    return <div className="loading">Cargando usuarios...</div>;
  }

  return (
    <div style={{ width: '100%', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Usuarios</h1>
        <button 
          onClick={() => setShowForm(true)}
          className="btn btn-primary"
        >
          <Plus size={16} style={{ marginRight: '8px' }} />
          Nuevo Usuario
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '24px' }}>
          <div className="card-header">
            <h3 className="card-title">
              {editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}
            </h3>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Email *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="form-control"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Usuario *</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  className="form-control"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Nombre Completo *</label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleChange}
                  className="form-control"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">
                  Contraseña {editingUser ? '(dejar vacío para mantener)' : '*'}
                </label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="form-control"
                  required={!editingUser}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Rol</label>
                <select
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  className="form-control"
                >
                  <option value="user">Usuario</option>
                  <option value="manager">Manager</option>
                  {user?.role === 'admin' && (
                    <option value="admin">Administrador</option>
                  )}
                </select>
              </div>

              {user?.role === 'admin' && (
                <div className="form-group">
                  <label className="form-label">Empresa *</label>
                  <select
                    name="company_id"
                    value={formData.company_id}
                    onChange={handleChange}
                    className="form-control"
                    required
                  >
                    <option value="">Seleccionar empresa</option>
                    {Array.isArray(companies) && companies.map(company => (
                      <option key={company.id} value={company.id}>
                        {company.name}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '16px' }}>
              <button
                type="button"
                onClick={resetForm}
                className="btn btn-secondary"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={createMutation.isLoading || updateMutation.isLoading}
              >
                {editingUser ? 'Actualizar' : 'Crear'}
              </button>
            </div>
          </form>
        </div>
      )}


      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Lista de Usuarios</h3>
        </div>
        
        {!Array.isArray(users) || users.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            {!Array.isArray(users) ? 'Cargando usuarios...' : 'No hay usuarios registrados.'}
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Email</th>
                  <th>Rol</th>
                  <th>Empresa</th>
                  <th>Estado</th>
                  <th>Fecha de Creación</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {users.map(userItem => (
                  <tr key={userItem.id}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <UserIcon size={16} />
                        <strong>{userItem.full_name}</strong>
                        <small style={{ color: '#666' }}>({userItem.username})</small>
                      </div>
                    </td>
                    <td>{userItem.email}</td>
                    <td>
                      <span className={getRoleBadge(userItem.role)}>
                        {userItem.role.toUpperCase()}
                      </span>
                    </td>
                    <td>{userItem.company.name}</td>
                    <td>
                      <span className={`badge ${userItem.is_active ? 'badge-success' : 'badge-danger'}`}>
                        {userItem.is_active ? 'ACTIVO' : 'INACTIVO'}
                      </span>
                    </td>
                    <td>
                      {format(new Date(userItem.created_at), 'dd/MM/yyyy', { locale: es })}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          onClick={() => handleEdit(userItem)}
                          className="btn btn-secondary"
                          style={{ padding: '4px 8px', fontSize: '12px' }}
                        >
                          <Edit size={14} />
                        </button>
                        <button
                          onClick={() => handleDelete(userItem.id)}
                          className="btn btn-danger"
                          style={{ padding: '4px 8px', fontSize: '12px' }}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Users;
