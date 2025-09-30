import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { companyService } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit, Trash2, Building2 } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

function Companies() {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [editingCompany, setEditingCompany] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    is_active: true,
  });

  const { data: companies, isLoading, error } = useQuery(
    'companies',
    () => companyService.getAll(),
  );

  const createMutation = useMutation(
    (data) => companyService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('companies');
        toast.success('Empresa creada exitosamente');
        resetForm();
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Error al crear la empresa');
      },
    }
  );

  const updateMutation = useMutation(
    (data) => companyService.update(editingCompany.id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('companies');
        toast.success('Empresa actualizada exitosamente');
        resetForm();
      },
      onError: (error) => {
        toast.error(error.response?.data?.detail || 'Error al actualizar la empresa');
      },
    }
  );

  const deleteMutation = useMutation(
    (id) => companyService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('companies');
        toast.success('Empresa eliminada exitosamente');
      },
      onError: () => {
        toast.error('Error al eliminar la empresa');
      },
    }
  );

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      is_active: true,
    });
    setShowForm(false);
    setEditingCompany(null);
  };

  const handleEdit = (company) => {
    setEditingCompany(company);
    setFormData({
      name: company.name,
      description: company.description || '',
      is_active: company.is_active,
    });
    setShowForm(true);
  };

  const handleDelete = (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta empresa?')) {
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
    
    if (editingCompany) {
      updateMutation.mutate(formData);
    } else {
      createMutation.mutate(formData);
    }
  };

  if (isLoading) {
    return <div className="loading">Cargando empresas...</div>;
  }

  return (
    <div style={{ width: '100%', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Empresas</h1>
        <button 
          onClick={() => setShowForm(true)}
          className="btn btn-primary"
        >
          <Plus size={16} style={{ marginRight: '8px' }} />
          Nueva Empresa
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '24px' }}>
          <div className="card-header">
            <h3 className="card-title">
              {editingCompany ? 'Editar Empresa' : 'Nueva Empresa'}
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
                  placeholder="Nombre de la empresa"
                />
              </div>

              <div className="form-group">
                <label className="form-label">Descripción</label>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  className="form-control"
                  rows="3"
                  placeholder="Descripción de la empresa"
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
                  Empresa activa
                </label>
              </div>
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
                {editingCompany ? 'Actualizar' : 'Crear'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Lista de Empresas</h3>
        </div>
        
        {!Array.isArray(companies) || companies.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            No hay empresas registradas.
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Empresa</th>
                  <th>Descripción</th>
                  <th>Estado</th>
                  <th>Fecha de Creación</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {Array.isArray(companies) && companies.map(company => (
                  <tr key={company.id}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <Building2 size={16} />
                        <strong>{company.name}</strong>
                      </div>
                    </td>
                    <td>
                      {company.description || (
                        <span style={{ color: '#666', fontStyle: 'italic' }}>
                          Sin descripción
                        </span>
                      )}
                    </td>
                    <td>
                      <span className={`badge ${company.is_active ? 'badge-success' : 'badge-danger'}`}>
                        {company.is_active ? 'ACTIVA' : 'INACTIVA'}
                      </span>
                    </td>
                    <td>
                      {format(new Date(company.created_at), 'dd/MM/yyyy', { locale: es })}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          onClick={() => handleEdit(company)}
                          className="btn btn-secondary"
                          style={{ padding: '4px 8px', fontSize: '12px' }}
                        >
                          <Edit size={14} />
                        </button>
                        <button
                          onClick={() => handleDelete(company.id)}
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

export default Companies;
