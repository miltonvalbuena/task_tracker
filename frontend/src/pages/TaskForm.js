import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { taskService, userService, clientService } from '../services/api';
import toast from 'react-hot-toast';
import { Save, ArrowLeft } from 'lucide-react';
import FormSelect from '../components/FormSelect';
import ActionButton from '../components/ActionButton';

function TaskForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const isEdit = !!id;

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'pendiente',
    priority: 'media',
    due_date: '',
    assigned_to: '',
    client_id: user?.client_id || '',
    custom_fields: {},
  });

  const { data: task } = useQuery(
    ['task', id],
    () => taskService.getById(id),
    {
      enabled: isEdit,
    }
  );

  const { data: users } = useQuery(
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

  // Obtener la configuración de campos personalizados del cliente seleccionado
  const selectedClient = clients?.find(client => client.id === parseInt(formData.client_id));
  const customFieldsConfig = selectedClient?.custom_fields_config || [];

  const createMutation = useMutation(
    (data) => taskService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
        toast.success('Tarea creada exitosamente');
        navigate('/tasks');
      },
      onError: (error) => {
        const errorData = error.response?.data;
        if (errorData?.detail) {
          if (Array.isArray(errorData.detail)) {
            // Manejar errores de validación de Pydantic
            const errorMessages = errorData.detail.map(err => err.msg || err.message || 'Error de validación').join(', ');
            toast.error(errorMessages);
          } else {
            toast.error(errorData.detail);
          }
        } else {
          toast.error('Error al crear la tarea');
        }
      },
    }
  );

  const updateMutation = useMutation(
    (data) => taskService.update(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
        queryClient.invalidateQueries(['task', id]);
        toast.success('Tarea actualizada exitosamente');
        navigate('/tasks');
      },
      onError: (error) => {
        const errorData = error.response?.data;
        if (errorData?.detail) {
          if (Array.isArray(errorData.detail)) {
            // Manejar errores de validación de Pydantic
            const errorMessages = errorData.detail.map(err => err.msg || err.message || 'Error de validación').join(', ');
            toast.error(errorMessages);
          } else {
            toast.error(errorData.detail);
          }
        } else {
          toast.error('Error al actualizar la tarea');
        }
      },
    }
  );

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        status: task.status || 'pendiente',
        priority: task.priority || 'media',
        due_date: task.due_date ? task.due_date.split('T')[0] : '',
        assigned_to: task.assigned_to || '',
        client_id: task.client_id || user?.client_id || '',
        custom_fields: task.custom_fields || {},
      });
    }
  }, [task, user]);

  // Limpiar campos personalizados cuando cambie la empresa (solo en modo creación)
  useEffect(() => {
    if (!isEdit && formData.client_id) {
      setFormData(prev => ({
        ...prev,
        custom_fields: {}
      }));
    }
  }, [formData.client_id, isEdit]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleCustomFieldChange = (fieldName, value) => {
    setFormData({
      ...formData,
      custom_fields: {
        ...formData.custom_fields,
        [fieldName]: value
      }
    });
  };

  const renderCustomField = (field) => {
    const fieldName = field.name;
    const fieldValue = formData.custom_fields[fieldName] || '';

    const baseInputStyle = {
      width: '100%',
      padding: '12px 16px',
      border: '2px solid #e1e5e9',
      borderRadius: '8px',
      fontSize: '16px',
      background: '#fafbfc',
      transition: 'all 0.3s ease',
      fontFamily: 'inherit'
    };

    const focusStyle = (color = '#007bff') => ({
      borderColor: color,
      background: 'white',
      boxShadow: `0 0 0 3px rgba(${color === '#007bff' ? '0,123,255' : '255,193,7'},0.1)`
    });

    const blurStyle = {
      borderColor: '#e1e5e9',
      background: '#fafbfc',
      boxShadow: 'none'
    };

    switch (field.field_type) {
      case 'text':
        return (
          <input
            type="text"
            value={fieldValue}
            onChange={(e) => handleCustomFieldChange(fieldName, e.target.value)}
            style={baseInputStyle}
            placeholder={field.placeholder || ''}
            required={field.required}
            onFocus={(e) => Object.assign(e.target.style, focusStyle('#ffc107'))}
            onBlur={(e) => Object.assign(e.target.style, blurStyle)}
          />
        );
      
      case 'textarea':
        return (
          <textarea
            value={fieldValue}
            onChange={(e) => handleCustomFieldChange(fieldName, e.target.value)}
            style={{
              ...baseInputStyle,
              minHeight: '100px',
              resize: 'vertical',
              lineHeight: '1.5'
            }}
            rows="3"
            placeholder={field.placeholder || ''}
            required={field.required}
            onFocus={(e) => Object.assign(e.target.style, focusStyle('#ffc107'))}
            onBlur={(e) => Object.assign(e.target.style, blurStyle)}
          />
        );
      
      case 'number':
        return (
          <input
            type="number"
            value={fieldValue}
            onChange={(e) => handleCustomFieldChange(fieldName, e.target.value)}
            style={baseInputStyle}
            placeholder={field.placeholder || ''}
            required={field.required}
            onFocus={(e) => Object.assign(e.target.style, focusStyle('#ffc107'))}
            onBlur={(e) => Object.assign(e.target.style, blurStyle)}
          />
        );
      
      case 'date':
        return (
          <input
            type="date"
            value={fieldValue}
            onChange={(e) => handleCustomFieldChange(fieldName, e.target.value)}
            style={baseInputStyle}
            required={field.required}
            onFocus={(e) => Object.assign(e.target.style, focusStyle('#ffc107'))}
            onBlur={(e) => Object.assign(e.target.style, blurStyle)}
          />
        );
      
      case 'select':
        return (
          <select
            value={fieldValue}
            onChange={(e) => handleCustomFieldChange(fieldName, e.target.value)}
            style={{
              ...baseInputStyle,
              cursor: 'pointer'
            }}
            required={field.required}
            onFocus={(e) => Object.assign(e.target.style, focusStyle('#ffc107'))}
            onBlur={(e) => Object.assign(e.target.style, blurStyle)}
          >
            <option value="">Seleccionar...</option>
            {field.options?.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        );
      
      default:
        return (
          <input
            type="text"
            value={fieldValue}
            onChange={(e) => handleCustomFieldChange(fieldName, e.target.value)}
            style={baseInputStyle}
            placeholder={field.placeholder || ''}
            required={field.required}
            onFocus={(e) => Object.assign(e.target.style, focusStyle('#ffc107'))}
            onBlur={(e) => Object.assign(e.target.style, blurStyle)}
          />
        );
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convertir fecha a formato datetime si existe
    let dueDate = null;
    if (formData.due_date) {
      // Convertir fecha (YYYY-MM-DD) a datetime (YYYY-MM-DDTHH:MM:SS)
      dueDate = `${formData.due_date}T00:00:00`;
    }
    
    const submitData = {
      ...formData,
      assigned_to: formData.assigned_to ? parseInt(formData.assigned_to) : null,
      client_id: parseInt(formData.client_id),
      due_date: dueDate,
    };

    if (isEdit) {
      updateMutation.mutate(submitData);
    } else {
      createMutation.mutate(submitData);
    }
  };

  const isLoading = createMutation.isLoading || updateMutation.isLoading;

  return (
    <div style={{ 
      width: '100%', 
      padding: '20px',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      minHeight: '100vh'
    }}>
      {/* Header con diseño mejorado */}
      <div style={{ 
        background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
        color: 'white',
        padding: '24px',
        borderRadius: '12px',
        marginBottom: '30px',
        boxShadow: '0 8px 32px rgba(44, 62, 80, 0.3)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button
            onClick={() => navigate('/tasks')}
            style={{
              background: 'rgba(255,255,255,0.2)',
              border: 'none',
              color: 'white',
              padding: '10px 16px',
              borderRadius: '8px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '14px',
              fontWeight: '500',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(255,255,255,0.2)';
            }}
          >
            <ArrowLeft size={16} />
            Volver
          </button>
          <div>
            <h1 style={{ margin: 0, fontSize: '28px', fontWeight: 'bold' }}>
              {isEdit ? 'Editar Actividad' : 'Nueva Actividad'}
            </h1>
            <p style={{ margin: '4px 0 0', opacity: 0.9, fontSize: '14px' }}>
              {isEdit ? 'Modifica los detalles de la actividad' : 'Crea una nueva actividad en el sistema'}
            </p>
          </div>
        </div>
      </div>

      {/* Formulario principal con diseño mejorado */}
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '32px',
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        border: '1px solid rgba(255,255,255,0.2)'
      }}>
        <form onSubmit={handleSubmit}>
          {/* Sección de Información Básica */}
          <div style={{ marginBottom: '32px' }}>
            <h2 style={{ 
              color: '#333', 
              marginBottom: '20px', 
              fontSize: '20px',
              fontWeight: '600',
              borderBottom: '3px solid #3498db',
              paddingBottom: '8px'
            }}>
              Información Básica
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
                  Título de la Actividad *
                </label>
                <input
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    border: '2px solid #e1e5e9',
                    borderRadius: '8px',
                    fontSize: '16px',
                    transition: 'all 0.3s ease',
                    background: '#fafbfc'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#3498db';
                    e.target.style.background = 'white';
                    e.target.style.boxShadow = '0 0 0 3px rgba(52,152,219,0.1)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = '#e1e5e9';
                    e.target.style.background = '#fafbfc';
                    e.target.style.boxShadow = 'none';
                  }}
                  required
                  placeholder="Ingresa el título de la actividad"
                />
              </div>

              <FormSelect
                name="status"
                value={formData.status}
                onChange={handleChange}
                label="Estado"
                required
                options={[
                  { value: 'pendiente', label: 'Pendiente' },
                  { value: 'en_progreso', label: 'En Ejecución' },
                  { value: 'completada', label: 'Finalizada' },
                  { value: 'cancelada', label: 'Cancelada' }
                ]}
              />

              <FormSelect
                name="priority"
                value={formData.priority}
                onChange={handleChange}
                label="Prioridad"
                required
                options={[
                  { value: 'baja', label: 'Baja' },
                  { value: 'media', label: 'Media' },
                  { value: 'alta', label: 'Alta' },
                  { value: 'critica', label: 'Crítica' }
                ]}
              />

              <div>
                <label style={{
                  display: 'block',
                  marginBottom: '8px',
                  fontWeight: '600',
                  color: '#333',
                  fontSize: '14px'
                }}>
                  Fecha de Vencimiento
                </label>
                <input
                  type="date"
                  name="due_date"
                  value={formData.due_date}
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
                    e.target.style.borderColor = '#3498db';
                    e.target.style.background = 'white';
                    e.target.style.boxShadow = '0 0 0 3px rgba(52,152,219,0.1)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = '#e1e5e9';
                    e.target.style.background = '#fafbfc';
                    e.target.style.boxShadow = 'none';
                  }}
                />
              </div>

              <FormSelect
                name="assigned_to"
                value={formData.assigned_to}
                onChange={handleChange}
                label="Asignado a"
                placeholder="Sin asignar"
                options={users?.map(user => ({
                  value: user.id,
                  label: user.full_name
                })) || []}
              />

              {user?.role === 'admin' && (
                <FormSelect
                  name="client_id"
                  value={formData.client_id}
                  onChange={handleChange}
                  label="Cliente"
                  required
                  placeholder="Seleccionar cliente"
                  options={clients?.map(client => ({
                    value: client.id,
                    label: client.name
                  })) || []}
                />
              )}
            </div>
          </div>

          {/* Descripción */}
          <div style={{ marginBottom: '32px' }}>
            <h2 style={{ 
              color: '#333', 
              marginBottom: '20px', 
              fontSize: '20px',
              fontWeight: '600',
              borderBottom: '3px solid #27ae60',
              paddingBottom: '8px'
            }}>
              Descripción
            </h2>
            <div>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontWeight: '600',
                color: '#333',
                fontSize: '14px'
              }}>
                Descripción detallada
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                style={{
                  width: '100%',
                  padding: '16px',
                  border: '2px solid #e1e5e9',
                  borderRadius: '8px',
                  fontSize: '16px',
                  background: '#fafbfc',
                  minHeight: '120px',
                  resize: 'vertical',
                  fontFamily: 'inherit',
                  lineHeight: '1.5',
                  transition: 'all 0.3s ease'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#27ae60';
                  e.target.style.background = 'white';
                  e.target.style.boxShadow = '0 0 0 3px rgba(39,174,96,0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e1e5e9';
                  e.target.style.background = '#fafbfc';
                  e.target.style.boxShadow = 'none';
                }}
                placeholder="Describe detalladamente la actividad a realizar..."
              />
            </div>
          </div>

          {/* Campos Personalizados */}
          {customFieldsConfig.length > 0 && (
            <div style={{ marginBottom: '32px' }}>
              <h2 style={{ 
                color: '#333', 
                marginBottom: '20px', 
                fontSize: '20px',
                fontWeight: '600',
                borderBottom: '3px solid #ffc107',
                paddingBottom: '8px'
              }}>
                Campos Específicos de {selectedClient?.name || 'el Cliente'}
              </h2>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', 
                gap: '24px' 
              }}>
                {customFieldsConfig.map((field, index) => (
                  <div key={field.name}>
                    <label style={{
                      display: 'block',
                      marginBottom: '8px',
                      fontWeight: '600',
                      color: '#333',
                      fontSize: '14px'
                    }}>
                      {field.label}
                      {field.required && <span style={{ color: '#dc3545', marginLeft: '4px' }}>*</span>}
                    </label>
                    {renderCustomField(field)}
                    {field.help_text && (
                      <div style={{ 
                        fontSize: '12px', 
                        color: '#6c757d', 
                        marginTop: '6px',
                        fontStyle: 'italic',
                        lineHeight: '1.4'
                      }}>
                        {field.help_text}
                      </div>
                    )}
                  </div>
                ))}
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
            <ActionButton
              type="button"
              variant="secondary"
              onClick={() => navigate('/tasks')}
            >
              Cancelar
            </ActionButton>
            <ActionButton
              type="submit"
              variant="primary"
              disabled={isLoading}
              loading={isLoading}
              icon={Save}
            >
              {isLoading ? 'Guardando...' : (isEdit ? 'Actualizar Actividad' : 'Crear Actividad')}
            </ActionButton>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TaskForm;
