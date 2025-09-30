import React from 'react';
import { useConfig } from '../contexts/ConfigContext';

function Logo({ size = 'medium', style = {} }) {
  const { config } = useConfig();
  const getSizeStyles = () => {
    switch (size) {
      case 'small':
        return {
          fontSize: '18px',
          lineHeight: '1.2'
        };
      case 'large':
        return {
          fontSize: '32px',
          lineHeight: '1.2'
        };
      case 'xlarge':
        return {
          fontSize: '48px',
          lineHeight: '1.2'
        };
      default: // medium
        return {
          fontSize: '24px',
          lineHeight: '1.2'
        };
    }
  };

  const logoStyles = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    textAlign: 'center',
    fontFamily: 'Arial, sans-serif',
    fontWeight: 'bold',
    ...getSizeStyles(),
    ...style
  };

  const topTextStyle = {
    color: config.logo.primaryColor,
    margin: '0',
    letterSpacing: '1px'
  };

  const lineStyle = {
    width: '100%',
    height: '3px',
    backgroundColor: config.logo.primaryColor,
    margin: '4px 0',
    borderRadius: '2px'
  };

  const bottomTextStyle = {
    color: config.logo.secondaryColor,
    margin: '0',
    letterSpacing: '0.5px',
    fontSize: size === 'xlarge' ? '0.6em' : size === 'large' ? '0.65em' : size === 'small' ? '0.7em' : '0.7em'
  };

  return (
    <div style={logoStyles}>
      <div style={topTextStyle}>{config.logo.companyName}</div>
      <div style={lineStyle}></div>
      <div style={bottomTextStyle}>{config.logo.tagline}</div>
      <div style={lineStyle}></div>
    </div>
  );
}

export default Logo;
