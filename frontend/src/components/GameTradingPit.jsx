import React, { useEffect, useState } from 'react';
import TimeGraph from './TimeGraph';
import api from '../services/api';

const teams = ['monkeys', 'penguins', 'foxes', 'iguanas'];
const teamColors = {
  monkeys: 'rgb(255, 205, 86)',
  penguins: 'rgb(54, 162, 235)',
  foxes: 'rgb(255, 99, 132)',
  iguanas: 'rgb(75, 192, 192)'
};

const GameTradingPit = () => {
  const [graphData, setGraphData] = useState({
    labels: [],
    datasets: teams.map(team => ({
      label: team.charAt(0).toUpperCase() + team.slice(1),
      data: [],
      borderColor: teamColors[team],
      backgroundColor: 'transparent',
      tension: 0.1,
      animation: false
    }))
  });

  const fetchValuationHistory = async () => {
    try {
      const historyRes = await api.get('/valuation_history');
      
      if (historyRes.data) {
        setGraphData(prevData => {
          const newData = { ...prevData };
          
          // Clear existing data
          newData.labels = [];
          newData.datasets.forEach(dataset => {
            dataset.data = [];
          });

          // Get the maximum length of history across all teams
          const maxLength = Math.max(...Object.values(historyRes.data)
            .map(history => history.length));

          // Create fewer labels for x-axis
          const labelInterval = Math.max(1, Math.floor(maxLength / 4));
          newData.labels = Array.from({ length: maxLength }, (_, i) => 
            i % labelInterval === 0 ? `Tick ${i + 1}` : ''
          );

          // Update each team's data
          newData.datasets.forEach(dataset => {
            const teamName = dataset.label.toLowerCase();
            const teamHistory = historyRes.data[teamName] || [];
            dataset.data = teamHistory;
          });

          return newData;
        });
      }
    } catch (error) {
      console.error('Failed to fetch valuation history:', error);
    }
  };

  useEffect(() => {
    fetchValuationHistory();
    const interval = setInterval(fetchValuationHistory, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <TimeGraph 
        data={graphData} 
        options={{
          animation: false,
          scales: {
            x: {
              ticks: {
                callback: function(val, index) {
                  // Only show label if it's not empty
                  return this.getLabelForValue(val)
                }
              }
            }
          }
        }}
      />
    </div>
  );
};

export default GameTradingPit;