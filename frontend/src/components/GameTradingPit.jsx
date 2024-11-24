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
      backgroundColor: teamColors[team] + '40',
    }))
  });

  const fetchPortfolioValues = async () => {
    try {
      const clientsRes = await api.get('/clients');
      const currentTime = new Date().toLocaleTimeString();

      setGraphData(prevData => {
        const newData = { ...prevData };
        newData.labels.push(currentTime);

        newData.datasets.forEach(dataset => {
          const teamName = dataset.label.toLowerCase();
          const teamData = clientsRes.data[teamName];
          
          if (teamData) {
            const portfolioValue = teamData.portfolio.reduce((total, holding) => {
              return total + (holding.quantity * holding.price);
            }, 0);
            
            const totalValue = portfolioValue + teamData.balance;
            dataset.data.push(totalValue);
          }
        });

        if (newData.labels.length > 20) {
          newData.labels.shift();
          newData.datasets.forEach(dataset => dataset.data.shift());
        }

        return newData;
      });
    } catch (error) {
      console.error('Failed to fetch portfolio values:', error);
    }
  };

  useEffect(() => {
    fetchPortfolioValues();

    const interval = setInterval(fetchPortfolioValues, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <TimeGraph data={graphData} />
    </div>
  );
};

export default GameTradingPit;