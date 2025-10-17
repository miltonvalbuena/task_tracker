import React from 'react';

const Badge = ({ 
  children, 
  color, 
  backgroundColor, 
  size = 'medium',
  variant = 'default',
  ...props 
}) => {
  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          padding: '4px 8px',
          fontSize: '11px',
          borderRadius: '10px'
        };
      case 'large':
        return {
          padding: '8px 16px',
          fontSize: '14px',
          borderRadius: '16px'
        };
      default: // medium
        return {
          padding: '6px 12px',
          fontSize: '12px',
          borderRadius: '12px'
        };
    }
  };

  const getVariantStyles = () => {
    switch (variant) {
      case 'status':
        return {
          textTransform: 'uppercase',
          fontWeight: '600'
        };
      case 'priority':
        return {
          textTransform: 'uppercase',
          fontWeight: '600'
        };
      case 'count':
        return {
          fontWeight: '600'
        };
      default:
        return {
          fontWeight: '500'
        };
    }
  };

  const baseStyles = {
    display: 'inline-block',
    color: color || 'white',
    backgroundColor: backgroundColor || '#6c757d',
    cursor: 'default',
    userSelect: 'none',
    pointerEvents: 'none',
    border: 'none',
    outline: 'none',
    ...getSizeStyles(),
    ...getVariantStyles()
  };

  return (
    <span
      style={baseStyles}
      onMouseDown={(e) => e.preventDefault()}
      onMouseUp={(e) => e.preventDefault()}
      onClick={(e) => e.preventDefault()}
      {...props}
    >
      {children}
    </span>
  );
};

// Componentes específicos para diferentes tipos de badges
export const StatusBadge = ({ status, size = 'medium' }) => {
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

  const getStatusText = (status) => {
    switch (status) {
      case 'en_progreso':
        return 'En Ejecución';
      case 'completada':
        return 'Finalizada';
      default:
        return status.replace('_', ' ');
    }
  };

  return (
    <Badge
      backgroundColor={getStatusColor(status)}
      variant="status"
      size={size}
    >
      {getStatusText(status)}
    </Badge>
  );
};

export const PriorityBadge = ({ priority, size = 'medium' }) => {
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

  return (
    <Badge
      backgroundColor={getPriorityColor(priority)}
      variant="priority"
      size={size}
    >
      {priority}
    </Badge>
  );
};

export const CountBadge = ({ count, color = '#3498db', size = 'small' }) => {
  return (
    <Badge
      backgroundColor={color}
      variant="count"
      size={size}
    >
      {count}
    </Badge>
  );
};

export { Badge };
export default Badge;
