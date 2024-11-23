import React from 'react';
import Button from './ui/Button';
import { useNavigate, useLocation } from 'react-router-dom'

const Header = () => {
  const navigate = useNavigate()
  const location = useLocation()
  
  return (
    <header className="bg-gradient-to-r from-green-600 to-green-800 text-white p-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <h1 
          className="text-3xl font-medium flex items-center tracking-wide cursor-pointer" 
          onClick={() => navigate('/')}
        >
          <span className="mr-2">🦁</span>
          Trading Zoo
        </h1>
        <nav>
          {location.pathname === '/' ? (
            <Button 
              variant="outline" 
              className="font-display text-white border-white hover:bg-green-700 transition-colors duration-300"
              onClick={() => navigate('/game')}
            >
              Start Trading
            </Button>
          ) : (
            <Button 
              variant="outline" 
              className="font-display text-white border-white hover:bg-green-700 transition-colors duration-300"
              onClick={() => navigate('/')}
            >
              Back to Home
            </Button>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;

