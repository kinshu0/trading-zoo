import React from 'react';

const Button = ({ children, variant = 'default', className = '', ...props }) => {
  const baseStyles = 'px-4 py-2 rounded font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2';
  const variantStyles = {
    default: 'bg-blue-500 text-white hover:bg-blue-600 focus:ring-blue-500',
    outline: 'bg-transparent border border-current hover:bg-gray-100 focus:ring-gray-500',
  };

  const combinedClassName = `${baseStyles} ${variantStyles[variant]} ${className}`;

  return (
    <button className={combinedClassName} {...props}>
      {children}
    </button>
  );
};

export default Button;

