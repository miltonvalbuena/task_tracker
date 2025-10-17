import React from 'react';

const ActionButton = ({ 
  children, 
  type = 'button',
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  onClick,
  icon: Icon,
  ...props 
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'secondary':
        return {
          background: '#6c757d',
          hoverBackground: '#5a6268',
          shadow: '0 4px 12px rgba(108, 117, 125, 0.3)',
          hoverShadow: '0 6px 16px rgba(108, 117, 125, 0.4)'
        };
      case 'danger':
        return {
          background: '#dc3545',
          hoverBackground: '#c82333',
          shadow: '0 4px 12px rgba(220, 53, 69, 0.3)',
          hoverShadow: '0 6px 16px rgba(220, 53, 69, 0.4)'
        };
      case 'success':
        return {
          background: '#28a745',
          hoverBackground: '#218838',
          shadow: '0 4px 12px rgba(40, 167, 69, 0.3)',
          hoverShadow: '0 6px 16px rgba(40, 167, 69, 0.4)'
        };
      default: // primary
        return {
          background: '#3498db',
          hoverBackground: '#2980b9',
          shadow: '0 4px 12px rgba(52, 152, 219, 0.3)',
          hoverShadow: '0 6px 16px rgba(52, 152, 219, 0.4)'
        };
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          padding: '8px 16px',
          fontSize: '12px',
          gap: '6px'
        };
      case 'large':
        return {
          padding: '16px 32px',
          fontSize: '18px',
          gap: '12px'
        };
      default: // medium
        return {
          padding: '12px 24px',
          fontSize: '14px',
          gap: '8px'
        };
    }
  };

  const variantStyles = getVariantStyles();
  const sizeStyles = getSizeStyles();

  const baseStyles = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: sizeStyles.gap,
    background: disabled || loading ? '#6c757d' : variantStyles.background,
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: sizeStyles.fontSize,
    fontWeight: '600',
    cursor: disabled || loading ? 'not-allowed' : 'pointer',
    transition: 'all 0.3s ease',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
    padding: sizeStyles.padding,
    boxShadow: disabled || loading ? 'none' : variantStyles.shadow,
    outline: 'none',
    opacity: disabled || loading ? 0.7 : 1
  };

  const handleMouseEnter = (e) => {
    if (!disabled && !loading) {
      e.currentTarget.style.transform = 'translateY(-2px)';
      e.currentTarget.style.boxShadow = variantStyles.hoverShadow;
    }
  };

  const handleMouseLeave = (e) => {
    if (!disabled && !loading) {
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = variantStyles.shadow;
    }
  };

  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      style={baseStyles}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      {...props}
    >
      {loading ? (
        <span style={{ 
          width: '16px', 
          height: '16px', 
          border: '2px solid transparent',
          borderTop: '2px solid white',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
      ) : Icon ? (
        <Icon size={16} />
      ) : null}
      {children}
    </button>
  );
};

export default ActionButton;
