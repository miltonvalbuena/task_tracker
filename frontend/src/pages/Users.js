import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useAuth } from '../contexts/AuthContext';
import { userService, clientService } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit, Trash2, User as UserIcon } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { Badge, StatusBadge } from '../components/Badge';
import FormSelect from '../components/FormSelect';
import ActionButton from '../components/ActionButton';
import LinkButton from '../components/LinkButton';

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
    client_id: user?.client_id || '',
  });

  const { data: users, isLoading } = useQuery(
    'users',
    () => userService.getAll(),
    {
      enabled: !!user,
    }
  );

  const { data: clients } = useQuery(
    'clients',
    () => clientService.getAll(),
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
        const errorData = error.response?.data;
        if (errorData?.detail) {
          if (Array.isArray(errorData.detail)) {
            const errorMessages = errorData.detail.map(err => err.msg || err.message || 'Error de validación').join(', ');
            toast.error(errorMessages);
          } else {
            toast.error(errorData.detail);
          }
        } else {
          toast.error('Error al crear el usuario');
        }
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
        const errorData = error.response?.data;
        if (errorData?.detail) {
          if (Array.isArray(errorData.detail)) {
            const errorMessages = errorData.detail.map(err => err.msg || err.message || 'Error de validación').join(', ');
            toast.error(errorMessages);
          } else {
            toast.error(errorData.detail);
          }
        } else {
          toast.error('Error al actualizar el usuario');
        }
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
      client_id: user?.client_id || '',
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
      client_id: user.client_id,
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
      client_id: parseInt(formData.client_id),
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

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin':
        return '#e74c3c'; // Rojo para admin
      case 'manager':
        return '#f39c12'; // Naranja para manager
      case 'user':
        return '#3498db'; // Azul para user
      default:
        return '#95a5a6'; // Gris por defecto
    }
  };

  const getStatusColor = (isActive) => {
    return isActive ? '#27ae60' : '#e74c3c'; // Verde para activo, rojo para inactivo
  };

  if (isLoading) {
    return <div className="loading">Cargando usuarios...</div>;
  }

  return (
    <div style={{ width: '100%', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Usuarios</h1>
        <ActionButton
          variant="primary"
          size="medium"
          onClick={() => setShowForm(true)}
          icon={Plus}
        >
          Nuevo Usuario
        </ActionButton>
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

              <FormSelect
                name="role"
                value={formData.role}
                onChange={handleChange}
                label="Rol"
                required
                options={[
                  { value: 'user', label: 'Usuario' },
                  { value: 'manager', label: 'Manager' },
                  ...(user?.role === 'admin' ? [{ value: 'admin', label: 'Administrador' }] : [])
                ]}
              />

              {user?.role === 'admin' && (
                <FormSelect
                  name="client_id"
                  value={formData.client_id}
                  onChange={handleChange}
                  label="Cliente"
                  required
                  placeholder="Seleccionar cliente"
                  options={Array.isArray(clients) ? clients.map(client => ({
                    value: client.id,
                    label: client.name
                  })) : []}
                />
              )}
            </div>

            <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '16px' }}>
              <ActionButton
                type="button"
                variant="secondary"
                onClick={resetForm}
              >
                Cancelar
              </ActionButton>
              <ActionButton
                type="submit"
                variant="primary"
                disabled={createMutation.isLoading || updateMutation.isLoading}
                loading={createMutation.isLoading || updateMutation.isLoading}
              >
                {editingUser ? 'Actualizar' : 'Crear'}
              </ActionButton>
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
                      <Badge 
                        backgroundColor={getRoleColor(userItem.role)}
                        variant="status"
                        size="small"
                      >
                        {userItem.role.toUpperCase()}
                      </Badge>
                    </td>
                    <td>{userItem.client?.name || 'N/A'}</td>
                    <td>
                      <Badge 
                        backgroundColor={getStatusColor(userItem.is_active)}
                        variant="status"
                        size="small"
                      >
                        {userItem.is_active ? 'ACTIVO' : 'INACTIVO'}
                      </Badge>
                    </td>
                    <td>
                      {format(new Date(userItem.created_at), 'dd/MM/yyyy', { locale: es })}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <ActionButton
                          variant="secondary"
                          size="small"
                          onClick={() => handleEdit(userItem)}
                          icon={Edit}
                        >
                          Editar
                        </ActionButton>
                        <ActionButton
                          variant="danger"
                          size="small"
                          onClick={() => handleDelete(userItem.id)}
                          icon={Trash2}
                        >
                          Eliminar
                        </ActionButton>
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
