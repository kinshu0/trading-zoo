import React, { useState } from 'react';
import Modal from './Modal';

const teams = [
  { 
    name: 'Penguins', 
    icon: '🐧', 
    description: 'Cool traders from the South', 
    color: 'from-blue-50 to-blue-100',
    agents: [
      { name: 'Pingu', role: 'Trader', specialty: 'Ice futures', avatar: '🧊' },
      { name: 'Frosty', role: 'Analyst', specialty: 'Climate trends', avatar: '❄️' },
      { name: 'Waddle', role: 'Negotiator', specialty: 'Cold calls', avatar: '🐾' }
    ]
  },
  { 
    name: 'Monkeys', 
    icon: '🐒', 
    description: 'Agile and clever merchants', 
    color: 'from-yellow-50 to-yellow-100',
    agents: [
      { name: 'Bananas', role: 'Trader', specialty: 'Fruit arbitrage', avatar: '🍌' },
      { name: 'Curious George', role: 'Analyst', specialty: 'Jungle economics', avatar: '🌴' },
      { name: 'Chimpy', role: 'Risk Manager', specialty: 'Vine swinging investments', avatar: '🦧' }
    ]
  },
  { 
    name: 'Foxes', 
    icon: '🦊', 
    description: 'Cunning market analysts', 
    color: 'from-orange-50 to-orange-100',
    agents: [
      { name: 'Sly', role: 'Trader', specialty: 'Options trading', avatar: '🦊' },
      { name: 'Sherlock', role: 'Analyst', specialty: 'Market psychology', avatar: '🔍' },
      { name: 'Vixen', role: 'Strategist', specialty: 'Trend prediction', avatar: '📈' }
    ]
  },
  { 
    name: 'Iguanas', 
    icon: '🦎', 
    description: 'Patient long-term investors', 
    color: 'from-green-50 to-green-100',
    agents: [
      { name: 'Scales', role: 'Trader', specialty: 'Long-term holds', avatar: '⏳' },
      { name: 'Sunny', role: 'Analyst', specialty: 'Climate impact analysis', avatar: '☀️' },
      { name: 'Spiky', role: 'Risk Assessor', specialty: 'Defensive investments', avatar: '🛡️' }
    ]
  },
];

const TeamSection = () => {
  const [selectedTeam, setSelectedTeam] = useState(null);

  return (
    <section className="py-16">
      <h3 className="text-3xl font-bold mb-8 text-center text-green-900">Meet the Teams</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {teams.map((team) => (
          <div 
            key={team.name} 
            className={`bg-gradient-to-br ${team.color} shadow-md hover:shadow-lg transition-all transform hover:scale-102 duration-300 rounded-lg p-6 cursor-pointer`}
            onClick={() => setSelectedTeam(team)}
          >
            <h4 className="text-2xl flex items-center justify-center mb-4">
              <span className="text-4xl mr-2">{team.icon}</span>
              {team.name}
            </h4>
            <p className="text-center text-green-800 mb-4">{team.description}</p>
          </div>
        ))}
      </div>
      <Modal isOpen={!!selectedTeam} onClose={() => setSelectedTeam(null)}>
        {selectedTeam && (
          <div>
            <h2 className="text-3xl font-display mb-4 flex items-center">
              <span className="text-5xl mr-3">{selectedTeam.icon}</span>
              {selectedTeam.name}
            </h2>
            <p className="text-lg mb-6">{selectedTeam.description}</p>
            <h3 className="text-2xl font-display mb-4">Team Members</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {selectedTeam.agents.map((agent, index) => (
                <div key={index} className="bg-gray-50 p-4 rounded-lg">
                  <div className="text-4xl mb-2">{agent.avatar}</div>
                  <h4 className="font-display">{agent.name}</h4>
                  <p className="text-sm text-gray-600">{agent.role}</p>
                  <p className="text-sm">{agent.specialty}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </Modal>
    </section>
  );
};

export default TeamSection;

