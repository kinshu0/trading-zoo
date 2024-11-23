import React from 'react';
import Header from './components/Header';
import { HeroSection } from './components/HeroSection';
import TeamSection from './components/TeamSection';
import AssetSection from './components/AssetSection';
import TradingPit from './components/TradingPit';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-green-100 relative">
{/*       <div className="absolute top-0 right-0 m-4 bg-yellow-100 text-green-800 px-4 py-2 rounded-md shadow-md">
        Humans Welcome! 👋
      </div> */}
      <Header />
      <main className="container mx-auto px-4 py-8">
        <HeroSection />
        <TeamSection />
        <AssetSection />
        <TradingPit />
      </main>
    </div>
  );
}

export default App;

