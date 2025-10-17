import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { taskService, userService } from '../services/api';
import toast from 'react-hot-toast';
import { Plus, Edit, Trash2, Filter } from 'lucide-react';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import { StatusBadge, PriorityBadge } from '../components/Badge';
import ActionButton from '../components/ActionButton';
import LinkButton from '../components/LinkButton';

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
        return '#f39c12';
      case 'en_progreso':
        return '#3498db';
      case 'completada':
        return '#27ae60';
      case 'cancelada':
        return '#e74c3c';
      default:
        return '#95a5a6';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'baja':
        return '#95a5a6';
      case 'media':
        return '#f39c12';
      case 'alta':
        return '#e67e22';
      case 'critica':
        return '#c0392b';
      default:
        return '#95a5a6';
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
        <LinkButton
          to="/tasks/new"
          variant="primary"
          size="medium"
          icon={Plus}
        >
          Nueva Tarea
        </LinkButton>
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
          background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
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
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f8f9fa'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}>
                  
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
                    <StatusBadge status={task.status} />
                  </div>
                  
                  {/* Prioridad */}
                  <div>
                    <PriorityBadge priority={task.priority} />
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
                      {task.client?.name || 'N/A'}
                    </div>
                  </div>
                  
                  {/* Acciones */}
                  <div>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <LinkButton
                        to={`/tasks/${task.id}/edit`}
                        variant="secondary"
                        size="small"
                        icon={Edit}
                      >
                        Editar
                      </LinkButton>
                      <ActionButton
                        variant="danger"
                        size="small"
                        onClick={() => handleDelete(task.id)}
                        icon={Trash2}
                      >
                        Eliminar
                      </ActionButton>
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
