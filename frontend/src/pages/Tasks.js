import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { taskService, userService } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit, Trash2, Filter } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

function Tasks() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [filters, setFilters] = useState({
    status: '',
    assigned_to: '',
  });

  const { data: tasks, isLoading, error } = useQuery(
    ['tasks', filters],
    () => {
      // Limpiar filtros vacíos para evitar errores 422
      const cleanFilters = {};
      if (filters.status && filters.status !== '') {
        cleanFilters.status = filters.status;
      }
      if (filters.assigned_to && filters.assigned_to !== '') {
        cleanFilters.assigned_to = parseInt(filters.assigned_to);
      }
      return taskService.getAll(cleanFilters);
    },
    {
      enabled: !!user,
    }
  );

  const { data: users, isLoading: usersLoading } = useQuery(
    'users',
    () => userService.getAll(),
    {
      enabled: !!user,
    }
  );

  const deleteTaskMutation = useMutation(
    (id) => taskService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
        toast.success('Tarea eliminada exitosamente');
      },
      onError: () => {
        toast.error('Error al eliminar la tarea');
      },
    }
  );

  const handleDelete = (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
      deleteTaskMutation.mutate(id);
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getStatusBadge = (status) => {
    const statusMap = {
      pendiente: 'badge-pendiente',
      en_progreso: 'badge-en-progreso',
      completada: 'badge-completada',
      cancelada: 'badge-cancelada',
    };
    return `badge ${statusMap[status] || 'badge-secondary'}`;
  };

  const getPriorityBadge = (priority) => {
    const priorityMap = {
      baja: 'badge-baja',
      media: 'badge-media',
      alta: 'badge-alta',
      critica: 'badge-critica',
    };
    return `badge ${priorityMap[priority] || 'badge-secondary'}`;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pendiente':
        return '#ffc107';
      case 'en_progreso':
        return '#17a2b8';
      case 'completada':
        return '#28a745';
      case 'cancelada':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'baja':
        return '#28a745';
      case 'media':
        return '#ffc107';
      case 'alta':
        return '#fd7e14';
      case 'critica':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  };

  if (isLoading) {
    return <div className="loading">Cargando tareas...</div>;
  }

  if (error) {
    return <div className="error">Error al cargar tareas: {error.message}</div>;
  }

  return (
    <div style={{ width: '100%', padding: '20px' }}>
      {/* Debug info - temporal */}
      <div style={{ background: '#f0f0f0', padding: '10px', marginBottom: '20px', fontSize: '12px' }}>
        <strong>Debug:</strong> isLoading: {isLoading.toString()}, tasks: {tasks ? 'loaded' : 'null'}, 
        tasks type: {typeof tasks}, tasks length: {Array.isArray(tasks) ? tasks.length : 'not array'}, 
        user: {user ? 'loaded' : 'null'}
      </div>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Tareas</h1>
        <Link to="/tasks/new" className="btn btn-primary">
          <Plus size={16} style={{ marginRight: '8px' }} />
          Nueva Tarea
        </Link>
      </div>

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Filtros</h3>
        </div>
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <div className="form-group" style={{ marginBottom: 0, minWidth: '200px' }}>
            <label className="form-label">Estado</label>
            <select
              className="form-control"
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <option value="">Todos los estados</option>
              <option value="pendiente">Pendiente</option>
              <option value="en_progreso">En Progreso</option>
              <option value="completada">Completada</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>
          
          <div className="form-group" style={{ marginBottom: 0, minWidth: '200px' }}>
            <label className="form-label">Asignado a</label>
            <select
              className="form-control"
              value={filters.assigned_to}
              onChange={(e) => handleFilterChange('assigned_to', e.target.value)}
            >
              <option value="">Todos los usuarios</option>
              {Array.isArray(users) && users.map(user => (
                <option key={user.id} value={user.id}>
                  {user.full_name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Lista de Tareas Mejorada */}
      <div style={{
        background: 'white',
        borderRadius: '16px',
        boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        border: '1px solid #f0f0f0',
        overflow: 'hidden'
      }}>
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          padding: '20px 24px',
          borderBottom: '1px solid #f0f0f0'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '20px', fontWeight: '600' }}>
                📋 Lista de Tareas
              </h3>
              <p style={{ margin: '4px 0 0', fontSize: '14px', opacity: 0.9 }}>
                {Array.isArray(tasks) ? `${tasks.length} tareas encontradas` : 'Cargando...'}
              </p>
            </div>
            <div style={{
              background: 'rgba(255,255,255,0.2)',
              padding: '8px 16px',
              borderRadius: '20px',
              fontSize: '14px',
              fontWeight: '500'
            }}>
              Total: {Array.isArray(tasks) ? tasks.length : 0}
            </div>
          </div>
        </div>
        
        {!Array.isArray(tasks) || tasks.length === 0 ? (
          <div style={{ 
            textAlign: 'center', 
            padding: '60px 20px', 
            color: '#666',
            background: '#f8f9fa'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>📝</div>
            <h4 style={{ margin: '0 0 8px', color: '#333' }}>
              {!Array.isArray(tasks) ? 'Cargando tareas...' : 'No hay tareas'}
            </h4>
            <p style={{ margin: 0, fontSize: '14px' }}>
              {!Array.isArray(tasks) ? 'Por favor espera...' : 'No se encontraron tareas que coincidan con los filtros seleccionados.'}
            </p>
          </div>
        ) : (
          <div style={{ padding: '0' }}>
            {/* Encabezados de tabla mejorados */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '2fr 1fr 1fr 1.5fr 1fr 1fr 1fr',
              gap: '16px',
              padding: '16px 24px',
              background: '#f8f9fa',
              borderBottom: '1px solid #e9ecef',
              fontWeight: '600',
              fontSize: '14px',
              color: '#495057'
            }}>
              <div>Título y Descripción</div>
              <div>Estado</div>
              <div>Prioridad</div>
              <div>Asignado a</div>
              <div>Fecha Vencimiento</div>
              <div>Empresa</div>
              <div>Acciones</div>
            </div>
            
            {/* Lista de tareas como tarjetas */}
            <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
              {tasks.map((task, index) => (
                <div key={task.id} style={{
                  display: 'grid',
                  gridTemplateColumns: '2fr 1fr 1fr 1.5fr 1fr 1fr 1fr',
                  gap: '16px',
                  padding: '20px 24px',
                  borderBottom: index < tasks.length - 1 ? '1px solid #f0f0f0' : 'none',
                  alignItems: 'center',
                  transition: 'background-color 0.2s ease'
                }}
                onMouseOver={(e) => e.target.style.backgroundColor = '#f8f9fa'}
                onMouseOut={(e) => e.target.style.backgroundColor = 'transparent'}>
                  
                  {/* Título y Descripción */}
                  <div>
                    <div style={{ 
                      fontWeight: '600', 
                      fontSize: '16px', 
                      color: '#333',
                      marginBottom: '4px',
                      lineHeight: '1.4'
                    }}>
                      {task.title}
                    </div>
                    {task.description && (
                      <div style={{ 
                        fontSize: '13px', 
                        color: '#666', 
                        lineHeight: '1.4'
                      }}>
                        {task.description.length > 80 
                          ? `${task.description.substring(0, 80)}...` 
                          : task.description
                        }
                      </div>
                    )}
                  </div>
                  
                  {/* Estado */}
                  <div>
                    <span style={{
                      display: 'inline-block',
                      padding: '6px 12px',
                      borderRadius: '20px',
                      fontSize: '12px',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                      backgroundColor: getStatusColor(task.status),
                      color: 'white'
                    }}>
                      {task.status.replace('_', ' ')}
                    </span>
                  </div>
                  
                  {/* Prioridad */}
                  <div>
                    <span style={{
                      display: 'inline-block',
                      padding: '6px 12px',
                      borderRadius: '20px',
                      fontSize: '12px',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                      backgroundColor: getPriorityColor(task.priority),
                      color: 'white'
                    }}>
                      {task.priority}
                    </span>
                  </div>
                  
                  {/* Asignado a */}
                  <div>
                    <div style={{ 
                      fontWeight: '500', 
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      {task.assigned_user ? task.assigned_user.full_name : 'Sin asignar'}
                    </div>
                    {task.assigned_user && (
                      <div style={{ 
                        fontSize: '12px', 
                        color: '#666',
                        marginTop: '2px'
                      }}>
                        {task.assigned_user.email}
                      </div>
                    )}
                  </div>
                  
                  {/* Fecha de Vencimiento */}
                  <div>
                    <div style={{ 
                      fontWeight: '500', 
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      {task.due_date 
                        ? format(new Date(task.due_date), 'dd/MM/yyyy', { locale: es })
                        : 'Sin fecha'
                      }
                    </div>
                    {task.due_date && (
                      <div style={{ 
                        fontSize: '12px', 
                        color: '#666',
                        marginTop: '2px'
                      }}>
                        {new Date(task.due_date) < new Date() ? '⚠️ Vencida' : '✅ Vigente'}
                      </div>
                    )}
                  </div>
                  
                  {/* Empresa */}
                  <div>
                    <div style={{ 
                      fontWeight: '500', 
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      {task.company.name}
                    </div>
                  </div>
                  
                  {/* Acciones */}
                  <div>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <Link 
                        to={`/tasks/${task.id}/edit`}
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          padding: '8px 12px',
                          background: '#6c757d',
                          color: 'white',
                          borderRadius: '6px',
                          textDecoration: 'none',
                          fontSize: '12px',
                          fontWeight: '500',
                          transition: 'background-color 0.2s ease'
                        }}
                        onMouseOver={(e) => e.target.style.backgroundColor = '#5a6268'}
                        onMouseOut={(e) => e.target.style.backgroundColor = '#6c757d'}
                      >
                        <Edit size={14} style={{ marginRight: '4px' }} />
                        Editar
                      </Link>
                      <button
                        onClick={() => handleDelete(task.id)}
                        style={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          padding: '8px 12px',
                          background: '#dc3545',
                          color: 'white',
                          border: 'none',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '500',
                          cursor: 'pointer',
                          transition: 'background-color 0.2s ease'
                        }}
                        onMouseOver={(e) => e.target.style.backgroundColor = '#c82333'}
                        onMouseOut={(e) => e.target.style.backgroundColor = '#dc3545'}
                      >
                        <Trash2 size={14} style={{ marginRight: '4px' }} />
                        Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Tasks;
