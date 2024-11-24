import React, { useEffect, useState } from 'react';
import TimeGraph from './TimeGraph';

const teams = ['Monkeys', 'Penguins', 'Foxes', 'Iguanas'];
const teamColors = {
  Monkeys: 'rgb(255, 205, 86)',
  Penguins: 'rgb(54, 162, 235)',
  Foxes: 'rgb(255, 99, 132)',
  Iguanas: 'rgb(75, 192, 192)'
};

const GameTradingPit = () => {
  const [graphData, setGraphData] = useState({
    labels: [],
    datasets: teams.map(team => ({
      label: team,
      data: [],
      borderColor: teamColors[team],
      backgroundColor: teamColors[team] + '40',
    }))
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setGraphData(prevData => {
        const newData = { ...prevData };
        const currentTime = new Date().toLocaleTimeString();
        newData.labels.push(currentTime);
        newData.datasets.forEach(dataset => {
          const lastValue = dataset.data[dataset.data.length - 1] || 1000;
          const change = (Math.random() - 0.5) * 100;
          dataset.data.push(lastValue + change);
        });
        if (newData.labels.length > 20) {
          newData.labels.shift();
          newData.datasets.forEach(dataset => dataset.data.shift());
        }
        return newData;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <TimeGraph data={graphData} />
    </div>
  );
};

export default GameTradingPit;