import React from 'react';
import { Link } from 'react-router-dom';

const LinkButton = ({ 
  to, 
  children, 
  variant = 'secondary',
  size = 'small',
  icon: Icon,
  ...props 
}) => {
  const getVariantStyles = () => {
    switch (variant) {
      case 'primary':
        return {
          background: '#3498db',
          hoverBackground: '#2980b9',
          shadow: '0 4px 12px rgba(52, 152, 219, 0.3)',
          hoverShadow: '0 6px 16px rgba(52, 152, 219, 0.4)'
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
      default: // secondary
        return {
          background: '#6c757d',
          hoverBackground: '#5a6268',
          shadow: '0 4px 12px rgba(108, 117, 125, 0.3)',
          hoverShadow: '0 6px 16px rgba(108, 117, 125, 0.4)'
        };
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          padding: '8px 12px',
          fontSize: '12px',
          gap: '4px'
        };
      case 'medium':
        return {
          padding: '12px 24px',
          fontSize: '14px',
          gap: '8px'
        };
      case 'large':
        return {
          padding: '16px 32px',
          fontSize: '16px',
          gap: '12px'
        };
      default:
        return {
          padding: '8px 12px',
          fontSize: '12px',
          gap: '4px'
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
    background: variantStyles.background,
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: sizeStyles.fontSize,
    fontWeight: '500',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    textDecoration: 'none',
    padding: sizeStyles.padding,
    boxShadow: variantStyles.shadow,
    outline: 'none'
  };

  const handleMouseEnter = (e) => {
    e.currentTarget.style.transform = 'translateY(-2px)';
    e.currentTarget.style.boxShadow = variantStyles.hoverShadow;
  };

  const handleMouseLeave = (e) => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.boxShadow = variantStyles.shadow;
  };

  return (
    <Link
      to={to}
      style={baseStyles}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      {...props}
    >
      {Icon && <Icon size={14} />}
      {children}
    </Link>
  );
};

export default LinkButton;

