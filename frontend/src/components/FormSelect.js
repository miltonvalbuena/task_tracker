import React from 'react';

const FormSelect = ({ 
  name, 
  value, 
  onChange, 
  options, 
  label, 
  required = false,
  placeholder = "Seleccionar...",
  disabled = false,
  ...props 
}) => {
  return (
    <div>
      <label style={{
        display: 'block',
        marginBottom: '8px',
        fontWeight: '600',
        color: '#2c3e50',
        fontSize: '14px',
        textTransform: 'uppercase',
        letterSpacing: '0.5px'
      }}>
        {label} {required && <span style={{ color: '#e74c3c' }}>*</span>}
      </label>
      <select
        name={name}
        value={value}
        onChange={onChange}
        disabled={disabled}
        style={{
          width: '100%',
          padding: '12px 16px',
          border: '2px solid #ecf0f1',
          borderRadius: '8px',
          fontSize: '14px',
          fontWeight: '500',
          background: disabled ? '#f8f9fa' : '#ffffff',
          color: disabled ? '#6c757d' : '#2c3e50',
          cursor: disabled ? 'not-allowed' : 'pointer',
          transition: 'all 0.3s ease',
          outline: 'none',
          boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
        }}
        onFocus={(e) => {
          if (!disabled) {
            e.target.style.borderColor = '#3498db';
            e.target.style.background = '#ffffff';
            e.target.style.boxShadow = '0 0 0 3px rgba(52,152,219,0.1)';
          }
        }}
        onBlur={(e) => {
          e.target.style.borderColor = '#ecf0f1';
          e.target.style.background = disabled ? '#f8f9fa' : '#ffffff';
          e.target.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)';
        }}
        {...props}
      >
        <option value="">{placeholder}</option>
        {options?.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default FormSelect;
