import React, { useState, useEffect } from 'react';
import Button from './ui/Button';
import TimeGraph from './TimeGraph';
import TradeHistoryPopup from './TradeHistoryPopup';
import { getRandomEvent } from '../data/events';

const initialPrices = {
  Bananas: 10,
  Ice: 15,
  Pineapples: 20,
  Fish: 25,
  Pebbles: 50
};

const teams = ['Monkeys', 'Penguins', 'Foxes', 'Iguanas'];
const teamColors = {
  Monkeys: 'rgb(255, 205, 86)',
  Penguins: 'rgb(54, 162, 235)',
  Foxes: 'rgb(255, 99, 132)',
  Iguanas: 'rgb(75, 192, 192)'
};

function generateTrade() {
  const team = teams[Math.floor(Math.random() * teams.length)]
  const asset = Object.keys(initialPrices)[Math.floor(Math.random() * Object.keys(initialPrices).length)]
  const quantity = Math.floor(Math.random() * 10) + 1
  const price = initialPrices[asset] * (1 + (Math.random() - 0.5) * 0.1)
  const type = Math.random() > 0.5 ? 'buy' : 'sell'
  return { team, asset, quantity, price, type }
}

const TradingPit = () => {
  const [messages, setMessages] = useState([]);
  const [prices, setPrices] = useState(initialPrices);
  const [teamBalances, setTeamBalances] = useState(teams.reduce((acc, team) => ({ ...acc, [team]: 1000 }), {}));
  const [graphData, setGraphData] = useState({
    labels: [],
    datasets: teams.map(team => ({
      label: team,
      data: [],
      borderColor: teamColors[team],
      backgroundColor: teamColors[team] + '40',
    }))
  });
  const [currentEvent, setCurrentEvent] = useState(null);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const [tradeHistory, setTradeHistory] = useState(teams.reduce((acc, team) => ({ ...acc, [team]: [] }), {}));
  const [eventHistory, setEventHistory] = useState([]);

  const addTrade = () => {
    const trade = generateTrade()
    const action = trade.type === 'buy' ? 'bought' : 'sold'
    const newMessage = `${trade.team} ${action} ${trade.quantity} ${trade.asset} at ${trade.price.toFixed(2)} Jungle Coins each!`
    setMessages(prevMessages => [newMessage, ...prevMessages.slice(0, 4)])
    
    setPrices(prevPrices => {
      const newPrices = { ...prevPrices };
      newPrices[trade.asset] = prevPrices[trade.asset] * (1 + (Math.random() - 0.5) * 0.05);
      return newPrices;
    });

    setTeamBalances(prevBalances => {
      const newBalances = { ...prevBalances }
      const totalCost = trade.quantity * trade.price
      newBalances[trade.team] += trade.type === 'sell' ? totalCost : -totalCost
      return newBalances
    })

    setGraphData(prevData => {
      const newData = { ...prevData };
      const currentTime = new Date().toLocaleTimeString();
      newData.labels.push(currentTime);
      newData.datasets.forEach(dataset => {
        dataset.data.push(teamBalances[dataset.label]);
      });
      if (newData.labels.length > 20) {
        newData.labels.shift();
        newData.datasets.forEach(dataset => dataset.data.shift());
      }
      return newData;
    });

    setTradeHistory(prevHistory => ({
      ...prevHistory,
      [trade.team]: [...prevHistory[trade.team], trade],
    }))
  };

  const triggerEvent = () => {
    const event = getRandomEvent();
    setCurrentEvent(event);
    setPrices(prevPrices => {
      const newPrices = { ...prevPrices };
      newPrices[event.effect.asset] *= event.effect.multiplier;
      return newPrices;
    });
    setMessages(prevMessages => [`EVENT: ${event.name} - ${event.description}`, ...prevMessages.slice(0, 4)]);
    setEventHistory(prevHistory => [...prevHistory, event]);
  };

  useEffect(() => {
    const tradeInterval = setInterval(addTrade, 5000);
    const eventInterval = setInterval(triggerEvent, 15000);
    return () => {
      clearInterval(tradeInterval);
      clearInterval(eventInterval);
    };
  }, []);

  return (
    <section className="py-16 bg-gradient-to-br from-green-50 to-green-100 rounded-lg shadow-lg my-8">
      <h3 className="text-3xl font-display mb-8 text-center text-green-900">Live Trading Pit</h3>
      {currentEvent && (
        <div className="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4" role="alert">
          <p className="font-display">{currentEvent.name}</p>
          <p>{currentEvent.description}</p>
        </div>
      )}
      <div className="flex flex-wrap justify-center gap-8">
        <div className="bg-white/80 backdrop-blur-sm w-full max-w-md p-6 rounded-lg shadow-md">
          <h4 className="text-xl font-semibold mb-4 text-center">Latest Trades & Events</h4>
          <ul className="space-y-2 mb-4">
            {messages.map((message, index) => (
              <li key={index} className={`p-3 rounded-lg shadow text-green-800 animate-fade-in ${message.startsWith('EVENT') ? 'bg-yellow-50' : 'bg-green-50'}`}>
                {message}
              </li>
            ))}
          </ul>
          <Button onClick={addTrade} className="w-full bg-green-500 hover:bg-green-600 text-white">
            Simulate Trade
          </Button>
        </div>
        <div className="bg-white/80 backdrop-blur-sm w-full max-w-md p-6 rounded-lg shadow-md">
          <h4 className="text-xl font-semibold mb-4 text-center">Current Prices (Jungle Coins)</h4>
          <ul className="space-y-2">
            {Object.entries(prices).map(([asset, price]) => (
              <li key={asset} className="bg-green-50 p-3 rounded-lg shadow text-green-800 flex justify-between items-center">
                <span>{asset}</span>
                <span className="font-bold">{price.toFixed(2)} JC</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="mt-8 bg-white/80 backdrop-blur-sm w-full p-6 rounded-lg shadow-md">
        <h4 className="text-xl font-semibold mb-4 text-center">Team Performance</h4>
        <TimeGraph data={graphData} />
      </div>
      <div className="mt-8 text-center">
        <Button onClick={() => setIsPopupOpen(true)} className="bg-blue-500 hover:bg-blue-600 text-white">
          View Trade History and Events
        </Button>
      </div>
      <TradeHistoryPopup
        isOpen={isPopupOpen}
        onClose={() => setIsPopupOpen(false)}
        trades={tradeHistory}
        events={eventHistory}
      />
    </section>
  );
};

export default TradingPit;

