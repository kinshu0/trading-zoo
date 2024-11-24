import React from 'react';

const assets = [
  { name: 'Bananas', icon: '🍌', description: 'A staple food for many', color: 'from-yellow-100 to-yellow-200' },
  { name: 'Ice', icon: '🧊', description: 'Essential for cool drinks', color: 'from-blue-100 to-blue-200' },
  { name: 'Pineapples', icon: '🍍', description: 'Tropical luxury fruit', color: 'from-yellow-200 to-green-100' },
  { name: 'Fish', icon: '🐟', description: 'For the best sushi', color: 'from-purple-100 to-purple-200' },
  { name: 'Pebbles', icon: '🪨', description: 'Beach treasure', color: 'from-blue-200 to-green-100' },
];

const AssetSection = () => {
  return (
    <section className="py-16 bg-gradient-to-br from-green-100 to-yellow-100 rounded-lg shadow-lg my-8">
      <h3 className="text-4xl font-display tracking-wide mb-8 text-center text-green-900">Tradable Assets</h3>      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {assets.map((asset) => (
          <div key={asset.name} className={`bg-gradient-to-br ${asset.color} shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105 rounded-lg p-6 flex flex-col items-center`}>
            <span className="text-6xl mb-4 animate-bounce-slow">{asset.icon}</span>
            <h4 className="text-xl font-bold mb-2 font-jungle">{asset.name}</h4>
            <p className="text-center text-sm text-green-800">{asset.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default AssetSection;

