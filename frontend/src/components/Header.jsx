import React from 'react';
import Button from './ui/Button';

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-green-600 to-green-800 text-white p-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-3xl font-medium flex items-center tracking-wide">
          <span className="mr-2">🦁</span>
          Trading Zoo
        </h1>
        <nav>
          <Button 
            variant="outline" 
            className="font-display text-white border-white hover:bg-green-700 transition-colors duration-300"
          >
            Start Trading
          </Button>
        </nav>
      </div>
    </header>
  );
};

export default Header;

