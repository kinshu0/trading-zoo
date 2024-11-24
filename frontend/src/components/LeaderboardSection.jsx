import React from 'react';

const mockLeaderboard = [
  { rank: 1, team: 'Monkeys', icon: '🐒', balance: 10000, topAsset: 'Bananas' },
  { rank: 2, team: 'Penguins', icon: '🐧', balance: 8500, topAsset: 'Ice' },
  { rank: 3, team: 'Foxes', icon: '🦊', balance: 7200, topAsset: 'Fish' },
  { rank: 4, team: 'Iguanas', icon: '🦎', balance: 6800, topAsset: 'Pebbles' },
];

const LeaderboardSection = () => {
  return (
    <section className="py-16 bg-gradient-to-br from-green-200 to-yellow-200 rounded-lg shadow-lg my-8">
      <h3 className="text-3xl font-bold mb-8 text-center text-green-900">Current Standings</h3>
      <div className="overflow-x-auto px-4">
        <table className="w-full">
          <thead>
            <tr className="bg-green-600 text-white">
              <th className="text-center py-2">Rank</th>
              <th className="py-2">Team</th>
              <th className="text-right py-2">Balance (JC)</th>
              <th className="py-2">Top Asset</th>
            </tr>
          </thead>
          <tbody>
            {mockLeaderboard.map((entry) => (
              <tr key={entry.rank} className="bg-white/60 hover:bg-white/80 transition-colors duration-200">
                <td className="text-center font-medium py-2">{entry.rank}</td>
                <td className="flex items-center py-2">
                  <span className="text-2xl mr-2">{entry.icon}</span>
                  {entry.team}
                </td>
                <td className="text-right font-bold text-green-700 py-2">{entry.balance.toLocaleString()} JC</td>
                <td className="py-2">{entry.topAsset}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};

export default LeaderboardSection;

