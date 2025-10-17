import React, { useState, useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { clientService, arlService } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit, Trash2, Building2, Filter, ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { Badge } from '../components/Badge';
import FormSelect from '../components/FormSelect';
import ActionButton from '../components/ActionButton';
import LinkButton from '../components/LinkButton';

function Clients() {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [editingClient, setEditingClient] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    arl_id: '',
    is_active: true,
  });

  // Estados para filtros y búsqueda
  const [selectedARL, setSelectedARL] = useState(''); // Filtro predeterminado vacío para mostrar todos
  const [statusFilter, setStatusFilter] = useState('all'); // all, active, inactive
  const [sortField, setSortField] = useState('name'); // name, arl, created_at
  const [sortDirection, setSortDirection] = useState('asc'); // asc, desc

  const { data: clients, isLoading, error } = useQuery(
    'clients',
    () => clientService.getAll(),
  );

  const { data: arls } = useQuery(
    'arls',
    () => arlService.getAll(),
  );

  // Lógica de filtrado y ordenamiento
  const filteredAndSortedClients = useMemo(() => {
    if (!Array.isArray(clients)) return [];

    let filtered = clients.filter(client => {
      // Filtro por ARL
      const matchesARL = selectedARL === '' || client.arl?.id?.toString() === selectedARL;

      // Filtro por estado
      const matchesStatus = statusFilter === 'all' || 
        (statusFilter === 'active' && client.is_active) ||
        (statusFilter === 'inactive' && !client.is_active);

      return matchesARL && matchesStatus;
    });

    // Ordenamiento
    filtered.sort((a, b) => {
      let aValue, bValue;
      
      switch (sortField) {
        case 'name':
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
          break;
        case 'arl':
          aValue = a.arl?.name?.toLowerCase() || '';
          bValue = b.arl?.name?.toLowerCase() || '';
          break;
        case 'created_at':
          aValue = new Date(a.created_at);
          bValue = new Date(b.created_at);
          break;
        default:
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
      }

      if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });

    return filtered;
  }, [clients, selectedARL, statusFilter, sortField, sortDirection]);

  // Función para cambiar el ordenamiento
  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  // Función para obtener el icono de ordenamiento
  const getSortIcon = (field) => {
    if (sortField !== field) return <ArrowUpDown size={16} />;
    return sortDirection === 'asc' ? <ArrowUp size={16} /> : <ArrowDown size={16} />;
  };

  const createMutation = useMutation(
    (data) => clientService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('clients');
        toast.success('Cliente creado exitosamente');
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
          toast.error('Error al crear el cliente');
        }
      },
    }
  );

  const updateMutation = useMutation(
    (data) => clientService.update(editingClient.id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('clients');
        toast.success('Cliente actualizado exitosamente');
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
          toast.error('Error al actualizar el cliente');
        }
      },
    }
  );

  const deleteMutation = useMutation(
    (id) => clientService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('clients');
        toast.success('Cliente eliminado exitosamente');
      },
      onError: () => {
        toast.error('Error al eliminar el cliente');
      },
    }
  );

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      arl_id: '',
      is_active: true,
    });
    setShowForm(false);
    setEditingClient(null);
  };

  const getARLColor = (arlName) => {
    switch (arlName?.toLowerCase()) {
      case 'colmena arl':
        return '#3498db'; // Azul para COLMENA
      case 'positiva arl':
        return '#27ae60'; // Verde para POSITIVA
      case 'sura arl':
        return '#e67e22'; // Naranja para SURA
      default:
        return '#95a5a6'; // Gris por defecto
    }
  };

  const getStatusColor = (isActive) => {
    return isActive ? '#27ae60' : '#e74c3c'; // Verde para activo, rojo para inactivo
  };

  const handleEdit = (client) => {
    setEditingClient(client);
    setFormData({
      name: client.name,
      description: client.description || '',
      arl_id: client.arl?.id || '',
      is_active: client.is_active,
    });
    setShowForm(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar este cliente?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (editingClient) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  if (isLoading) {
    return <div className="loading">Cargando clientes...</div>;
  }

  return (
    <div style={{ width: '100%', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Clientes</h1>
        <ActionButton
          variant="primary"
          size="medium"
          onClick={() => setShowForm(true)}
          icon={Plus}
        >
          Nuevo Cliente
        </ActionButton>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '24px' }}>
          <div className="card-header">
            <h3 className="card-title">
              {editingClient ? 'Editar Cliente' : 'Nuevo Cliente'}
            </h3>
          </div>
          
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
              <div className="form-group">
                <label className="form-label">Nombre *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="form-control"
                  required
                  placeholder="Nombre del cliente"
                />
              </div>

              <FormSelect
                name="arl_id"
                value={formData.arl_id}
                onChange={handleChange}
                label="ARL"
                required
                placeholder="Seleccionar ARL"
                options={arls?.map(arl => ({
                  value: arl.id,
                  label: arl.name
                })) || []}
              />

              <div className="form-group">
                <label className="form-label">Descripción</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  className="form-control"
                  rows="3"
                  placeholder="Descripción del cliente"
                />
              </div>

              <div className="form-group">
                <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <input
                    type="checkbox"
                    name="is_active"
                    checked={formData.is_active}
                    onChange={handleChange}
                  />
                  Cliente activo
                </label>
              </div>
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
                {editingClient ? 'Actualizar' : 'Crear'}
              </ActionButton>
            </div>
          </form>
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Lista de Clientes</h3>
        </div>

        {/* Filtros */}
        <div style={{ 
          padding: '20px', 
          borderBottom: '1px solid #e1e5e9',
          backgroundColor: '#f8f9fa'
        }}>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
            gap: '16px',
            marginBottom: '16px'
          }}>
            {/* Filtro por ARL */}
            <div className="form-group">
              <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Filter size={16} />
                Filtrar por ARL
              </label>
              <FormSelect
                value={selectedARL}
                onChange={(e) => setSelectedARL(e.target.value)}
                placeholder="Todas las ARLs"
                options={[
                  { value: '', label: 'Todas las ARLs' },
                  ...(arls?.map(arl => ({
                    value: arl.id.toString(),
                    label: arl.name
                  })) || [])
                ]}
              />
            </div>

            {/* Filtro por Estado */}
            <div className="form-group">
              <label className="form-label">Estado</label>
              <FormSelect
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                options={[
                  { value: 'all', label: 'Todos los estados' },
                  { value: 'active', label: 'Solo activos' },
                  { value: 'inactive', label: 'Solo inactivos' }
                ]}
              />
            </div>
          </div>

          {/* Información de resultados */}
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            fontSize: '14px',
            color: '#666'
          }}>
            <span>
              Mostrando {filteredAndSortedClients.length} de {clients?.length || 0} clientes
            </span>
            {(selectedARL || statusFilter !== 'all') && (
              <button
                onClick={() => {
                  setSelectedARL('');
                  setStatusFilter('all');
                }}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#3498db',
                  cursor: 'pointer',
                  textDecoration: 'underline',
                  fontSize: '14px'
                }}
              >
                Limpiar filtros
              </button>
            )}
          </div>
        </div>
        
        {!Array.isArray(clients) || clients.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            No hay clientes registrados.
          </div>
        ) : filteredAndSortedClients.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            No se encontraron clientes con los filtros aplicados.
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th 
                    style={{ cursor: 'pointer', userSelect: 'none' }}
                    onClick={() => handleSort('name')}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      Cliente
                      {getSortIcon('name')}
                    </div>
                  </th>
                  <th 
                    style={{ cursor: 'pointer', userSelect: 'none' }}
                    onClick={() => handleSort('arl')}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      ARL
                      {getSortIcon('arl')}
                    </div>
                  </th>
                  <th>Descripción</th>
                  <th>Estado</th>
                  <th 
                    style={{ cursor: 'pointer', userSelect: 'none' }}
                    onClick={() => handleSort('created_at')}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      Fecha de Creación
                      {getSortIcon('created_at')}
                    </div>
                  </th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredAndSortedClients.map(client => (
                  <tr key={client.id}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Building2 size={16} />
                        <strong>{client.name}</strong>
                      </div>
                    </td>
                    <td>
                      <Badge 
                        backgroundColor={getARLColor(client.arl?.name)}
                        variant="status"
                        size="small"
                      >
                        {client.arl?.name || 'N/A'}
                      </Badge>
                    </td>
                    <td>
                      {client.description || (
                        <span style={{ color: '#666', fontStyle: 'italic' }}>
                          Sin descripción
                        </span>
                      )}
                    </td>
                    <td>
                      <Badge 
                        backgroundColor={getStatusColor(client.is_active)}
                        variant="status"
                        size="small"
                      >
                        {client.is_active ? 'ACTIVO' : 'INACTIVO'}
                      </Badge>
                    </td>
                    <td>
                      {format(new Date(client.created_at), 'dd/MM/yyyy', { locale: es })}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <ActionButton
                          variant="secondary"
                          size="small"
                          onClick={() => handleEdit(client)}
                          icon={Edit}
                        >
                          Editar
                        </ActionButton>
                        <ActionButton
                          variant="danger"
                          size="small"
                          onClick={() => handleDelete(client.id)}
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

export default Clients;
